# scripts/tdd_guard.py
"""TDD-Guard: PreToolUse hook that enforces test-first edits during a build.

Off by default. Active only when a `.tdd-guard` marker file exists at repo root.
See docs/superpowers/specs/2026-06-13-tdd-guard-design.md.
"""

import json
import shlex
import subprocess
import sys
from pathlib import Path

CODE_EXTS = {".py", ".pyi", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs"}
TEST_FILENAMES = {"conftest.py"}


def classify(file_path: str) -> str:
    """Return 'test', 'impl', or 'noncode' for a target file path."""
    p = file_path.replace("\\", "/").lower()
    name = p.rsplit("/", 1)[-1]
    if (
        name in TEST_FILENAMES
        or "/tests/" in f"/{p}"
        or name.startswith("test_")
        or name.endswith("_test.py")
        or name.endswith((".test.ts", ".spec.ts", ".test.js", ".spec.js"))
    ):
        return "test"
    ext = name[name.rfind(".") :] if "." in name else ""
    return "impl" if ext in CODE_EXTS else "noncode"


def decide(mode, classification: str, tests_red: bool) -> str:
    """Return 'allow' or 'block'.

    mode: None (guard off) | 'strict' | 'refactor' | anything else (treated as strict).
    """
    if mode is None:
        return "allow"
    if classification in ("test", "noncode"):
        return "allow"
    if mode == "refactor":
        return "allow"
    return "allow" if tests_red else "block"


MARKER = ".tdd-guard"
DEFAULT_TEST_CMD = "python -m pytest -q"


def read_marker(root):
    """Return {'mode':..., 'test':...} if the marker exists at root, else None."""
    marker = Path(root) / MARKER
    if not marker.exists():
        return None
    cfg = {"mode": "strict", "test": DEFAULT_TEST_CMD}
    for line in marker.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        cfg[key.strip()] = value.strip()
    return cfg


def tests_are_red(test_cmd: str, cwd) -> bool:
    """Run the test command; True if a test fails (non-zero exit)."""
    result = subprocess.run(
        shlex.split(test_cmd),
        cwd=str(cwd),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode != 0


BLOCK_MSG = (
    "TDD-Guard: all tests are green — write a failing test before adding or changing "
    "implementation code. (Refactoring? set 'mode: refactor' in .tdd-guard.)"
)


def main() -> int:
    raw = sys.stdin.read()
    try:
        data = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        data = {}

    if data.get("tool_name") not in ("Edit", "Write", "MultiEdit"):
        return 0

    file_path = data.get("tool_input", {}).get("file_path", "")
    root = Path(data.get("cwd") or Path.cwd())

    marker = read_marker(root)
    if marker is None:
        return 0

    classification = classify(file_path)
    tests_red = False
    if classification == "impl" and marker.get("mode") != "refactor":
        tests_red = tests_are_red(marker.get("test", DEFAULT_TEST_CMD), root)

    if decide(marker.get("mode"), classification, tests_red) == "block":
        print(
            json.dumps(
                {
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": "deny",
                        "permissionDecisionReason": BLOCK_MSG,
                    }
                }
            )
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
