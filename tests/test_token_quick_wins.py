"""Guard test for the Token Quick-Wins habits doc.

Spec: specs/002-token-quick-wins/spec.md
Plan: specs/002-token-quick-wins/plan.md  (chosen architecture = docs + this guard test)

Written FIRST (TDD): every assertion must FAIL before docs/token-quick-wins.md and the portability
registrations exist. Pure filesystem string-reads — no mocks, no network, no model calls. Each test
maps to a spec requirement (FR/SC) and exists so the habits doc can never silently rot.
"""

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
DOC = ROOT / "docs" / "token-quick-wins.md"

# Wins that are Claude-Code-specific and therefore REQUIRE a non-Claude fallback (FR-002 / SC-002).
CLAUDE_ONLY = ["/compact", "/recap", "caveman"]


def _doc_text() -> str:
    return DOC.read_text(encoding="utf-8")


def _win_sections() -> dict[int, str]:
    """Split the doc into {win_number: section_text} on '## Win N' headings."""
    text = _doc_text()
    sections: dict[int, str] = {}
    matches = list(re.finditer(r"(?im)^##\s*Win\s*([1-6])\b", text))
    for i, m in enumerate(matches):
        num = int(m.group(1))
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        sections[num] = text[start:end]
    return sections


def test_T1_all_six_wins_present_with_an_already_in_place_label():
    """FR-001 / SC-001: six wins documented; SC-005 graft: at least one labelled already-in-place."""
    sections = _win_sections()
    assert set(sections) == {1, 2, 3, 4, 5, 6}, f"expected wins 1-6, found {sorted(sections)}"
    assert "already-in-place" in _doc_text().lower(), "no win labelled 'already-in-place'"


def test_T2_each_claude_only_win_has_a_fallback():
    """FR-002 / SC-002: every Claude-only win carries a non-Claude fallback marker."""
    for token in CLAUDE_ONLY:
        # Find the win section containing this token, assert a fallback marker is in the same section.
        owning = [s for s in _win_sections().values() if token.lower() in s.lower()]
        assert owning, f"no win section mentions {token!r}"
        assert any("fallback" in s.lower() for s in owning), f"win for {token!r} has no fallback"


@pytest.mark.parametrize("fname", ["AGENTS.md", "SKILL-MAP.md", "HANDOFF.md"])
def test_T3_T4_T5_doc_registered_in_portability_files(fname):
    """FR-003 / SC-003: the doc is discoverable from every portability file."""
    text = (ROOT / fname).read_text(encoding="utf-8")
    # Match the doc filename, not the spec folder name (specs/002-token-quick-wins), so the
    # Autopilot state marker in HANDOFF.md can't satisfy this by accident.
    assert "token-quick-wins.md" in text, f"{fname} does not reference the habits doc"


def test_T6_ai_feature_checklist_cross_refs_prompt_caching():
    """FR-005: the AI-feature checklist points to the prompt-caching win."""
    text = (ROOT / "docs" / "ai-feature-checklist.md").read_text(encoding="utf-8")
    assert "token-quick-wins.md" in text, "ai-feature-checklist.md does not cross-ref the wins doc"


def test_T7_doc_embeds_no_workflow_change_imperative():
    """FR-006 / SC-004: habits doc LINKS to workflow steps, never embeds 'do X before /speckit-*'.

    Narrow guard (kept deliberately tight per the plan's known-risk note to avoid false positives):
    forbid the specific imperative phrasing 'before /speckit'.
    """
    text = _doc_text().lower()
    assert "before /speckit" not in text, "habits doc embeds a workflow-change imperative (T7)"
