"""Guard test for the Inventory Coverage Gate.

Spec: specs/005-inventory-coverage-gate/spec.md

Written FIRST (TDD): these assertions FAIL before scripts/check_inventory.py exists.
Pure filesystem string-reads — no mocks, no network, no model calls. This test IS the CI gate:
the repo's existing pytest step turns RED if any skill / script / top-level doc is left out of
README.md, so the index can never silently rot.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# The checker lives in scripts/ (dev repo) or plugins/<plugin>/scripts/ (published plugin repo).
_SCRIPTS = ROOT / "scripts"
if not _SCRIPTS.is_dir():
    _candidates = sorted(ROOT.glob("plugins/*/scripts"))
    if _candidates:
        _SCRIPTS = _candidates[0]
sys.path.insert(0, str(_SCRIPTS))

import check_inventory  # noqa: E402


def test_FR001_find_missing_is_callable_and_returns_list():
    """FR-001: the checker exposes find_missing(root) -> list[str]."""
    result = check_inventory.find_missing(ROOT)
    assert isinstance(result, list)
    assert all(isinstance(x, str) for x in result)


def test_FR003_readme_documents_every_skill_script_and_top_level_doc():
    """FR-003 / SC-001 / SC-002: nothing in scope is missing from README.md."""
    missing = check_inventory.find_missing(ROOT)
    assert missing == [], "README.md is missing index entries:\n" + "\n".join(missing)


def test_SC001_a_fake_undocumented_skill_is_detected(tmp_path):
    """SC-001: an item not present in the README is reported as missing.

    Builds a tiny fake repo so the test proves the detector actually fires (a test that can't
    go red when the rule is violated would be worthless — see constitution Quality Gate 9).
    """
    (tmp_path / ".claude" / "skills" / "ghost-skill").mkdir(parents=True)
    (tmp_path / "scripts").mkdir()
    (tmp_path / "docs").mkdir()
    (tmp_path / "README.md").write_text("# Empty index\n", encoding="utf-8")

    missing = check_inventory.find_missing(tmp_path)
    assert any("ghost-skill" in m for m in missing), missing


def test_SC001_wildcard_token_covers_a_family(tmp_path):
    """SC-001 helper: a `prefix*` token in README covers every name starting with prefix."""
    for name in ("speckit-plan", "speckit-clarify"):
        (tmp_path / ".claude" / "skills" / name).mkdir(parents=True)
    (tmp_path / "scripts").mkdir()
    (tmp_path / "docs").mkdir()
    (tmp_path / "README.md").write_text("Documents the `speckit-*` family.\n", encoding="utf-8")

    assert check_inventory.find_missing(tmp_path) == []


def test_markdown_emphasis_is_not_a_wildcard(tmp_path):
    """Bold/italic like **plan** must NOT become a wildcard that marks unlisted names documented."""
    (tmp_path / ".claude" / "skills" / "planner").mkdir(parents=True)
    (tmp_path / "scripts").mkdir()
    (tmp_path / "docs").mkdir()
    (tmp_path / "README.md").write_text("We **plan** before we build.\n", encoding="utf-8")

    missing = check_inventory.find_missing(tmp_path)
    assert any("planner" in m for m in missing), missing


def test_repo_root_without_git_resolves_plugin_layout(tmp_path):
    """Without a .git anchor, _repo_root must still find the real root in the plugin layout."""
    (tmp_path / "plugins" / "p" / "skills" / "demo").mkdir(parents=True)
    scripts = tmp_path / "plugins" / "p" / "scripts"
    scripts.mkdir(parents=True)
    script = scripts / "check_inventory.py"
    script.write_text("# stub\n", encoding="utf-8")

    assert check_inventory._repo_root(script.resolve()) == tmp_path.resolve()
