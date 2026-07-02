# tests/test_production_readiness.py
"""Spec 016 Phase 3 guard: the six production-readiness gaps the 2026-07-02 audit found
(dependency vuln scanning, DB migration safety, error monitoring, data backup/restore,
load smoke, accessibility) must have a canonical doc, CI wiring where applicable, and
kit registration — so they can't silently rot back out of the kit."""
from pathlib import Path

from _kitpaths import skills_dir

ROOT = Path(__file__).resolve().parent.parent


def _read(rel):
    p = ROOT / rel
    assert p.is_file(), f"{rel} is missing"
    return p.read_text(encoding="utf-8")


def test_canonical_doc_exists_with_all_six_sections():
    doc = _read("docs/production-readiness.md").lower()
    for topic in (
        "dependency",  # vuln scanning
        "migration",  # DB schema safety
        "error monitoring",  # Sentry-style, beyond AI drift
        "backup",  # data backup/restore
        "load",  # load smoke
        "accessibility",  # a11y/legal basics
    ):
        assert topic in doc, f"production-readiness.md lost its '{topic}' section"


def test_migration_safety_names_the_additive_first_rule():
    doc = _read("docs/production-readiness.md").lower()
    assert "additive" in doc, "migration section must teach additive-first schema changes"
    assert "backup before" in doc or "backup first" in doc


def test_ci_has_blocking_dependency_audit():
    ci = _read(".github/workflows/ci.yml")
    assert "pip-audit" in ci, "CI lost the Python dependency audit"
    assert "npm audit" in ci, "CI lost the Node dependency audit"
    job = ci[ci.index("deps-audit") :]
    assert "continue-on-error: true" not in job.split("jobs:")[0], (
        "dependency audit must block, not just report"
    )


def test_dependabot_config_exists():
    dep = _read(".github/dependabot.yml")
    for eco in ("pip", "npm", "github-actions"):
        assert eco in dep, f"dependabot.yml lost the {eco} ecosystem"


def test_registered_in_kit_maps():
    assert "production-readiness" in _read("AGENTS.md").lower()
    assert "production-readiness" in _read("SKILL-MAP.md").lower()
    assert "production-readiness.md" in _read("README.md")


def test_git_safety_points_at_doc_on_deploy():
    skill_path = skills_dir(ROOT) / "git-safety" / "SKILL.md"
    assert skill_path.is_file(), "git-safety SKILL.md is missing"
    skill = skill_path.read_text(encoding="utf-8")
    assert "production-readiness.md" in skill, (
        "git-safety must walk the production-readiness doc at deploy time"
    )
