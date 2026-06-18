"""Inventory Coverage Gate — fail when a skill / script / top-level doc is missing from README.md.

Spec: specs/005-inventory-coverage-gate/spec.md

Turns the README "completeness rule" from a trust-based note into an enforced one. The repo's
existing CI `pytest` step imports `find_missing` (see tests/test_inventory_coverage.py) and turns
RED if the index has rotted, so a new skill/script/doc cannot be added without listing it.

Run locally:  python scripts/check_inventory.py
Exit code 0 = index complete; 1 = items missing (printed).

Pure stdlib, no network, no model calls.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Names listed in README that we must NOT treat as undocumented items themselves
# (none today; kept as an explicit, auditable hook for future exceptions).
EXEMPT: set[str] = set()


def _required_items(root: Path) -> list[tuple[str, str]]:
    """Return (category, name) pairs that must each appear in README.md.

    Scope (see spec): every skill dir, every script file, every top-level docs/*.md.
    """
    items: list[tuple[str, str]] = []

    skills_dir = root / ".claude" / "skills"
    if skills_dir.is_dir():
        for d in sorted(skills_dir.iterdir()):
            if d.is_dir() and not d.name.startswith("."):
                items.append(("skill", d.name))

    scripts_dir = root / "scripts"
    if scripts_dir.is_dir():
        for f in sorted(scripts_dir.iterdir()):
            if f.is_file() and not f.name.startswith("."):
                items.append(("script", f.name))

    docs_dir = root / "docs"
    if docs_dir.is_dir():
        for f in sorted(docs_dir.glob("*.md")):
            items.append(("doc", f.name))

    return items


def _wildcard_prefixes(readme: str) -> list[str]:
    """Prefixes from `prefix*` tokens in the README (e.g. `speckit-*` -> 'speckit-')."""
    return [m.group(1) for m in re.finditer(r"([A-Za-z0-9_./-]+)\*", readme)]


def _is_documented(name: str, readme: str, prefixes: list[str]) -> bool:
    if name in readme:
        return True
    return any(prefix and name.startswith(prefix) for prefix in prefixes)


def find_missing(root: Path | str) -> list[str]:
    """Human-readable line per undocumented in-scope item; empty list when all are covered."""
    root = Path(root)
    readme_path = root / "README.md"
    readme = readme_path.read_text(encoding="utf-8") if readme_path.is_file() else ""
    prefixes = _wildcard_prefixes(readme)

    missing: list[str] = []
    for category, name in _required_items(root):
        if name in EXEMPT:
            continue
        if not _is_documented(name, readme, prefixes):
            missing.append(f"{category}: {name} (not found in README.md index)")
    return missing


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    missing = find_missing(root)
    if missing:
        print("Inventory coverage FAILED — add these to the README File index:")
        for line in missing:
            print(f"  - {line}")
        return 1
    print("Inventory coverage OK — every skill, script, and top-level doc is in the README index.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
