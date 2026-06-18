# Spec — Inventory Coverage Gate

## Why (problem)
The README "File index" is a hand-maintained list. Nothing forced it to stay complete, so summaries of
the kit (by humans or AI sessions) kept dropping real features (`.mcp.json`, the awesome-claude-code
shortlist, scripts, etc.). A written "keep this complete" note is trust-based; a new skill/script/doc
can be added and silently left out of the index.

## What (outcome)
A mechanical gate that **fails CI** when something that should be documented is missing from `README.md`.
This turns the documented "completeness rule" into an enforced one — the index cannot silently rot.

## Scope (what must be individually documented in README.md)
The gate checks that **each of these appears in `README.md`**:
- Every skill — each subdirectory of `.claude/skills/`.
- Every script — each file directly in `scripts/`.
- Every top-level doc — each `*.md` directly in `docs/`.

A name counts as documented if its exact name appears in `README.md`, **or** a wildcard token of the
form `prefix*` is present and the name starts with `prefix` (so a family like `speckit-*` can be
documented as one group).

Out of scope for v1 (documented by group, not individually — low value, high false-positive risk):
`specs/` subfiles, `tests/` files, `.specify/` internals, files in `docs/` subdirectories.

## Functional requirements
- **FR-001:** `scripts/check_inventory.py` exposes `find_missing(root) -> list[str]` returning a
  human-readable line per undocumented item (category + path), empty when all covered.
- **FR-002:** Run as a script (`python scripts/check_inventory.py`) it prints the missing items and
  exits non-zero when any are missing, zero when clean.
- **FR-003:** A pytest test asserts `find_missing` is empty for the current repo, so the existing CI
  `pytest` step blocks any push/PR that leaves a skill/script/top-level-doc out of the index.

## Success criteria
- **SC-001:** Adding a new skill dir / script / top-level doc without listing it in README turns the
  test RED.
- **SC-002:** With the index complete, the test is GREEN and `python scripts/check_inventory.py`
  exits 0.
- **SC-003:** No network, no model calls — pure filesystem string reads (matches existing guard tests).

## Architecture
Plain Python stdlib (`pathlib`, `re`). One script + one guard test. No new CI step — the repo's
existing `test` job already runs `pytest`, so the test IS the gate.
