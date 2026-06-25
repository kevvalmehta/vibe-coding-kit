#!/usr/bin/env python3
"""monitor_sample.py — Conductor v5: post-launch AI-output drift check.

Given a batch of logged live `(input, output)` records + a rubric/passing bar, grade them and report a
DRIFT verdict — REUSING agent-eval's tested `eval_runner` (grade_code / grade_model / score_set). The
judge `transport` is injectable so this is unit-testable with a mock (no live API/app needed).

Honest boundary: this grades a batch you hand it. Capturing live outputs to a log + running this on a
schedule needs a DEPLOYED app — that wiring is the switch-on recipe in the `/monitor` skill, not here.

Fails loud (exit 2) on any grading/judge error — never a false "all good" (Principle VII).

Spec: specs/014-live-monitoring/spec.md
"""
import importlib.util
import json
import sys
from pathlib import Path

_ER = None  # cached agent-eval eval_runner module


def _find_eval_runner():
    """Locate agent-eval's eval_runner.py in either repo layout (kit root or plugin)."""
    here = Path(__file__).resolve()
    patterns = (
        ".claude/skills/agent-eval/assets/eval_runner.py",
        "plugins/*/skills/agent-eval/assets/eval_runner.py",
    )
    for base in [here.parent, *here.parents]:
        for pat in patterns:
            matches = list(base.glob(pat))
            if matches:
                return matches[0]
    return None


def _eval_runner():
    """Import + cache agent-eval's eval_runner (raises a clear error if it can't be found)."""
    global _ER
    if _ER is None:
        path = _find_eval_runner()
        if path is None:
            raise RuntimeError(
                "Could not find agent-eval's eval_runner.py — /monitor reuses it. "
                "Make sure the agent-eval skill is present."
            )
        spec = importlib.util.spec_from_file_location("eval_runner", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _ER = mod
    return _ER


def _default_transport(config):
    """Return a lazy judge transport: it builds the real Anthropic client only on first use, so a
    purely code-graded batch never needs an API key."""
    state = {}

    def transport(system, user):  # pragma: no cover - real path needs the live API
        if "fn" not in state:
            state["fn"] = _eval_runner()._real_transport(config)
        return state["fn"](system, user)

    return transport


def grade_records(records, config, transport):
    """Grade a batch of logged records for drift, reusing eval_runner. Returns a verdict dict:
    {pct_passed, passed, total, overall_passed, critical_failures, drift, failing}.
    Raises (→ fail loud) if the judge returns no parseable score."""
    er = _eval_runner()
    if not records:
        return {"pct_passed": 0, "passed": 0, "total": 0, "overall_passed": True,
                "critical_failures": [], "drift": False, "failing": []}

    results = []
    for i, rec in enumerate(records):
        cid = rec.get("id", str(i))
        crit = bool(rec.get("critical"))
        if rec.get("grading") == "code" and "expected" in rec:
            passed = er.grade_code(rec["output"], rec["expected"], rec.get("match", "contains"))
        else:
            score, _reason = er.grade_model(rec["input"], rec["output"], rec, config, transport)
            passed = score >= config.get("case_score_threshold", 4)
        results.append({"id": cid, "passed": passed, "critical": crit})

    verdict = er.score_set(results, config)
    verdict["drift"] = not verdict["overall_passed"]
    verdict["failing"] = [r["id"] for r in results if not r["passed"]]
    return verdict


def _load_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception:
        return None


def main(argv=None):
    """CLI: monitor_sample.py <records.json> <config.json>. Exit 0 normally, 2 on a grading error."""
    argv = argv if argv is not None else sys.argv[1:]
    if len(argv) < 2:
        print("Usage: python monitor_sample.py <records.json> <config.json>")
        return 0

    records = _load_json(argv[0])
    config = _load_json(argv[1])
    if records is None or config is None:
        print("Could not read the records or config file (missing or invalid JSON).")
        return 0
    if not records:
        print("No outputs to check — nothing logged yet. (OK: nothing to be wrong.)")
        return 0

    transport = _default_transport(config)
    try:
        verdict = grade_records(records, config, transport)
    except Exception as exc:
        # fail loud — never report a false "all good"
        print(f"Monitoring FAILED LOUD (a grading/judge error occurred, not a pass): {exc}")
        return 2

    bar = config.get("pass_bar", 80)
    if verdict["drift"]:
        print(f"DRIFT DETECTED — {verdict['pct_passed']}% passed (bar {bar}%). "
              f"Failing: {', '.join(verdict['failing']) or '(critical case)'}")
        print("The live AI output has dropped below your quality bar — time to look.")
    else:
        print(f"OK — {verdict['pct_passed']}% passed (bar {bar}%). No drift; live output still meets the bar.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
