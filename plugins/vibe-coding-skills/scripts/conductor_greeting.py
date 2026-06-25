#!/usr/bin/env python3
"""SessionStart hook: offer the Conductor (`/start`) once per project.

The first time Claude Code opens in a real project that hasn't been greeted yet, this injects ONE
short line offering the Conductor — the proactive front-door mentor that walks a non-technical owner
through building (or changing) something without needing to know any commands. After firing, it drops
a marker (.claude/.conductor-greeted) and stays quiet forever after — no nagging.

Deterministic, stdlib only. Always exits 0 — a SessionStart hook must never block a session. The
greeting is only an OFFER; the Conductor never runs unless the owner says "start".

Manual fallback (non-Claude agents, where this hook doesn't run): when opening a project, tell the
owner they can say "start" to be guided — see `.claude/skills/start/SKILL.md`.
"""

import json
import sys
import time
from pathlib import Path

# Presence of any of these (or a .git dir) means "this is a real project".
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

MARKER_REL = (".claude", ".conductor-greeted")

GREETING = (
    "[conductor-greeting] This project has not been greeted by the Conductor yet. At the very START "
    "of your first reply this session, add ONE short line offering it, then continue with the user's "
    "actual request. Suggested line: \"\U0001f9ed New here? Say 'start' and I'll walk you through "
    "building (or changing) something step by step — no commands to memorize. Or just tell me what "
    "you want to do.\" Offer only once; only launch the Conductor (the /start skill) if the user agrees."
)


def existing_manifests(root: Path) -> list:
    return [root / m for m in MANIFESTS if (root / m).is_file()]


def is_real_project(root: Path) -> bool:
    """True if the directory looks like a real project (has git or a known manifest)."""
    return (root / ".git").exists() or bool(existing_manifests(root))


def should_greet(root: Path) -> bool:
    """Greet once: real project AND not greeted before."""
    if not is_real_project(root):
        return False
    return not root.joinpath(*MARKER_REL).exists()


def mark_done(root: Path) -> None:
    marker = root.joinpath(*MARKER_REL)
    try:
        marker.parent.mkdir(parents=True, exist_ok=True)
        marker.write_text(f"conductor greeted at {time.time():.0f}\n", encoding="utf-8")
    except OSError:
        pass


def main() -> int:
    raw = sys.stdin.read()
    try:
        data = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        return 0

    root = Path(data.get("cwd") or Path.cwd())
    if not should_greet(root):
        return 0

    mark_done(root)
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "SessionStart",
                    "additionalContext": GREETING,
                }
            }
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
