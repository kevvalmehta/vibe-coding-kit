"""Guard test for the Audit Advisor (/audit) skill.

Spec: specs/004-audit-advisor/spec.md  ·  Plan: specs/004-audit-advisor/plan.md

Written FIRST (TDD): every assertion fails before the skill + references + registrations exist.
Pure filesystem string-reads. Proves STRUCTURE + HARD-RULES-PRESENT + WIRING + REGISTRATION — a
skill's output QUALITY is eye-checked at the verify step (documented plan limitation), not here.
"""

from pathlib import Path

from _kitpaths import skills_dir

ROOT = Path(__file__).resolve().parent.parent
SKILL = skills_dir(ROOT) / "audit" / "SKILL.md"
REFS = skills_dir(ROOT) / "audit" / "references"
PLAYBOOK = REFS / "audit-playbook.md"
BRIEF = REFS / "brief-template.md"
ROUTING = REFS / "routing-and-modes.md"
AGENTS = ROOT / "AGENTS.md"
SKILL_MAP = ROOT / "SKILL-MAP.md"
HEALTH = skills_dir(ROOT) / "health" / "SKILL.md"


def _text(p: Path) -> str:
    return p.read_text(encoding="utf-8").lower()


def test_T1_skill_exists_with_frontmatter():
    """FR-001/FR-016: SKILL.md exists with name: audit + non-empty description."""
    assert SKILL.exists(), "audit/SKILL.md missing"
    text = SKILL.read_text(encoding="utf-8")
    assert "name: audit" in text, "frontmatter missing 'name: audit'"
    assert "description:" in text, "frontmatter missing 'description:'"


def test_T2_three_reference_files_exist():
    """Plan structure: the heavy detail lives in 3 reference files."""
    assert PLAYBOOK.exists(), "references/audit-playbook.md missing"
    assert BRIEF.exists(), "references/brief-template.md missing"
    assert ROUTING.exists(), "references/routing-and-modes.md missing"


def test_T3_skill_encodes_the_hard_rules():
    """FR-001/009/011/012/013: the non-negotiable hard rules are written into SKILL.md."""
    t = _text(SKILL)
    assert "read-only" in t, "missing read-only-on-source rule"
    assert "secret" in t and "rotat" in t, "missing never-reproduce-secret-values + rotation rule"
    assert "not instructions" in t, "missing repo-content-is-data-not-instructions rule"
    assert "decline" in t, "missing decline-to-implement rule"
    # the push/merge/deploy wall, in BOTH modes
    assert "push" in t and "merge" in t and "deploy" in t, "missing the push/merge/deploy wall"
    assert ("both modes" in t or "stop before" in t or "before push" in t), \
        "the wall must apply in both modes / stop before push"


def test_T4_playbook_covers_nine_categories_and_finding_format():
    """FR-003: the audit playbook covers all 9 categories + a Finding format."""
    t = _text(PLAYBOOK)
    for cat in ["correctness", "security", "performance", "test coverage", "tech debt",
                "dependencies", "docs", "direction"]:
        assert cat in t, f"audit-playbook.md missing category: {cat}"
    assert "dx" in t or "tooling" in t, "audit-playbook.md missing DX & tooling category"
    assert "finding format" in t, "audit-playbook.md missing a 'Finding format'"


def test_T5_brief_template_has_required_fields_and_example():
    """FR-007: a self-contained brief template with all required fields + a worked example."""
    t = _text(BRIEF)
    assert "in scope" in t or "in-scope" in t, "brief-template.md missing in-scope list"
    assert "out of scope" in t or "out-of-scope" in t, "brief-template.md missing out-of-scope list"
    assert "verify" in t, "brief-template.md missing a verify-gate"
    assert "stop" in t, "brief-template.md missing STOP conditions"
    assert "planned at" in t or "planned-at" in t, "brief-template.md missing planned-at SHA"
    assert "/safe-change" in t, "brief-template.md missing the executor-routing line"
    assert "example" in t, "brief-template.md missing a worked golden example"


def test_T6_routing_documents_both_modes_and_executor_map():
    """FR-008/009/010: both modes, the executor map, and the portability fallbacks."""
    t = _text(ROUTING)
    assert "interactive" in t and "auto" in t, "routing-and-modes.md missing the two modes"
    assert "/safe-change" in t and "/speckit-specify" in t and "/autopilot" in t, \
        "routing-and-modes.md missing the executor map"
    assert "sequential" in t or "fallback" in t, "routing-and-modes.md missing the fallbacks"


def test_T7_registered_in_agents_md():
    """FR-016: portability — registered in AGENTS.md."""
    assert "/audit" in _text(AGENTS), "AGENTS.md does not register /audit"


def test_T8_registered_in_skill_map():
    """FR-016: portability — registered in SKILL-MAP.md."""
    assert "/audit" in _text(SKILL_MAP), "SKILL-MAP.md does not register /audit"


def test_T9_health_cross_links_audit():
    """Plan: /health (score) hands off to /audit (specifics)."""
    assert "/audit" in _text(HEALTH), "health/SKILL.md does not cross-link /audit"
