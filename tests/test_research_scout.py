"""Guard test for the /research-scout skill.

Spec: specs/008-research-scout/spec.md  ·  Plan: specs/008-research-scout/plan.md

Written FIRST (TDD): every assertion fails before the skill + registrations exist. Pure filesystem
string-reads — no network, no model. research-scout is a PROCEDURE skill (like /discover), so this
guards that the SKILL.md states every non-negotiable rule from the spec + is wired/registered, so
the FRs can't silently rot. Output QUALITY is eye-checked at the verify step, not here.
"""

from pathlib import Path

from _kitpaths import skills_dir

ROOT = Path(__file__).resolve().parent.parent
SKILL = skills_dir(ROOT) / "research-scout" / "SKILL.md"
SOURCE_QUALITY = skills_dir(ROOT) / "research-scout" / "references" / "source-quality.md"
NOTE_TEMPLATE = skills_dir(ROOT) / "research-scout" / "references" / "note-template.md"


def _skill_text() -> str:
    return SKILL.read_text(encoding="utf-8").lower()


def test_T1_skill_exists_with_frontmatter():
    """FR-001/FR-012: SKILL.md exists with name + description."""
    assert SKILL.exists(), "research-scout/SKILL.md missing"
    text = SKILL.read_text(encoding="utf-8")
    assert "name: research-scout" in text, "frontmatter missing 'name: research-scout'"
    assert "description:" in text, "frontmatter missing 'description:'"


def test_T2_never_fabricate_and_cite_everything():
    """FR-002 / SC-001/003: no fabrication; cite every claim; say-so-and-stop if unavailable."""
    t = _skill_text()
    assert "never fabricate" in t or "no fabrication" in t or "never invent" in t, \
        "missing the never-fabricate rule"
    assert "cite" in t and "source" in t, "missing cite-every-claim rule"


def test_T3_consent_gate_before_autorun():
    """FR-004 / SC-004: must ASK before auto-running from grill-me/plan/conductor."""
    t = _skill_text()
    assert "ask" in t and ("consent" in t or "before" in t), "missing consent gate"
    assert "decline" in t or "say no" in t or "no penalty" in t or "continue" in t, \
        "missing the decline-and-continue path"


def test_T4_depth_tiers_and_hard_ceiling():
    """FR-005/006: quick default + tiers + a hard runaway ceiling + effort heads-up."""
    t = _skill_text()
    assert "quick" in t and "deep" in t, "missing depth tiers (quick/standard/deep)"
    assert "default" in t, "quick must be the default"
    assert "ceiling" in t or "cap" in t or "limit" in t, "missing hard ceiling/cap (runaway guard)"


def test_T5_advise_cost_benefit():
    """FR-007 / SC-005: advises when deeper is worth it vs when quick is plenty."""
    t = _skill_text()
    assert "advise" in t or "recommend" in t, "missing the advise behavior"
    assert "worth" in t or "overspend" in t or "deeper" in t, "missing cost/benefit guidance"


def test_T6_method_decompose_to_stop():
    """FR-010: decompose -> search -> triage -> synthesize -> citation pass -> STOP."""
    t = _skill_text()
    for needle in ("decompose", "synthes", "citation pass", "stop"):
        assert needle in t, f"method step missing: {needle}"


def test_T7_source_quality_and_injection_safe():
    """FR-008/009: source-quality ladder + treat fetched text as data, not instructions."""
    sq = SOURCE_QUALITY
    assert sq.exists(), "references/source-quality.md missing"
    t = sq.read_text(encoding="utf-8").lower()
    assert "reddit" in t or "forum" in t, "source-quality must address Reddit/forum anecdote"
    assert "anecdote" in t or "cross-check" in t, "Reddit/forums must be treated as anecdote/cross-checked"
    assert "data" in t and "instruction" in t, "missing the data-not-instructions (injection-safe) rule"


def test_T8_note_template_exists():
    """FR-001: the research/<topic>.md cited-note template exists."""
    assert NOTE_TEMPLATE.exists(), "references/note-template.md missing"
    t = NOTE_TEMPLATE.read_text(encoding="utf-8").lower()
    assert "source" in t and "summary" in t, "note-template missing source/summary structure"


def test_T9_third_lane_not_duplicate():
    """Spec context: positioned as a third lane distinct from /discover + GitMCP."""
    t = _skill_text()
    assert "discover" in t, "SKILL.md should distinguish itself from /discover"


def test_T10_registered_everywhere():
    """FR-012 / SC-006: portability — registered in AGENTS.md, SKILL-MAP.md, README.md."""
    assert "research-scout" in (ROOT / "AGENTS.md").read_text(encoding="utf-8"), "not in AGENTS.md"
    assert "research-scout" in (ROOT / "SKILL-MAP.md").read_text(encoding="utf-8"), "not in SKILL-MAP.md"
    assert "research-scout" in (ROOT / "README.md").read_text(encoding="utf-8"), "not in README.md"


def test_T11_wired_into_grill_me():
    """FR-003: grill-me can call it (offer-with-consent before recommending)."""
    grill = (skills_dir(ROOT) / "grill-me" / "SKILL.md").read_text(encoding="utf-8").lower()
    assert "research-scout" in grill, "grill-me/SKILL.md does not reference research-scout"
