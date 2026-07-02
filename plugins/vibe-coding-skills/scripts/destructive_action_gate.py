#!/usr/bin/env python3
"""PreToolUse hook: pause destructive actions for explicit owner approval.

Agents are good at stateless code and bad at stateful consequences: the top production
failure mode is an unsupervised schema migration, database reset, or bulk delete. This
hook intercepts the action BEFORE it runs and downgrades it to "ask" — the owner sees a
plain-English explanation of what would change and approves or rejects it. Reads are
never gated; forward `migrate dev` is never gated; only the irreversible shapes are.

Opt-out: create a `.no-destructive-gate` file at the repo root.
Always exits 0; any internal error is swallowed (a hook must never break a session).
"""

import json
import re
import sys
from pathlib import Path

OPT_OUT_MARKER = ".no-destructive-gate"

# (pattern in the Bash command, plain-English reason shown to the owner)
BASH_RULES = [
    (
        re.compile(r"\brm\s+-[a-z]*(?:rf|fr)[a-z]*\b", re.IGNORECASE),
        "This command recursively force-deletes files (`rm -rf`) — anything removed is "
        "gone for good unless it was committed to git. Make sure the path is right "
        "before you approve.",
    ),
    (
        re.compile(r"\bdrop\s+(?:table|database|schema)\b", re.IGNORECASE),
        "This command DROPs a database table/database/schema — it permanently deletes "
        "the structure AND all data in it. Approve only if you are sure this data is "
        "expendable or backed up.",
    ),
    (
        re.compile(r"\btruncate\s+table\b", re.IGNORECASE),
        "This command TRUNCATEs a table — it wipes every row in it instantly, with no "
        "undo. Approve only if losing all rows in this table is intended.",
    ),
    (
        re.compile(r"\bdb\s+reset\b", re.IGNORECASE),
        "This command resets the database — it deletes ALL data and re-runs migrations "
        "from scratch. Fine on a throwaway dev database, catastrophic on one with real "
        "user data. Check which database this points at before you approve.",
    ),
    (
        re.compile(r"\bmigrate\s+(?:reset|down)\b", re.IGNORECASE),
        "This command rolls the database schema backwards (migrate reset/down), which "
        "usually deletes data created under the newer schema. Approve only if you "
        "understand what will be lost.",
    ),
    (
        re.compile(r"\bdelete\s+from\s+\S+\s*(?:;|$|\")", re.IGNORECASE),
        "This command bulk-DELETEs rows with no WHERE filter — it empties the whole "
        "table. If only some rows should go, reject and ask for a WHERE clause.",
    ),
    (
        re.compile(r"--dangerously-skip-permissions"),
        "This command runs the AI with --dangerously-skip-permissions, which removes "
        "every human approval gate (this one included). The kit's hard rule is to "
        "never use it.",
    ),
]

FILE_RULE = re.compile(r"(?:^|[\\/])migrations?[\\/]|schema\.(?:prisma|sql)$", re.IGNORECASE)

FILE_REASON = (
    "This edit touches a database migration or schema file — the blueprint for how "
    "data is stored. A wrong migration can destroy or corrupt real data when applied. "
    "Read the plain-English summary of the change and approve only if it matches what "
    "you asked for."
)

GATED_EDIT_TOOLS = {"Edit", "Write", "MultiEdit"}


def _ask(reason: str) -> dict:
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "ask",
            "permissionDecisionReason": reason,
        }
    }


def process(data: dict):
    """Return an 'ask' decision dict, or None to let the action through untouched."""
    root = Path(data.get("cwd") or Path.cwd())
    if (root / OPT_OUT_MARKER).exists():
        return None
    tool = data.get("tool_name")
    tool_input = data.get("tool_input") or {}

    if tool == "Bash":
        command = tool_input.get("command") or ""
        for pattern, reason in BASH_RULES:
            if pattern.search(command):
                return _ask(reason)
        return None

    if tool in GATED_EDIT_TOOLS:
        file_path = tool_input.get("file_path") or ""
        if FILE_RULE.search(file_path):
            return _ask(FILE_REASON)
        return None

    return None


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
