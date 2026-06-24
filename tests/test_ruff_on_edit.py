# tests/test_ruff_on_edit.py
import importlib.util
import io
import json
from pathlib import Path

from _kitpaths import scripts_dir

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location(
    "ruff_on_edit", scripts_dir(ROOT) / "ruff_on_edit.py"
)
ruff_on_edit = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ruff_on_edit)


def test_is_python_true_for_py_sources():
    assert ruff_on_edit.is_python("app/widget.py")
    assert ruff_on_edit.is_python("scripts/foo.pyi")
    assert ruff_on_edit.is_python(r"C:\proj\app\bar.py")


def test_is_python_false_for_non_python():
    assert not ruff_on_edit.is_python("README.md")
    assert not ruff_on_edit.is_python("src/index.ts")
    assert not ruff_on_edit.is_python("data/config.json")
    assert not ruff_on_edit.is_python("")


def test_build_fix_argv_targets_only_the_edited_file():
    argv = ruff_on_edit.build_fix_argv("app/widget.py")
    assert argv == ["ruff", "check", "--fix", "app/widget.py"]


def test_main_ignores_non_edit_tools(monkeypatch):
    calls = []
    monkeypatch.setattr(ruff_on_edit, "run_fix", lambda path, cwd: calls.append(path))
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps({"tool_name": "Read"})))
    assert ruff_on_edit.main() == 0
    assert calls == []


def test_main_ignores_non_python_edits(monkeypatch):
    calls = []
    monkeypatch.setattr(ruff_on_edit, "run_fix", lambda path, cwd: calls.append(path))
    payload = {"tool_name": "Edit", "tool_input": {"file_path": "README.md"}}
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps(payload)))
    assert ruff_on_edit.main() == 0
    assert calls == []


def test_main_fixes_python_edit(monkeypatch):
    calls = []
    monkeypatch.setattr(ruff_on_edit, "run_fix", lambda path, cwd: calls.append(path))
    payload = {
        "tool_name": "Edit",
        "tool_input": {"file_path": "app/widget.py"},
        "cwd": str(ROOT),
    }
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps(payload)))
    assert ruff_on_edit.main() == 0
    assert calls == ["app/widget.py"]


def test_main_survives_garbage_stdin(monkeypatch):
    monkeypatch.setattr("sys.stdin", io.StringIO("not json"))
    assert ruff_on_edit.main() == 0
