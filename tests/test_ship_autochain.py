"""Guard test for the `/ship` build-auto-chaining skill (Conductor v4).

Spec: specs/011-ship-autochain/spec.md  ·  Plan: specs/011-ship-autochain/plan.md

Written FIRST (TDD). Pure filesystem reads — no network/model. Guards that the SKILL.md drives the
existing kit skills in order, carries the multi-exit STOP rule and the anti-cheating guardrails, the
never-push/merge/deploy wall, the no-plan refusal, that /start routes in, and that it is registered.
"""
from pathlib import Path

from _kitpaths import skills_dir

ROOT = Path(__file__).resolve().parent.parent
SKILL = skills_dir(ROOT) / "ship" / "SKILL.md"
LOOP = skills_dir(ROOT) / "ship" / "references" / "bug-fix-loop.md"
START = skills_dir(ROOT) / "start" / "SKILL.md"


def _skill() -> str:
    return SKILL.read_text(encoding="utf-8").lower()


def _loop() -> str:
    return LOOP.read_text(encoding="utf-8").lower()


# ---------- exists + well-formed ----------

def test_T1_skill_exists_with_frontmatter():
    assert SKILL.exists(), "ship/SKILL.md missing"
    text = SKILL.read_text(encoding="utf-8")
    assert "name: ship" in text, "frontmatter missing 'name: ship'"
    assert "description:" in text, "frontmatter missing description"


# ---------- drives existing skills, in order, not a new engine ----------

def test_T2_drives_existing_skills():
    t = _skill()
    for needle in ("superpowers", "verify", "systematic-debugging", "security-review", "git-safety"):
        assert needle in t, f"/ship must drive existing skill: {needle}"
    assert "drive" in t or "route" in t, "must state it drives/routes, not reimplements"


def test_T3_stage_order_build_then_verify_then_fix_then_security():
    t = _skill()
    i_build = t.find("build")
    i_verify = t.find("verify")
    i_sec = t.find("security-review")
    assert 0 <= i_build < i_verify < i_sec, "stages must run build → verify → … → security in order"


# ---------- the bug-fix loop: STOP rule + feedback ----------

def test_T4_multi_exit_stop_rule():
    t = _skill() + _loop()
    assert "3" in t and "attempt" in t, "STOP needs a 3-attempt cost backstop"
    assert "no progress" in t or "no-progress" in t, "STOP needs a no-progress exit"
    assert "stop" in t and ("hand back" in t or "escalate" in t or "hands" in t), \
        "must stop and hand back / escalate"
    # the canonical four STOP exits must ALL appear in the SKILL.md itself (guard against drift):
    s = _skill()
    for exit_ in ("attempt", "no-progress", "cheat", "budget"):
        assert exit_ in s, f"SKILL.md STOP list missing the '{exit_}' exit"


def test_T5_one_test_per_pass_with_real_output():
    t = _loop()
    assert "one" in t and "per pass" in t, "loop must fix one failing test per pass"
    assert "output" in t or "feedback" in t, "loop must feed the real failing-test output back"


def test_T6_independent_green_check():
    t = _skill() + _loop()
    assert "independent" in t or "full suite" in t or "full test suite" in t, \
        "green must be confirmed by an independent full-suite run, not self-report"


# ---------- anti-cheating guardrails ----------

def test_T7_tests_are_read_only():
    t = _skill() + _loop()
    assert "read-only" in t or "read only" in t, "test files must be read-only in the loop"


def test_T8_diff_check_rejects_cheating():
    t = _loop()
    assert "diff" in t, "must diff-check every fix"
    for needle in ("skip", "hardcode", "weaken"):
        assert needle in t, f"anti-cheat diff-check must catch: {needle}"
    assert "reject" in t or "escalate" in t, "a detected cheat must be rejected/escalated, not a pass"


# ---------- walls + gates ----------

def test_T9_never_push_merge_deploy():
    t = _skill()
    assert "never" in t and ("push" in t and "merge" in t and "deploy" in t), \
        "missing the never push/merge/deploy wall"


def test_T10_refuses_to_build_without_a_plan():
    t = _skill()
    assert "plan" in t and ("refuse" in t or "without a plan" in t or "no plan" in t), \
        "/ship must refuse to build without an approved plan"


def test_T11_checkpoints_and_bypass():
    t = _skill()
    assert "checkpoint" in t, "missing per-stage checkpoints"
    assert "just run it" in t or "bypass" in t, "missing the opt-in bypass"


# ---------- grounding + /start + registration ----------

def test_T12_grounded_in_research():
    t = _skill() + _loop()
    assert "self-healing-loop-safety" in t, "must reference the cited research note"


def test_T13_start_routes_into_ship():
    s = START.read_text(encoding="utf-8").lower()
    assert "/ship" in s or "`ship`" in s, "/start build stages must route into /ship"


def test_T14_registered_everywhere():
    assert "ship" in (ROOT / "SKILL-MAP.md").read_text(encoding="utf-8").lower(), "not in SKILL-MAP.md"
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8").lower()
    assert "/ship" in agents or "ship —" in agents or "`ship`" in agents, "AGENTS.md does not register /ship"
    assert "ship" in (ROOT / "README.md").read_text(encoding="utf-8").lower(), "README missing /ship"
