"""Guard test for Autopilot v2 polish (gate modes, mid-flight, pre-PR ordering).

Locks the v2 invariants into the skill's markdown so they can't silently regress. Pure
read-only filesystem string checks (same pattern as the other guard tests). The deterministic
helper (scripts/autopilot_state.py) is covered separately by tests/test_autopilot_state.py and is
intentionally NOT changed by v2 — STEP_ORDER stays fixed.
"""

from pathlib import Path

from _kitpaths import skills_dir

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = skills_dir(ROOT) / "autopilot"
SKILL = SKILL_DIR / "SKILL.md"
GATES = SKILL_DIR / "references" / "gates.md"
PREPR = SKILL_DIR / "references" / "prepr-checks.md"


def _text(p: Path) -> str:
    return p.read_text(encoding="utf-8").lower()


def test_relaxed_gate_modes_documented():
    """(a) Three gate modes exist and default is stop-at-every-step."""
    t = _text(GATES)
    assert "big-3" in t or "big-three" in t, "big-3 relaxed mode not documented"
    assert "auto" in t, "auto mode not documented"
    assert "stop-at-every-step" in t, "stop-at-every-step mode not named"
    assert "default" in t, "no default gate mode stated"


def test_relaxed_gate_is_opt_in_default_preserved():
    """(a) Safety promise preserved: default is stop-at-every-step unless owner opts in."""
    t = _text(GATES)
    # The default must be the safe v1 behavior; relaxed modes are opt-in.
    assert "opt-in" in t or "only when" in t or "must ask" in t or "explicitly" in t, \
        "relaxed mode is not clearly opt-in"


def test_mid_flight_new_idea_handled():
    """(b) Starting a new idea while another feature is incomplete is handled."""
    t = _text(GATES)
    assert "mid-flight" in t or "incomplete" in t or "in progress" in t, \
        "no mid-flight / incomplete-active-feature handling"
    # It must offer a choice (finish vs park/start fresh), not silently resume.
    assert "finish" in t or "park" in t or "switch" in t, \
        "mid-flight handling does not offer finish-vs-switch choice"


def test_prepr_checks_handle_no_build_yet():
    """(d) pre-PR checks detect 'only planning artifacts changed' and don't fake-run on docs."""
    t = _text(PREPR)
    assert "no build" in t or "after the build" in t or "build yet" in t, \
        "pre-PR step does not handle the no-build-yet case"
    # It must look at what actually changed (the git diff) rather than verify nothing.
    assert "git diff" in t, "pre-PR step does not check the diff for whether real code changed"


def test_skill_points_to_gate_modes():
    """(a) SKILL.md references the gate-mode options (not only the v1 single mode)."""
    t = _text(SKILL)
    assert "gate mode" in t and "big-3" in t, \
        "SKILL.md does not surface the gate-mode options"
