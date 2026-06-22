"""Layout-aware paths for the kit's guard tests.

The dev repo (Perfecting-Coding-Spec-Kit) keeps skills in `.claude/skills/` and helper
scripts in `scripts/`. The published plugin repo (vibe-coding-kit) keeps both under
`plugins/<plugin>/`. These resolvers prefer the dev-repo layout and fall back to the plugin
layout, so the same guard tests run green in BOTH repos instead of erroring on missing folders.
"""

from __future__ import annotations

from pathlib import Path


def _resolve(root: Path, root_rel: str, leaf: str) -> Path:
    primary = root / root_rel
    if primary.is_dir():
        return primary
    for candidate in sorted(root.glob(f"plugins/*/{leaf}")):
        if candidate.is_dir():
            return candidate
    return primary  # dev-repo path; keeps failure messages sensible if neither exists


def skills_dir(root: Path) -> Path:
    """Directory holding skill folders (`.claude/skills` or `plugins/<plugin>/skills`)."""
    return _resolve(root, ".claude/skills", "skills")


def scripts_dir(root: Path) -> Path:
    """Directory holding helper scripts (`scripts` or `plugins/<plugin>/scripts`)."""
    return _resolve(root, "scripts", "scripts")
