# scripts/ruff_on_edit.py
"""Ruff-on-edit: PostToolUse hook that auto-fixes Python files right after Claude edits them.

Runs `ruff check --fix` on the single file an Edit/Write/MultiEdit just touched, using the
project's own ruff.toml. Catches the same real bugs CI catches (undefined names, unused imports)
in-session, so a push is never red for something fixable on the spot.

Never blocks an edit: it only fixes-in-place and always exits 0. Non-Python edits are ignored.
"""

import json
import subprocess
import sys
from pathlib import Path

PY_EXTS = (".py", ".pyi")
EDIT_TOOLS = ("Edit", "Write", "MultiEdit")


def is_python(file_path: str) -> bool:
    """True if the edited path is a Python source file."""
    return bool(file_path) and file_path.lower().endswith(PY_EXTS)


def build_fix_argv(file_path: str) -> list:
    """The ruff command that auto-fixes just the edited file."""
    return ["ruff", "check", "--fix", file_path]


def run_fix(file_path: str, cwd) -> None:
    """Run ruff against the edited file. Best-effort: any failure is swallowed so the hook
    can never break the edit that already happened."""
    try:
        subprocess.run(
            build_fix_argv(file_path),
            cwd=str(cwd),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except OSError:
        pass


def main() -> int:
    raw = sys.stdin.read()
    try:
        data = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        return 0

    if data.get("tool_name") not in EDIT_TOOLS:
        return 0

    file_path = data.get("tool_input", {}).get("file_path", "")
    if not is_python(file_path):
        return 0

    run_fix(file_path, data.get("cwd") or Path.cwd())
    return 0


if __name__ == "__main__":
    sys.exit(main())
