# Memory Snapshot — Index

This folder mirrors Claude Code's session memory so **other AI tools** (Codex, Cursor)
can read the same persistent project rules. It is updated automatically by the Stop hook
after each Claude Code turn (`sync_memory_to_repo.py`).

## What lives here
- This `MEMORY.md` — index of persistent rules.
- Additional `.md` files copied from Claude Code's memory directory (populated automatically).

## Source-of-truth rules
The authoritative project rules are in:
- `../../.specify/memory/constitution.md` — the hard rules (security, TDD, regression safety)
- `../../HANDOFF.md` — current state
- `../../CLAUDE.md` / `../../AGENTS.md` — full brief

If this folder is empty, the Claude Code memory hook has not run yet — read the files above instead.
