#!/usr/bin/env python3
"""Stop hook: block strong completion claims that were never verified this turn.

Mechanizes the owner's Truth Over Confidence rule. If the assistant's final message
claims "tests pass" / "pushed" / "committed" / "build green" / "deployed" / "lint clean"
but the matching command was never actually run in the SAME turn, the turn is blocked
with a plain-English reason: run the proving command, or correct the claim.

v1 checks command PRESENCE, not output — it catches the dominant failure (a confident
claim with zero verification behind it). Output-parsing is a later tightening.

Opt-out: create a `.no-claim-verify` file at the repo root.
Respects stop_hook_active so a blocked turn can't loop forever.
Always exits 0; any internal error is swallowed (a hook must never break a session).
"""

import json
import re
import sys
from pathlib import Path

OPT_OUT_MARKER = ".no-claim-verify"

# claim category -> (claim pattern in assistant prose, evidence pattern in run commands)
CATEGORIES = {
    "tests": (
        re.compile(
            r"\b(?:all\s+)?tests?\s+(?:pass(?:ed|ing)?|(?:are|go|stay)\s+green)\b"
            r"|\bsuite\s+(?:is\s+)?green\b"
            r"|\b\d+\s+(?:tests?\s+)?passed\b",
            re.IGNORECASE,
        ),
        re.compile(
            r"\b(?:pytest|python\s+-m\s+pytest|npm\s+test|npx\s+(?:jest|vitest)|yarn\s+test|"
            r"pnpm\s+test|go\s+test|cargo\s+test|python\s+-m\s+unittest)\b",
            re.IGNORECASE,
        ),
    ),
    "push": (
        re.compile(r"\bpushed\b", re.IGNORECASE),
        re.compile(r"\bgit\s+push\b", re.IGNORECASE),
    ),
    "commit": (
        re.compile(r"\bcommitted\b", re.IGNORECASE),
        re.compile(r"\bgit\s+commit\b", re.IGNORECASE),
    ),
    "build": (
        re.compile(r"\bbuild\s+(?:succeed(?:s|ed)?|pass(?:es|ed)?|is\s+green)\b", re.IGNORECASE),
        re.compile(
            r"\b(?:npm\s+run\s+build|yarn\s+build|pnpm\s+build|tsc\b|cargo\s+build|"
            r"go\s+build|vite\s+build|next\s+build)",
            re.IGNORECASE,
        ),
    ),
    "deploy": (
        re.compile(r"\bdeployed\b", re.IGNORECASE),
        re.compile(r"\b(?:vercel|render|fly|netlify|deploy)\b", re.IGNORECASE),
    ),
    "lint": (
        re.compile(r"\blint(?:er|ing)?\s+(?:pass(?:es|ed)?|(?:is\s+)?clean)\b", re.IGNORECASE),
        re.compile(r"\b(?:ruff|eslint|biome|flake8|pylint)\b", re.IGNORECASE),
    ),
}

PROOF_HINT = {
    "tests": "run the test suite (e.g. `python -m pytest -q` / `npm test`)",
    "push": "run `git push` (or `git rev-list --count origin/<branch>..HEAD`, 0 = pushed)",
    "commit": "run `git commit` / show `git log -1`",
    "build": "run the build command",
    "deploy": "show the deploy command / URL check",
    "lint": "run the linter",
}


def _blocks(line_obj):
    content = (line_obj.get("message") or {}).get("content")
    if content is None:
        return []
    if isinstance(content, str):
        return [{"type": "text", "text": content}]
    return [b for b in content if isinstance(b, dict)]


def _is_real_user_message(line_obj) -> bool:
    """True only for the human speaking — tool_result messages also have type 'user'."""
    if line_obj.get("type") != "user":
        return False
    blocks = _blocks(line_obj)
    if any(b.get("type") == "tool_result" for b in blocks):
        return False
    return any(b.get("type") == "text" and (b.get("text") or "").strip() for b in blocks)


def load_turn(transcript_path: Path) -> list:
    """Parse the transcript and return only the lines after the last real user message."""
    objs = []
    for raw in transcript_path.read_text(encoding="utf-8", errors="replace").splitlines():
        raw = raw.strip()
        if not raw:
            continue
        try:
            objs.append(json.loads(raw))
        except json.JSONDecodeError:
            continue
    last_user = -1
    for i, obj in enumerate(objs):
        if _is_real_user_message(obj):
            last_user = i
    return objs[last_user + 1 :]


# "NOT pushed" / "hasn't been deployed" are honest status lines, not completion claims.
NEGATION_RE = re.compile(
    r"\b(?:not|never|no|haven'?t|hasn'?t|isn'?t|aren'?t|wasn'?t|weren'?t|won'?t(?:\s+be)?|"
    r"without(?:\s+being)?|un)[\s-]*(?:yet\s+|been\s+|be\s+|being\s+)*"
    r"(?:pushed|committed|deployed|merged|verified|tested)\b",
    re.IGNORECASE,
)


def detect_claims(text: str) -> set:
    text = NEGATION_RE.sub(" ", text)
    return {cat for cat, (claim_re, _) in CATEGORIES.items() if claim_re.search(text)}


def evidence_in_turn(turn: list) -> set:
    """Claim categories whose verifying command was actually run this turn."""
    commands = []
    for obj in turn:
        if obj.get("type") != "assistant":
            continue
        for b in _blocks(obj):
            if b.get("type") == "tool_use":
                cmd = (b.get("input") or {}).get("command")
                if cmd:
                    commands.append(cmd)
    joined = "\n".join(commands)
    return {cat for cat, (_, ev_re) in CATEGORIES.items() if ev_re.search(joined)}


def final_assistant_text(turn: list) -> str:
    """The last assistant text in the turn — the message the user is about to read."""
    for obj in reversed(turn):
        if obj.get("type") != "assistant":
            continue
        texts = [b.get("text", "") for b in _blocks(obj) if b.get("type") == "text"]
        if any(t.strip() for t in texts):
            return "\n".join(texts)
    return ""


def process(data: dict):
    """Return a block decision dict, or None to stay silent."""
    if data.get("stop_hook_active"):
        return None  # we already blocked once this turn; never loop
    root = Path(data.get("cwd") or Path.cwd())
    if (root / OPT_OUT_MARKER).exists():
        return None
    transcript = Path(data.get("transcript_path") or "")
    if not transcript.is_file():
        return None

    turn = load_turn(transcript)
    claims = detect_claims(final_assistant_text(turn))
    if not claims:
        return None
    unproven = sorted(claims - evidence_in_turn(turn))
    if not unproven:
        return None

    wants = "; ".join(f"'{c}' claim -> {PROOF_HINT[c]}" for c in unproven)
    return {
        "decision": "block",
        "reason": (
            "Done-claim verifier: your final message makes a completion claim that was not "
            f"verified in this turn ({', '.join(unproven)}). Truth over confidence: either "
            f"run the proving command now and show its output ({wants}), or rewrite the "
            "claim honestly (e.g. 'I believe X but have not verified'). Do not restate the "
            "claim without proof."
        ),
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
