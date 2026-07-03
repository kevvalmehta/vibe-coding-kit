# tests/test_adopted_patterns.py
"""Guard for spec 018 (adopted patterns): the four adaptations must exist with their
load-bearing rules intact — /pathfinder's discipline (one ticket per session, fog kept
loose, routes to existing kit skills), git-safety's merge-conflict rescue, /ship's
two-axis review lens, and the domain-modeling named entry. If a future edit drops one
of these rules, the pattern silently degrades into what it was meant to prevent."""
from pathlib import Path

from _kitpaths import skills_dir

ROOT = Path(__file__).resolve().parent.parent


def read(path):
    return path.read_text(encoding="utf-8")


def test_pathfinder_skill_exists_with_hard_rules():
    text = read(skills_dir(ROOT) / "pathfinder" / "SKILL.md")
    low = text.lower()
    # the map lives in the project as local markdown, not on an issue tracker
    assert "pathfinder/map.md" in text
    assert "fog" in low
    # the two hard rules that make it work
    assert "one ticket" in low  # one ticket resolved per session
    assert "speckit-specify" in low  # exit hands off to the spec stage
    # ticket types route to EXISTING kit skills, not new machinery
    for target in ("research-scout", "prototype", "grill"):
        assert target in low


def test_pathfinder_fog_vs_ticket_test_present():
    low = read(skills_dir(ROOT) / "pathfinder" / "SKILL.md").lower()
    # the discriminator: sharp question now -> ticket; not yet phrasable -> fog
    assert "sharp" in low


def test_git_safety_has_merge_conflict_rescue():
    text = read(skills_dir(ROOT) / "git-safety" / "SKILL.md")
    low = text.lower()
    assert "conflict" in low
    assert "<<<<<<<" in text  # explains the actual markers the owner will see
    assert "merge --abort" in low  # the always-safe escape hatch
    assert "nothing is lost" in low or "nothing lost" in low


def test_ship_reviews_on_two_axes():
    low = read(skills_dir(ROOT) / "ship" / "SKILL.md").lower()
    assert "spec fidelity" in low
    assert "standards" in low
    # the point of the split: one axis must not mask the other
    assert "wrong thing" in low


def test_domain_modeling_registered_in_skill_map():
    low = read(ROOT / "SKILL-MAP.md").lower()
    assert "domain-modeling" in low
    assert "grill-with-docs" in low


def test_pathfinder_registered_everywhere():
    # Principle VI: not done until registered for other AI tools too
    for rel in ("SKILL-MAP.md", "AGENTS.md", "README.md"):
        assert "pathfinder" in read(ROOT / rel).lower(), f"pathfinder missing from {rel}"
