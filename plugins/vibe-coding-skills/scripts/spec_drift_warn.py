#!/usr/bin/env python3
"""PreToolUse hook: warn (never block) when code is committed without a spec update.

Spec-anchored development keeps the AI on rails: the spec is the source of truth, and code
is meant to follow it. When code changes but no spec/plan file changes alongside it, the
project quietly drifts away from its own spec — and the next AI session works from a spec
that no longer matches reality. This hook catches that at commit time.

Fires only on a `git commit` Bash command. If any staged path is in a source dir
(app/, src/, lib/, scripts/, plugins/) AND no staged path is under specs/ or .specify/,
it emits an advisory systemMessage. It is ADVISORY ONLY — it returns no permission
decision at all (an explicit "allow" would force-approve the command and bypass the
user's normal permission prompt); it never blocks or auto-approves a commit.

Opt-out: create a `.no-spec-drift-warn` file at the repo root.
Always exits 0; any internal error is swallowed (a hook must never break a session).
"""

import json
import re
import subprocess
import sys
from pathlib import Path

OPT_OUT_MARKER = ".no-spec-drift-warn"
GIT_COMMIT_RE = re.compile(r"\bgit\s+commit\b")
SOURCE_PREFIXES = ("app/", "src/", "lib/", "scripts/", "plugins/")
SPEC_PREFIXES = ("specs/", ".specify/")

WARNING = (
    "WARNING: code changed without a spec update — update the spec first to prevent AI "
    "drift (spec-anchored development). Suppress with .no-spec-drift-warn."
)


def _staged_files(cwd: Path):
    """Staged paths (posix strings), or None if not a git repo / git failed."""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=10,
        )
    except Exception:
        return None
    if result.returncode != 0:
        return None
    return [line.strip().replace("\\", "/") for line in result.stdout.splitlines() if line.strip()]


def process(data: dict):
    """Return the hook output dict, or None for a silent no-op."""
    if data.get("tool_name") != "Bash":
        return None
    command = (data.get("tool_input") or {}).get("command") or ""
    if not GIT_COMMIT_RE.search(command):
        return None
    root = Path(data.get("cwd") or Path.cwd())
    if (root / OPT_OUT_MARKER).exists():
        return None
    staged = _staged_files(root)
    if not staged:
        return None
    touched_source = any(p.startswith(SOURCE_PREFIXES) for p in staged)
    touched_spec = any(p.startswith(SPEC_PREFIXES) for p in staged)
    if not (touched_source and not touched_spec):
        return None
    return {"systemMessage": WARNING}


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
