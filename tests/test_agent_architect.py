"""Guard test for the Agent-Architect skill.

Spec: specs/003-agent-architect/spec.md  ·  Plan: specs/003-agent-architect/plan.md

Written FIRST (TDD): every assertion fails before the skill + registrations exist. Pure filesystem
string-reads. Proves STRUCTURE + WIRING + REGISTRATION — a skill's output QUALITY is eye-checked at
the verify step (documented plan limitation), not here.
"""

from pathlib import Path

from _kitpaths import skills_dir

ROOT = Path(__file__).resolve().parent.parent
SKILL = skills_dir(ROOT) / "agent-architect" / "SKILL.md"
ROUTINE = skills_dir(ROOT) / "agent-architect" / "references" / "decision-routine.md"


def _skill_text() -> str:
    return SKILL.read_text(encoding="utf-8").lower()


def test_T1_skill_exists_with_frontmatter():
    """FR-001 / FR-008: SKILL.md exists with name + non-empty description."""
    assert SKILL.exists(), "agent-architect/SKILL.md missing"
    text = SKILL.read_text(encoding="utf-8")
    assert "name: agent-architect" in text, "frontmatter missing 'name: agent-architect'"
    # description: followed by something on the same line or the next non-empty line.
    assert "description:" in text, "frontmatter missing 'description:'"


def test_T2_skill_states_the_non_negotiable_rules():
    """FR-002/004/005/006/007: the rules that define correct behavior are written into the routine."""
    t = _skill_text()
    assert "decline" in t and ("no ai" in t or "no llm" in t), "missing decline-if-no-AI rule"
    assert "haiku" in t, "missing cheap/Haiku model-routing rule"
    assert ("owner decides" in t or "you decide" in t), "managed-vs-API must leave the choice to owner"
    assert "managed agent" in t and "messages api" in t, "missing managed-vs-API suggestion"
    assert "grill" in t and "by default" in t, "missing grill-by-default rule"
    assert "scaffold" in t and "defer" in t, "missing scaffolding-deferred reminder"


def test_T3_skill_references_the_12_factor_checklist():
    """FR-003: the routine draws the 13 factors from the existing checklist doc."""
    assert "ai-feature-checklist.md" in _skill_text(), "SKILL.md does not reference ai-feature-checklist.md"


def test_T4_worked_golden_example_exists():
    """Plan mitigation: a concrete worked example so the output shape is unambiguous."""
    assert ROUTINE.exists(), "references/decision-routine.md missing"
    t = ROUTINE.read_text(encoding="utf-8").lower()
    assert "example" in t and "orchestrator" in t, "no worked golden example in decision-routine.md"


def test_T5_registered_in_agents_md():
    """FR-008 / SC-006: portability — registered in AGENTS.md."""
    assert "agent-architect" in (ROOT / "AGENTS.md").read_text(encoding="utf-8"), \
        "AGENTS.md does not register agent-architect"


def test_T6_registered_in_skill_map():
    """FR-008 / SC-006: portability — registered in SKILL-MAP.md."""
    assert "agent-architect" in (ROOT / "SKILL-MAP.md").read_text(encoding="utf-8"), \
        "SKILL-MAP.md does not register agent-architect"


def test_T7_wired_into_idea_to_app_gate():
    """FR-009: invoked from idea-to-app's AI-inside gate."""
    gate = (skills_dir(ROOT) / "idea-to-app" / "SKILL.md").read_text(encoding="utf-8")
    assert "agent-architect" in gate, "idea-to-app/SKILL.md does not reference agent-architect"
