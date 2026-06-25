"""Guard test for the `/stack` stack-decider skill (Conductor v3).

Spec: specs/010-stack-decider/spec.md  ·  Plan: specs/010-stack-decider/plan.md

Written FIRST (TDD). Pure filesystem reads — no network/model. Guards that the SKILL.md states every
required behavior (8 lanes, tiered cost-labelled options, owner override, the Streamlit/Vercel
correction, recommend-only/no-deploy wall, AI-inside reuse), is grounded in the research, that /start
routes into it, and that it is registered everywhere.
"""
from pathlib import Path

from _kitpaths import skills_dir

ROOT = Path(__file__).resolve().parent.parent
SKILL = skills_dir(ROOT) / "stack" / "SKILL.md"
TABLE = skills_dir(ROOT) / "stack" / "references" / "stack-decision-table.md"
START = skills_dir(ROOT) / "start" / "SKILL.md"


def _skill() -> str:
    return SKILL.read_text(encoding="utf-8").lower()


def _table() -> str:
    return TABLE.read_text(encoding="utf-8").lower()


# ---------- the skill exists + is well-formed ----------

def test_T1_skill_exists_with_frontmatter():
    assert SKILL.exists(), "stack/SKILL.md missing"
    text = SKILL.read_text(encoding="utf-8")
    assert "name: stack" in text, "frontmatter missing 'name: stack'"
    assert "description:" in text, "frontmatter missing description"


def test_T2_recommend_only_no_deploy_wall():
    t = _skill()
    assert "recommend" in t, "must state it is recommendation-only"
    assert "scaffold" in t, "must say it does NOT scaffold (deferred to v7)"
    assert "never" in t and ("push" in t and "merge" in t and "deploy" in t), \
        "missing the never push/merge/deploy wall"


# ---------- the 7 common rows + the 8th escape-hatch lane ----------

def test_T3_covers_seven_project_types():
    t = _skill() + _table()
    for needle in ("dashboard", "automation", "web app", "api", "marketing", "mobile", "ai"):
        assert needle in t, f"missing project-type coverage: {needle}"


def test_T4_escape_hatch_lane():
    t = _skill()
    assert "escape" in t or "doesn't fit" in t or "does not fit" in t, "missing the escape-hatch lane"
    for needle in ("research-scout", "discover", "agent-architect"):
        assert needle in t, f"escape hatch must route to: {needle}"


# ---------- tiered, cost-labelled options + ask-priority-once ----------

def test_T5_asks_priority_once_and_leads_best_fit():
    t = _skill()
    assert "priority" in t, "must ask the owner's priority"
    for needle in ("budget", "scale", "simplic", "speed"):
        assert needle in t, f"priority axis missing: {needle}"
    assert "best-fit" in t or "best fit" in t or "lead" in t, "must lead with the best-fit pick"


def test_T6_tiered_options_with_cost():
    t = _skill() + _table()
    assert "tier" in t or "pay-for-better" in t or "pay for better" in t, "missing tiered options"
    assert "cost" in t or "$" in t or "free" in t, "tiers must be labelled with cost"


# ---------- owner override ----------

def test_T7_honors_owner_override():
    t = _skill()
    assert "override" in t or "prefer" in t, "must handle an owner's tool preference/override"
    assert "never silently" in t or "not silently" in t or "defer" in t, \
        "must never silently override the owner (warn-but-defer)"


# ---------- the key research correction ----------

def test_T8_streamlit_not_on_vercel_correction():
    t = _skill() + _table()
    assert "streamlit" in t and "vercel" in t, "must mention Streamlit + Vercel"
    assert "community cloud" in t, "Streamlit apps must route to Streamlit Community Cloud, not Vercel"


# ---------- reuse + grounding ----------

def test_T9_reuses_ai_inside_check_and_research():
    t = _skill()
    assert "ai-inside" in t or "ai inside" in t, "must reuse idea-to-app's AI-inside check"
    assert "research/stack-by-project-type" in t, "must reference the cited research note"


# ---------- /start routes in + registration ----------

def test_T10_start_routes_into_stack():
    s = START.read_text(encoding="utf-8").lower()
    assert "/stack" in s or "`stack`" in s, "/start stage 4 must route into /stack"


def test_T11_registered_everywhere():
    assert "stack" in (ROOT / "SKILL-MAP.md").read_text(encoding="utf-8").lower(), "not in SKILL-MAP.md"
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8").lower()
    assert "/stack" in agents or "stack-decider" in agents, "AGENTS.md does not register /stack"
    assert "stack" in (ROOT / "README.md").read_text(encoding="utf-8").lower(), "README missing /stack"
