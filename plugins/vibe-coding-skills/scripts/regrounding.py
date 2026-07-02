#!/usr/bin/env python3
"""SessionStart hook (resume/compact only): re-ground the model in real project state.

Long sessions drift: after context compression (or resuming an old session) the model
works from a SUMMARY of what happened — and summaries are memory, not proof. This hook
injects fresh ground truth (current branch, changed files, last commit, HANDOFF pointer)
the moment a compressed/resumed session starts, so state claims restart from facts.

Fires only when the session source is `resume` or `compact` (a normal startup already
reads CLAUDE.md/HANDOFF.md cold). Never blocks; always exits 0.
"""

import json
import subprocess
import sys
from pathlib import Path

MAX_FILES_SHOWN = 10
FIRE_ON = {"resume", "compact"}


def _git(args, cwd):
    result = subprocess.run(
        ["git"] + args,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        timeout=10,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())
    return result.stdout.strip()


def git_snapshot(root):
    """{'branch','changed','last_commit'} or None when root is not a git repo."""
    try:
        branch = _git(["branch", "--show-current"], root)
        status = _git(["status", "--porcelain"], root)
        last_commit = _git(["log", "-1", "--format=%h %s"], root)
    except Exception:
        return None
    # porcelain lines are "XY path" (two status chars + space); strip prefix defensively
    changed = [line[2:].strip() for line in status.splitlines() if line.strip()]
    return {"branch": branch or "(detached)", "changed": changed, "last_commit": last_commit}


def build_context(snap: dict, root: Path) -> str:
    files = snap["changed"]
    shown = ", ".join(files[:MAX_FILES_SHOWN]) or "none"
    more = f" (+{len(files) - MAX_FILES_SHOWN} more)" if len(files) > MAX_FILES_SHOWN else ""
    handoff = ""
    if (root / "HANDOFF.md").is_file():
        handoff = " Re-read HANDOFF.md before making any claim about what is built or decided."
    return (
        "[re-ground] This session was resumed or its context was compressed. A summary is "
        "memory, and memory is not proof — re-verify any belief about project state against "
        f"this live snapshot before acting on it. Ground truth now: branch '{snap['branch']}', "
        f"{len(files)} file(s) with uncommitted changes ({shown}{more}), "
        f"last commit: {snap['last_commit']}.{handoff} If you were mid-task, restate the task "
        "and what is verified-done vs assumed-done before continuing."
    )


def process(data: dict):
    """Return the hook output dict, or None for a silent no-op."""
    if data.get("source") not in FIRE_ON:
        return None
    root = Path(data.get("cwd") or Path.cwd())
    snap = git_snapshot(root)
    if snap is None:
        return None
    return {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": build_context(snap, root),
        }
    }


def main() -> int:
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
        out = process(data)
        if out:
            print(json.dumps(out))
    except Exception:
        pass  # a hook must never break a session
    return 0


if __name__ == "__main__":
    sys.exit(main())
