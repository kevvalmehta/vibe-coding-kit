#!/usr/bin/env python3
"""SessionStart hook: offer the Claude automation recommender, but only when it would help.

Fires the offer at most ONCE per project: the first time Claude Code opens in a real project
that hasn't been offered yet, OR later when a dependency manifest changes (new framework ->
maybe a new hook / MCP server is worth it). After firing, it drops a marker file
(.claude/.recommender-nudged) so it stays quiet on every later session — no nagging.

Detection is plain code (deterministic, cheap). The actual nudge is one line of injected context
telling Claude to offer the recommender; Claude never runs it unprompted.

Output: prints a SessionStart additionalContext JSON block only when a signal fires; otherwise
nothing. Always exits 0 — a SessionStart hook must never block a session from starting.
"""

import json
import sys
import time
from pathlib import Path

# Files whose presence means "this is a real project" and whose mtime means "deps changed".
MANIFESTS = (
    "package.json",
    "pyproject.toml",
    "requirements.txt",
    "go.mod",
    "Cargo.toml",
    "pom.xml",
    "build.gradle",
    "Gemfile",
    "composer.json",
)

MARKER_REL = (".claude", ".recommender-nudged")

NUDGE = (
    "[recommender-nudge] This project looks newly opened (or a dependency manifest just changed) "
    "and the Claude automation recommender has not been offered here yet. At the very START of your "
    "first reply this session, add ONE short line offering it, then continue with the user's actual "
    "request. Suggested line: \"\U0001f4a1 Looks like a fresh project — want me to run the "
    "recommender? It scans this codebase and suggests tailored hooks, subagents, and MCP servers. "
    "Say 'run the recommender', or 'not now'.\" Offer only once; do NOT run it unless the user agrees."
)


def existing_manifests(root: Path) -> list:
    return [root / m for m in MANIFESTS if (root / m).is_file()]


def is_real_project(root: Path) -> bool:
    """True if the directory looks like a real project (has git or a known manifest)."""
    return (root / ".git").exists() or bool(existing_manifests(root))


def newest_manifest_mtime(root: Path) -> float:
    times = [p.stat().st_mtime for p in existing_manifests(root)]
    return max(times) if times else 0.0


def should_nudge(root: Path) -> bool:
    """Fire if the project is real AND (never offered yet OR a manifest changed since we offered)."""
    if not is_real_project(root):
        return False
    marker = root.joinpath(*MARKER_REL)
    if not marker.exists():
        return True
    return newest_manifest_mtime(root) > marker.stat().st_mtime


def mark_done(root: Path) -> None:
    marker = root.joinpath(*MARKER_REL)
    try:
        marker.parent.mkdir(parents=True, exist_ok=True)
        marker.write_text(f"recommender offered at {time.time():.0f}\n", encoding="utf-8")
    except OSError:
        pass


def main() -> int:
    raw = sys.stdin.read()
    try:
        data = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        return 0

    root = Path(data.get("cwd") or Path.cwd())

    if not should_nudge(root):
        return 0

    mark_done(root)
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "SessionStart",
                    "additionalContext": NUDGE,
                }
            }
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
