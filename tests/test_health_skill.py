"""Guard test for the /health project health-score skill.

Pure filesystem string-reads. Proves STRUCTURE + the non-negotiable RULES + REGISTRATION
across the portability maps — so the skill cannot silently rot or fall out of the maps.
A skill's output QUALITY is eye-checked at the verify step, not here.
"""

from pathlib import Path

from _kitpaths import skills_dir

ROOT = Path(__file__).resolve().parent.parent
SKILL = skills_dir(ROOT) / "health" / "SKILL.md"


def _skill_text() -> str:
    return SKILL.read_text(encoding="utf-8").lower()


def test_T1_skill_exists_with_frontmatter():
    """SKILL.md exists with name + non-empty description."""
    assert SKILL.exists(), "health/SKILL.md missing"
    text = SKILL.read_text(encoding="utf-8")
    assert "name: health" in text, "frontmatter missing 'name: health'"
    assert "description:" in text, "frontmatter missing 'description:'"


def test_T2_states_the_scoring_contract():
    """The score is 0-100, starts at 100, and uses a deduction ledger."""
    t = _skill_text()
    assert "100" in t, "missing the 100-point scale"
    assert "ledger" in t, "missing the deduction ledger"
    assert "fix this first" in t, "missing the single 'fix this first' handoff"


def test_T3_covers_all_twelve_checks():
    """All 12 health dimensions are present so the score can't quietly shrink."""
    t = _skill_text()
    checks = [
        "plan before code",
        "tests exist",
        "tests mean something",
        "main is green",
        "secrets are safe",
        "inputs & data",
        "simple & surgical",
        "docs match reality",
        "ai-portable",
        "git is reversible",
        "ci gate",
        "risks are written down",
    ]
    missing = [c for c in checks if c not in t]
    assert not missing, f"health checks missing from SKILL.md: {missing}"


def test_T4_is_diagnostic_only():
    """Like /guide: it scores and hands off, it never edits or builds."""
    t = _skill_text()
    assert "diagnostic only" in t, "missing the diagnostic-only guarantee"
    assert "never" in t and ("edit" in t or "fix" in t), "missing the never-edits rule"


def test_T5_registered_in_agents_md():
    """Portability — registered in AGENTS.md."""
    assert "health" in (ROOT / "AGENTS.md").read_text(encoding="utf-8").lower(), \
        "AGENTS.md does not register health"


def test_T6_registered_in_skill_map():
    """Portability — registered in SKILL-MAP.md."""
    assert "/health" in (ROOT / "SKILL-MAP.md").read_text(encoding="utf-8").lower(), \
        "SKILL-MAP.md does not register /health"


def test_T7_routed_from_guide_skill():
    """The guide router knows to send users to /health."""
    guide = (skills_dir(ROOT) / "guide" / "SKILL.md").read_text(encoding="utf-8").lower()
    assert "/health" in guide, "guide/SKILL.md does not route to /health"
