# tests/test_spec_drift_warn.py
"""Spec-drift warner mechanizes spec-anchored development: committing code without touching
the spec quietly drifts the project away from its own source of truth. This hook WARNS at
commit time (never blocks). Code staged + no spec staged -> warn; spec also staged -> silent."""
import importlib.util
import subprocess
from pathlib import Path

from _kitpaths import scripts_dir

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location(
    "spec_drift_warn", scripts_dir(ROOT) / "spec_drift_warn.py"
)
sdw = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sdw)


def make_repo(tmp_path):
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.email", "t@t"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=tmp_path, check=True)
    (tmp_path / "seed.txt").write_text("seed\n", encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-qm", "first commit"], cwd=tmp_path, check=True)
    return tmp_path


def stage(tmp_path, rel, content="x\n"):
    p = tmp_path / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    subprocess.run(["git", "add", str(rel)], cwd=tmp_path, check=True)


def commit_hook_data(tmp_path):
    return {
        "tool_name": "Bash",
        "tool_input": {"command": "git commit -m 'work'"},
        "cwd": str(tmp_path),
    }


def test_non_commit_command_is_silent(tmp_path):
    make_repo(tmp_path)
    stage(tmp_path, "src/app.py")
    data = {"tool_name": "Bash", "tool_input": {"command": "git status"}, "cwd": str(tmp_path)}
    assert sdw.process(data) is None


def test_non_bash_tool_is_silent(tmp_path):
    make_repo(tmp_path)
    stage(tmp_path, "src/app.py")
    data = {"tool_name": "Edit", "tool_input": {"command": "git commit -m x"}, "cwd": str(tmp_path)}
    assert sdw.process(data) is None


def test_code_without_spec_warns(tmp_path):
    make_repo(tmp_path)
    stage(tmp_path, "src/app.py")
    out = sdw.process(commit_hook_data(tmp_path))
    assert out is not None
    assert "spec" in out["systemMessage"].lower()
    assert "WARNING" in out["systemMessage"]


def test_code_with_spec_change_is_silent(tmp_path):
    make_repo(tmp_path)
    stage(tmp_path, "src/app.py")
    stage(tmp_path, "specs/017-x/spec.md")
    assert sdw.process(commit_hook_data(tmp_path)) is None


def test_specify_dir_also_counts_as_spec(tmp_path):
    make_repo(tmp_path)
    stage(tmp_path, "scripts/tool.py")
    stage(tmp_path, ".specify/memory/notes.md")
    assert sdw.process(commit_hook_data(tmp_path)) is None


def test_no_source_change_is_silent(tmp_path):
    make_repo(tmp_path)
    stage(tmp_path, "README.md")
    assert sdw.process(commit_hook_data(tmp_path)) is None


def test_marker_disables(tmp_path):
    make_repo(tmp_path)
    (tmp_path / ".no-spec-drift-warn").write_text("off\n", encoding="utf-8")
    stage(tmp_path, "src/app.py")
    assert sdw.process(commit_hook_data(tmp_path)) is None


def test_non_git_dir_is_silent(tmp_path):
    data = {
        "tool_name": "Bash",
        "tool_input": {"command": "git commit -m x"},
        "cwd": str(tmp_path),
    }
    assert sdw.process(data) is None


def test_advisory_only_no_permission_decision(tmp_path):
    # An explicit "allow" would FORCE-APPROVE the command and bypass the user's normal
    # permission prompt; "deny"/"ask" would block. Advisory means: systemMessage only,
    # no hookSpecificOutput at all.
    make_repo(tmp_path)
    stage(tmp_path, "src/app.py")
    out = sdw.process(commit_hook_data(tmp_path))
    assert "hookSpecificOutput" not in out
    assert set(out.keys()) == {"systemMessage"}
