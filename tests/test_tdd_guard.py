# tests/test_tdd_guard.py
import importlib.util
import io
import json
from pathlib import Path

import pytest

from _kitpaths import scripts_dir

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("tdd_guard", scripts_dir(ROOT) / "tdd_guard.py")
tdd_guard = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tdd_guard)


def test_classify_test_files():
    assert tdd_guard.classify("tests/test_foo.py") == "test"
    assert tdd_guard.classify("app/foo_test.py") == "test"
    assert tdd_guard.classify("src/widget.test.ts") == "test"
    assert tdd_guard.classify("src/widget.spec.ts") == "test"
    assert tdd_guard.classify(r"C:\proj\tests\test_bar.py") == "test"


def test_classify_impl_files():
    assert tdd_guard.classify("app/widget.py") == "impl"
    assert tdd_guard.classify("src/index.ts") == "impl"
    assert tdd_guard.classify("src/app.jsx") == "impl"


def test_classify_noncode_files():
    assert tdd_guard.classify("README.md") == "noncode"
    assert tdd_guard.classify("data/config.json") == "noncode"
    assert tdd_guard.classify("notes.txt") == "noncode"


def test_decide_guard_off_allows_everything():
    assert tdd_guard.decide(None, "impl", False) == "allow"


def test_decide_strict_allows_test_and_noncode():
    assert tdd_guard.decide("strict", "test", False) == "allow"
    assert tdd_guard.decide("strict", "noncode", False) == "allow"


def test_decide_strict_blocks_impl_when_green():
    assert tdd_guard.decide("strict", "impl", False) == "block"


def test_decide_strict_allows_impl_when_red():
    assert tdd_guard.decide("strict", "impl", True) == "allow"


def test_decide_refactor_allows_impl_when_green():
    assert tdd_guard.decide("refactor", "impl", False) == "allow"


def test_decide_unknown_mode_defaults_to_strict():
    assert tdd_guard.decide("strikt", "impl", False) == "block"


def test_read_marker_absent_returns_default_on(tmp_path):
    """Spec 016 Phase 2: TDD is a constitution hard rule, so the guard is ON by default —
    no marker means strict mode, not off."""
    cfg = tdd_guard.read_marker(tmp_path)
    assert cfg is not None
    assert cfg["mode"] == "strict"
    assert cfg["explicit"] is False


def test_off_marker_disables_guard(tmp_path):
    (tmp_path / ".no-tdd-guard").write_text("scratch project\n", encoding="utf-8")
    assert tdd_guard.read_marker(tmp_path) is None


def test_read_marker_defaults_to_strict_and_pytest(tmp_path):
    (tmp_path / ".tdd-guard").write_text("", encoding="utf-8")
    cfg = tdd_guard.read_marker(tmp_path)
    assert cfg["mode"] == "strict"
    assert cfg["test"] == "python -m pytest -q"


def test_read_marker_parses_mode_and_test(tmp_path):
    (tmp_path / ".tdd-guard").write_text(
        "# comment line\nmode: refactor\ntest: pytest tests/unit -q\n", encoding="utf-8"
    )
    cfg = tdd_guard.read_marker(tmp_path)
    assert cfg["mode"] == "refactor"
    assert cfg["test"] == "pytest tests/unit -q"


def test_tests_are_red_true_on_nonzero_exit(monkeypatch):
    class FakeResult:
        returncode = 1

    monkeypatch.setattr(tdd_guard.subprocess, "run", lambda *a, **k: FakeResult())
    assert tdd_guard.tests_are_red("python -m pytest -q", ".") is True


def test_tests_are_red_false_on_zero_exit(monkeypatch):
    class FakeResult:
        returncode = 0

    monkeypatch.setattr(tdd_guard.subprocess, "run", lambda *a, **k: FakeResult())
    assert tdd_guard.tests_are_red("python -m pytest -q", ".") is False


def _run_main(monkeypatch, capsys, payload, marker_red=None):
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps(payload)))
    if marker_red is not None:
        monkeypatch.setattr(tdd_guard, "tests_are_red", lambda *a, **k: marker_red)
    code = tdd_guard.main()
    return code, capsys.readouterr().out


def test_main_no_marker_impl_green_blocks(monkeypatch, capsys, tmp_path):
    """Default-on: even without a .tdd-guard marker, an impl edit on a green suite blocks."""
    payload = {"tool_name": "Edit", "tool_input": {"file_path": "app/x.py"}, "cwd": str(tmp_path)}
    code, out = _run_main(monkeypatch, capsys, payload, marker_red=False)
    assert code == 0
    data = json.loads(out)
    assert data["hookSpecificOutput"]["permissionDecision"] == "deny"
    assert ".no-tdd-guard" in data["hookSpecificOutput"]["permissionDecisionReason"]


def test_main_no_marker_impl_red_allows(monkeypatch, capsys, tmp_path):
    payload = {"tool_name": "Edit", "tool_input": {"file_path": "app/x.py"}, "cwd": str(tmp_path)}
    code, out = _run_main(monkeypatch, capsys, payload, marker_red=True)
    assert code == 0
    assert out.strip() == ""


def test_main_off_marker_allows_silently(monkeypatch, capsys, tmp_path):
    (tmp_path / ".no-tdd-guard").write_text("off\n", encoding="utf-8")
    payload = {"tool_name": "Edit", "tool_input": {"file_path": "app/x.py"}, "cwd": str(tmp_path)}
    code, out = _run_main(monkeypatch, capsys, payload, marker_red=False)
    assert code == 0
    assert out.strip() == ""


def test_main_default_mode_unrunnable_test_cmd_allows(monkeypatch, capsys, tmp_path):
    """Fail-open in DEFAULT mode: a project that never opted in (maybe no pytest at all)
    must not have every edit hard-blocked by a test command that can't run. Explicit
    .tdd-guard mode keeps the loud deny (tested separately)."""
    monkeypatch.setattr(
        tdd_guard,
        "tests_are_red",
        lambda *a, **k: (_ for _ in ()).throw(tdd_guard.TestCommandError("no pytest")),
    )
    payload = {"tool_name": "Edit", "tool_input": {"file_path": "app/x.py"}, "cwd": str(tmp_path)}
    code, out = _run_main(monkeypatch, capsys, payload)
    assert code == 0
    assert out.strip() == ""


def test_main_strict_impl_green_blocks(monkeypatch, capsys, tmp_path):
    (tmp_path / ".tdd-guard").write_text("mode: strict\n", encoding="utf-8")
    payload = {"tool_name": "Write", "tool_input": {"file_path": "app/x.py"}, "cwd": str(tmp_path)}
    code, out = _run_main(monkeypatch, capsys, payload, marker_red=False)
    assert code == 0
    data = json.loads(out)
    assert data["hookSpecificOutput"]["permissionDecision"] == "deny"
    assert "failing test" in data["hookSpecificOutput"]["permissionDecisionReason"].lower()


def test_main_strict_impl_red_allows(monkeypatch, capsys, tmp_path):
    (tmp_path / ".tdd-guard").write_text("mode: strict\n", encoding="utf-8")
    payload = {"tool_name": "Edit", "tool_input": {"file_path": "app/x.py"}, "cwd": str(tmp_path)}
    code, out = _run_main(monkeypatch, capsys, payload, marker_red=True)
    assert code == 0
    assert out.strip() == ""


def test_main_strict_testfile_allows_without_running_tests(monkeypatch, capsys, tmp_path):
    (tmp_path / ".tdd-guard").write_text("mode: strict\n", encoding="utf-8")
    monkeypatch.setattr(
        tdd_guard,
        "tests_are_red",
        lambda *a, **k: (_ for _ in ()).throw(AssertionError("must not run tests")),
    )
    payload = {"tool_name": "Edit", "tool_input": {"file_path": "tests/test_x.py"}, "cwd": str(tmp_path)}
    code, out = _run_main(monkeypatch, capsys, payload)
    assert code == 0
    assert out.strip() == ""


def test_main_ignores_non_edit_tools(monkeypatch, capsys, tmp_path):
    (tmp_path / ".tdd-guard").write_text("mode: strict\n", encoding="utf-8")
    payload = {"tool_name": "Bash", "tool_input": {"command": "ls"}, "cwd": str(tmp_path)}
    code, out = _run_main(monkeypatch, capsys, payload)
    assert code == 0
    assert out.strip() == ""


# C1 — malformed JSON must fail-safe (allow), not crash
def test_main_malformed_json_allows_silently(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("not valid {json"))
    code = tdd_guard.main()
    assert code == 0
    assert capsys.readouterr().out.strip() == ""


# I1 — unknown mode must still run tests (treated as strict)
def test_main_unknown_mode_impl_red_allows(monkeypatch, capsys, tmp_path):
    (tmp_path / ".tdd-guard").write_text("mode: oops\n", encoding="utf-8")
    payload = {"tool_name": "Edit", "tool_input": {"file_path": "app/x.py"}, "cwd": str(tmp_path)}
    code, out = _run_main(monkeypatch, capsys, payload, marker_red=True)
    assert code == 0
    assert out.strip() == ""


# I2 — conftest.py is test infra, not impl
def test_classify_conftest_is_test():
    assert tdd_guard.classify("conftest.py") == "test"
    assert tdd_guard.classify("app/conftest.py") == "test"


# M3 — MultiEdit coverage
def test_main_multiedit_impl_green_blocks(monkeypatch, capsys, tmp_path):
    (tmp_path / ".tdd-guard").write_text("mode: strict\n", encoding="utf-8")
    payload = {"tool_name": "MultiEdit", "tool_input": {"file_path": "app/x.py"}, "cwd": str(tmp_path)}
    code, out = _run_main(monkeypatch, capsys, payload, marker_red=False)
    assert json.loads(out)["hookSpecificOutput"]["permissionDecision"] == "deny"


# Task 6 — hook + gitignore
def test_hook_registered_in_settings():
    """Dev repo: TDD-Guard is wired in .claude/settings.json. Published-plugin repo: the PreToolUse
    wiring is intentionally NOT shipped (it would run python on every edit), so a settings.json that
    carries only plugin/marketplace config (no PreToolUse hooks at all) is allowed there. Either way,
    any shipped plugin hooks.json must parse — a broken hook config turns this RED, it never silently
    skips."""
    settings_path = ROOT / ".claude" / "settings.json"
    hook_files = sorted(ROOT.glob("plugins/*/hooks/hooks.json"))
    assert settings_path.is_file() or hook_files, "no .claude/settings.json and no plugins/*/hooks/hooks.json found"
    if settings_path.is_file():
        settings = json.loads(settings_path.read_text(encoding="utf-8"))
        pre = settings.get("hooks", {}).get("PreToolUse", [])
        if pre:
            cmds = [h.get("command", "") for entry in pre for h in entry.get("hooks", [])]
            assert any("tdd_guard.py" in c for c in cmds), "PreToolUse tdd_guard hook not registered"
    for hf in hook_files:
        json.loads(hf.read_text(encoding="utf-8"))  # must be valid JSON, not silently broken


def test_tests_are_red_raises_on_empty_command():
    with pytest.raises(tdd_guard.TestCommandError):
        tdd_guard.tests_are_red("   ", ROOT)


def test_tests_are_red_raises_on_missing_binary(tmp_path):
    with pytest.raises(tdd_guard.TestCommandError):
        tdd_guard.tests_are_red("definitely-not-a-real-binary-xyz --q", tmp_path)


def test_main_unrunnable_test_command_denies_not_crashes(tmp_path, monkeypatch, capsys):
    """A broken test command must fail LOUD (clear deny), never crash or silently allow the edit."""
    (tmp_path / ".tdd-guard").write_text(
        "mode: strict\ntest: definitely-not-a-real-binary-xyz\n", encoding="utf-8"
    )
    payload = {"tool_name": "Edit", "tool_input": {"file_path": "app/x.py"}, "cwd": str(tmp_path)}
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps(payload)))
    code = tdd_guard.main()
    out = capsys.readouterr().out
    assert code == 0
    data = json.loads(out)
    assert data["hookSpecificOutput"]["permissionDecision"] == "deny"
    assert "test command" in data["hookSpecificOutput"]["permissionDecisionReason"].lower()


def test_marker_is_gitignored():
    gi = (ROOT / ".gitignore").read_text(encoding="utf-8")
    assert ".tdd-guard" in gi, ".tdd-guard must be gitignored"
    assert ".no-tdd-guard" in gi, ".no-tdd-guard must be gitignored"


# Task 7 — portability docs
def test_registered_in_portability_maps():
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8").lower()
    skillmap = (ROOT / "SKILL-MAP.md").read_text(encoding="utf-8").lower()
    assert "tdd-guard" in agents, "TDD-Guard missing from AGENTS.md"
    assert "tdd-guard" in skillmap, "TDD-Guard missing from SKILL-MAP.md"
