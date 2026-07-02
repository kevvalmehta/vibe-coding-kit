# tests/test_regrounding.py
"""Re-grounding kills mid-session drift: after context compression or resume, the model
gets fresh ground truth (branch, changed files, last commit) instead of trusting its
compressed memory of project state."""
import importlib.util
import subprocess
from pathlib import Path

from _kitpaths import scripts_dir

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location(
    "regrounding", scripts_dir(ROOT) / "regrounding.py"
)
regrounding = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(regrounding)


def make_repo(tmp_path):
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.email", "t@t"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=tmp_path, check=True)
    (tmp_path / "a.txt").write_text("one\n", encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-qm", "first commit"], cwd=tmp_path, check=True)
    return tmp_path


def test_snapshot_reports_branch_and_changes(tmp_path):
    make_repo(tmp_path)
    (tmp_path / "a.txt").write_text("changed\n", encoding="utf-8")
    snap = regrounding.git_snapshot(tmp_path)
    assert snap["branch"]
    assert snap["changed"] == ["a.txt"]
    assert "first commit" in snap["last_commit"]


def test_non_git_dir_is_silent(tmp_path):
    assert regrounding.process({"cwd": str(tmp_path), "source": "compact"}) is None


def test_fires_only_on_resume_or_compact(tmp_path):
    make_repo(tmp_path)
    assert regrounding.process({"cwd": str(tmp_path), "source": "startup"}) is None
    out = regrounding.process({"cwd": str(tmp_path), "source": "compact"})
    assert out["hookSpecificOutput"]["hookEventName"] == "SessionStart"


def test_context_warns_memory_is_not_proof(tmp_path):
    make_repo(tmp_path)
    (tmp_path / "HANDOFF.md").write_text("state\n", encoding="utf-8")
    out = regrounding.process({"cwd": str(tmp_path), "source": "resume"})
    ctx = out["hookSpecificOutput"]["additionalContext"]
    assert "branch" in ctx.lower()
    assert "HANDOFF.md" in ctx
    assert "not proof" in ctx.lower() or "re-verify" in ctx.lower()
