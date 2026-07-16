#!/usr/bin/env python3
"""SessionStart hook: inject confirmed lessons (the Scar Log) into every session.

Closes the learning loop. capture-lessons.ps1 WRITES candidate lessons after each turn,
but until this hook nothing ever READ the confirmed entries back — so every session
started blank and "learn from your mistakes" never stuck.

Injects ONLY confirmed `### L-#` (scar) and `### P-#` (pattern) entries from
.specify/memory/lessons.md — never the auto-captured candidates (unreviewed suspects,
sometimes mis-captured noise) and never the copy-me templates.

Output: a SessionStart additionalContext block with a compact digest (Rule + Self-check
per entry). No lessons file or no confirmed entries -> prints nothing.
Always exits 0 — a SessionStart hook must never block a session from starting.
"""

import json
import re
import sys
from pathlib import Path

LESSONS_REL = (".specify", "memory", "lessons.md")

# Evolve-loop nudges (Hermes-style consolidation-by-constraint): a pile of unreviewed
# candidates or a bloated file must be surfaced at session start, or capture rots
# silently (the same junk candidate was once logged 14 times, unnoticed).
CANDIDATE_RE = re.compile(r"^### candidate --", re.MULTILINE)
LESSONS_CAP_CHARS = 16_000   # ~4k tokens; past 80% /evolve must consolidate, not append
CAP_WARN_FRAC = 0.8

# A confirmed entry heading: "### L-12 — name" or "### P-3 — name".
# Template placeholders ("### L-{number} — ...") deliberately do not match.
ENTRY_RE = re.compile(r"^### (?P<id>[LP]-\d+)\s*[—-]+\s*(?P<title>.+)$", re.MULTILINE)

HEADER = (
    "[lessons-injector] Confirmed lessons from this project's Scar Log "
    "(.specify/memory/lessons.md) — real past mistakes (L-#) and proven habits (P-#). "
    "Apply every rule below; run each self-check before you claim any task is done.\n"
)


def extract_confirmed(text: str) -> list:
    """Return [{'id','title','rule','selfcheck','body'}] for confirmed L-#/P-# entries.

    Entries inside fenced code blocks (the templates) and the auto-captured candidates
    section are excluded — templates can't match ENTRY_RE, and candidates use a
    different heading ("### candidate -- ...").
    """
    # Drop fenced code blocks so template examples can never leak through.
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    entries = []
    matches = list(ENTRY_RE.finditer(text))
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[m.end() : end]
        # Stop an entry's body at a section heading (## ...) such as the candidates section.
        cut = re.search(r"^## ", body, re.MULTILINE)
        if cut:
            body = body[: cut.start()]
        rule = _field(body, r"\*\*(?:Rule|Practice):\*\*\s*(.+)")
        selfcheck = _field(body, r"\*\*(?:Self-check[^:*]*|When to apply):\*\*\s*(.+)")
        entries.append(
            {
                "id": m.group("id"),
                "title": m.group("title").strip(),
                "rule": rule,
                "selfcheck": selfcheck,
                "body": body.strip(),
            }
        )
    return entries


def _field(body: str, pattern: str):
    m = re.search(pattern, body)
    return m.group(1).strip() if m else None


def build_digest(entries: list):
    """One compact block per entry: id, title, rule, self-check. Falls back to the raw
    entry body if the standard fields are missing (hand-written entries still count)."""
    if not entries:
        return None
    parts = [HEADER]
    for e in entries:
        if e["rule"]:
            line = f"- {e['id']} ({e['title']}): {e['rule']}"
            if e["selfcheck"]:
                line += f" Self-check: {e['selfcheck']}"
            parts.append(line)
        else:
            parts.append(f"- {e['id']} ({e['title']}):\n{e['body']}")
    return "\n".join(parts)


def process(data: dict):
    """Return the hook output dict, or None for a silent no-op."""
    root = Path(data.get("cwd") or Path.cwd())
    lessons = root.joinpath(*LESSONS_REL)
    if not lessons.is_file():
        return None
    text = lessons.read_text(encoding="utf-8")
    digest = build_digest(extract_confirmed(text))
    nudges = []
    n_cand = len(CANDIDATE_RE.findall(text))
    if n_cand:
        nudges.append(
            f"[evolve] {n_cand} unreviewed candidate lesson(s) pending in lessons.md — "
            "run /evolve to distill them into confirmed rules or the owner profile "
            "(real lessons promoted, junk deleted)."
        )
    frac = len(text) / LESSONS_CAP_CHARS
    if frac >= CAP_WARN_FRAC:
        nudges.append(
            f"[evolve] lessons.md is at {round(frac * 100)}% of its {LESSONS_CAP_CHARS:,}-char "
            "budget — /evolve must consolidate (merge, sharpen, delete) before adding new entries."
        )
    if nudges:
        digest = (digest + "\n" if digest else "") + "\n".join(nudges)
    if not digest:
        return None
    return {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": digest,
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
