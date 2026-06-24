# tests/test_recommender_nudge.py
import importlib.util
import io
import json
import time
from pathlib import Path

from _kitpaths import scripts_dir

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location(
    "recommender_nudge", scripts_dir(ROOT) / "recommender_nudge.py"
)
recommender_nudge = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(recommender_nudge)


def _make_project(tmp_path, manifest="package.json"):
    if manifest:
        (tmp_path / manifest).write_text("{}", encoding="utf-8")
    return tmp_path


def test_is_real_project_true_with_manifest(tmp_path):
    _make_project(tmp_path)
    assert recommender_nudge.is_real_project(tmp_path)


def test_is_real_project_true_with_git(tmp_path):
    (tmp_path / ".git").mkdir()
    assert recommender_nudge.is_real_project(tmp_path)


def test_is_real_project_false_when_empty(tmp_path):
    assert not recommender_nudge.is_real_project(tmp_path)


def test_should_nudge_fresh_project(tmp_path):
    _make_project(tmp_path)
    assert recommender_nudge.should_nudge(tmp_path)


def test_should_not_nudge_after_marker(tmp_path):
    _make_project(tmp_path)
    recommender_nudge.mark_done(tmp_path)
    assert not recommender_nudge.should_nudge(tmp_path)


def test_should_nudge_again_when_manifest_changes(tmp_path):
    _make_project(tmp_path)
    recommender_nudge.mark_done(tmp_path)
    time.sleep(1)
    (tmp_path / "package.json").write_text("{}", encoding="utf-8")
    assert recommender_nudge.should_nudge(tmp_path)


def test_main_emits_nudge_for_fresh_project(tmp_path, monkeypatch):
    _make_project(tmp_path)
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps({"cwd": str(tmp_path)})))
    captured = io.StringIO()
    monkeypatch.setattr("sys.stdout", captured)
    assert recommender_nudge.main() == 0
    out = captured.getvalue()
    assert "recommender-nudge" in out
    assert (tmp_path / ".claude" / ".recommender-nudged").exists()


def test_main_silent_for_non_project(tmp_path, monkeypatch):
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps({"cwd": str(tmp_path)})))
    captured = io.StringIO()
    monkeypatch.setattr("sys.stdout", captured)
    assert recommender_nudge.main() == 0
    assert captured.getvalue() == ""


def test_main_survives_garbage_stdin(monkeypatch):
    monkeypatch.setattr("sys.stdin", io.StringIO("not json"))
    assert recommender_nudge.main() == 0
