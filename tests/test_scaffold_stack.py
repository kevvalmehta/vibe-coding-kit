"""Guard test for the stack scaffolder (Conductor v7).

Spec: specs/013-stack-scaffold/spec.md  ·  Plan: specs/013-stack-scaffold/plan.md

Written FIRST (TDD). Pure filesystem/stdlib — no network/model. Guards that the scaffolder creates the
minimal starter per stack, includes a deploy note, NEVER overwrites existing files, declines unknown
stacks, and exits 0.
"""
import importlib.util
import io
from pathlib import Path

from _kitpaths import scripts_dir

ROOT = Path(__file__).resolve().parent.parent
SCAFFOLD = scripts_dir(ROOT) / "scaffold_stack.py"

_spec = importlib.util.spec_from_file_location("scaffold_stack", SCAFFOLD)
scaffold_stack = importlib.util.module_from_spec(_spec)
if _spec.loader and SCAFFOLD.exists():
    _spec.loader.exec_module(scaffold_stack)

_COMMON = (".gitignore", ".env.example", "README.md")
_PYTHON_STACKS = ("streamlit", "fastapi", "python-script")


def test_T1_script_exists():
    assert SCAFFOLD.exists(), "scripts/scaffold_stack.py missing"


def test_T2_lists_supported_stacks():
    stacks = scaffold_stack.list_stacks()
    for key in (*_PYTHON_STACKS, "nextjs", "static-site"):
        assert key in stacks, f"stack not supported: {key}"


def test_T3_creates_common_files_and_deploy_note(tmp_path):
    for key in scaffold_stack.list_stacks():
        target = tmp_path / key
        scaffold_stack.scaffold(key, target)
        for fname in _COMMON:
            assert (target / fname).exists(), f"{key}: missing {fname}"
        readme = (target / "README.md").read_text(encoding="utf-8").lower()
        assert "put this live" in readme, f"{key}: README missing the 'put this live' deploy note"


def test_T4_python_stacks_are_runnable_skeletons(tmp_path):
    for key in _PYTHON_STACKS:
        target = tmp_path / key
        scaffold_stack.scaffold(key, target)
        assert (target / "requirements.txt").exists(), f"{key}: missing requirements.txt"
        entries = list(target.glob("*.py"))
        assert entries, f"{key}: missing a Python entry file"


def test_T5_never_overwrites_existing_file(tmp_path):
    target = tmp_path / "streamlit"
    target.mkdir()
    (target / "README.md").write_text("MY CUSTOM README", encoding="utf-8")
    result = scaffold_stack.scaffold("streamlit", target)
    # the existing file is untouched...
    assert (target / "README.md").read_text(encoding="utf-8") == "MY CUSTOM README"
    assert "README.md" in [Path(p).name for p in result["skipped"]], "existing file not reported skipped"
    # ...but the missing files were created
    assert (target / "app.py").exists() and (target / ".gitignore").exists()


def test_T6_unknown_stack_writes_nothing(tmp_path):
    target = tmp_path / "weird"
    result = scaffold_stack.scaffold("not-a-real-stack", target)
    assert result.get("unknown") is True, "unknown stack must be flagged"
    # nothing written — not even the target dir created
    assert not target.exists(), "unknown stack must not create the target dir or any files"


def test_T7_main_exits_zero(tmp_path, monkeypatch):
    cap = io.StringIO()
    monkeypatch.setattr("sys.stdout", cap)
    code = scaffold_stack.main(["streamlit", str(tmp_path / "app")])
    assert code == 0
    assert "created" in cap.getvalue().lower()


def test_T8_main_unknown_stack_exits_zero_and_says_so(tmp_path, monkeypatch):
    cap = io.StringIO()
    monkeypatch.setattr("sys.stdout", cap)
    code = scaffold_stack.main(["bogus", str(tmp_path / "x")])
    assert code == 0
    out = cap.getvalue().lower()
    assert "not" in out and ("scaffold" in out or "supported" in out), "must say it can't scaffold that"
