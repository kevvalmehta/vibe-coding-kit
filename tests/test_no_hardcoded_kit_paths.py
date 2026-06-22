"""Guard: no test file may hardcode the kit's skills/scripts location.

The two repos store skills/scripts in different places — the dev repo uses `.claude/skills`
and `scripts/`; the published plugin repo uses `plugins/<plugin>/...`. A test that anchors those
folders on ROOT directly passes in one repo and crashes on collection in the other. This exact
hardcoding turned the public repo's CI RED (2026-06). Locate skills/scripts via the layout-aware
helpers in _kitpaths.py (`skills_dir` / `scripts_dir`) instead.

This test fails LOUD if a ROOT-anchored kit path comes back, so the bug can't quietly return.
Pure filesystem string-reads — no network, no model calls.
"""

import re
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent

# ROOT-anchored literals that should go through the _kitpaths helpers instead.
# Deliberately NOT matched: tmp_path fixtures (tmp_path / ...) and `.claude/settings.json`
# (a real dev-repo path, already guarded with a plugin-layout fallback in its test).
_BANNED = re.compile(
    r"""ROOT\s*/\s*["']scripts["']"""
    r"""|ROOT\s*/\s*["']\.claude["']\s*/\s*["']skills["']"""
)


def test_no_test_hardcodes_kit_paths():
    offenders = []
    for path in sorted(TESTS_DIR.glob("test_*.py")):
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if _BANNED.search(line):
                offenders.append(f"{path.name}:{lineno}: {line.strip()}")
    assert not offenders, (
        "Test files must locate skills/scripts via _kitpaths (skills_dir/scripts_dir), not a "
        "ROOT-anchored hardcoded path — that breaks the other repo's layout and reddens its CI:\n"
        + "\n".join(offenders)
    )
