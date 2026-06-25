"""Guard test for the live-monitoring sampler (Conductor v5).

Spec: specs/014-live-monitoring/spec.md  ·  Plan: specs/014-live-monitoring/plan.md

Written FIRST (TDD). Mocked judge transport — no live API/app. Guards that monitor_sample grades a
batch of live outputs for drift (reusing agent-eval), reports OK vs DRIFT, handles code grading, fails
loud on a judge error, and handles an empty batch.
"""
import importlib.util
import io
import json
from pathlib import Path

from _kitpaths import scripts_dir

ROOT = Path(__file__).resolve().parent.parent
MON = scripts_dir(ROOT) / "monitor_sample.py"

_spec = importlib.util.spec_from_file_location("monitor_sample", MON)
monitor_sample = importlib.util.module_from_spec(_spec)
if _spec.loader and MON.exists():
    _spec.loader.exec_module(monitor_sample)

_CONFIG = {"rubric": "Answer is correct and helpful.", "pass_bar": 80, "case_score_threshold": 4}


def _judge(score):
    return lambda system, user: f"<score>{score}</score><reason>mock</reason>"


def test_T1_script_exists():
    assert MON.exists(), "scripts/monitor_sample.py missing"


def test_T2_good_outputs_report_ok(tmp_path):
    records = [
        {"id": "a", "input": "2+2?", "output": "4"},
        {"id": "b", "input": "capital of France?", "output": "Paris"},
    ]
    verdict = monitor_sample.grade_records(records, _CONFIG, _judge(5))
    assert verdict["overall_passed"] is True
    assert verdict["drift"] is False
    assert verdict["pct_passed"] == 100


def test_T3_low_scores_report_drift(tmp_path):
    records = [
        {"id": "a", "input": "2+2?", "output": "banana"},
        {"id": "b", "input": "capital?", "output": "nope"},
    ]
    verdict = monitor_sample.grade_records(records, _CONFIG, _judge(1))
    assert verdict["drift"] is True
    assert verdict["overall_passed"] is False
    assert set(verdict["failing"]) == {"a", "b"}


def test_T4_code_grading_works(tmp_path):
    def _boom(system, user):
        raise AssertionError("judge must NOT be called for code-graded records")

    records = [{"id": "c", "input": "greet", "output": "hello world", "grading": "code",
                "expected": "hello", "match": "contains"}]
    verdict = monitor_sample.grade_records(records, _CONFIG, _boom)
    assert verdict["overall_passed"] is True and verdict["drift"] is False


def test_T5_judge_error_fails_loud(tmp_path, monkeypatch):
    # a judge that returns no parseable <score> must make the run fail loud (exit 2), never a false OK
    records = [{"id": "a", "input": "x", "output": "y"}]
    (tmp_path / "records.json").write_text(json.dumps(records), encoding="utf-8")
    (tmp_path / "config.json").write_text(json.dumps(_CONFIG), encoding="utf-8")
    monkeypatch.setattr(monitor_sample, "_default_transport", lambda cfg: (lambda s, u: "garbage no score"))
    cap = io.StringIO()
    monkeypatch.setattr("sys.stdout", cap)
    code = monitor_sample.main([str(tmp_path / "records.json"), str(tmp_path / "config.json")])
    assert code == 2, "a judge/grading error must exit 2 (fail loud), never a false all-good"


def test_T6_empty_batch_handled(tmp_path):
    verdict = monitor_sample.grade_records([], _CONFIG, _judge(5))
    assert verdict["total"] == 0
    assert verdict["drift"] is False  # nothing to be wrong yet


def test_T7_main_reports_verdict(tmp_path, monkeypatch):
    records = [{"id": "a", "input": "2+2?", "output": "4", "grading": "code", "expected": "4"}]
    (tmp_path / "r.json").write_text(json.dumps(records), encoding="utf-8")
    (tmp_path / "c.json").write_text(json.dumps(_CONFIG), encoding="utf-8")
    cap = io.StringIO()
    monkeypatch.setattr("sys.stdout", cap)
    code = monitor_sample.main([str(tmp_path / "r.json"), str(tmp_path / "c.json")])
    assert code == 0
    out = cap.getvalue().lower()
    assert "drift" in out or "ok" in out, "main must print a plain verdict"
