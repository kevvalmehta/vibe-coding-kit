#!/usr/bin/env python3
"""lint-goal.py — a tiny checker for a /goal task contract.

What it does (plain English): reads a goal file and FLAGS weak spots. It does not fix anything,
and it does not judge whether the goal is a good idea — it only checks that the contract has teeth.
This mirrors the constitution's Gate 1 idea: "the script decides, not the agent's word."

Usage:
    python3 scripts/lint-goal.py goal.txt
    python3 scripts/lint-goal.py            # reads from stdin (paste a goal, then Ctrl-D)

Exit code 0 = clean, 1 = problems found (handy for CI). Use --quiet to print only problems.
"""
from __future__ import annotations

import argparse
import re
import sys

# The seven fields a complete contract should name (case-insensitive, ":" optional-ish).
REQUIRED_FIELDS = [
    ("outcome", r"\boutcome\b"),
    ("verification", r"\bverif"),                 # verification / verify
    ("constraints", r"\bconstraint"),
    ("boundaries", r"\bboundar"),                 # boundary / boundaries
    ("iteration", r"\biterat"),                   # iteration / iterate
    ("done when", r"\bdone\s*when\b|\bcompletion\b"),
    ("pause / stop", r"\bpause\b|\bstop\s*when\b|\bstop\b"),
]

# Phrases that mean the goal is too loose. (pattern, plain-English why)
WEAK_PHRASES = [
    (r"\bmake sure it works\b", "vague verification — say WHAT proves it (command, log, screenshot, passing test)"),
    (r"\bit should work\b", "vague verification — name the concrete proof instead"),
    (r"\bconfirm (?:it'?s |it is )?(?:working|done)\b", "vague verification — name the concrete proof instead"),
    (r"\bworks (?:fine|properly|correctly)\b", "vague verification — name the concrete proof instead"),
    (r"\bedit anything\b", "unbounded write permission — name the files/areas the agent may touch"),
    (r"\bchange whatever\b", "unbounded write permission — name the lane"),
    (r"\banywhere in the (?:code|repo|project)\b", "unbounded write permission — name the lane"),
    (r"\bkeep trying\b", "infinite retry — set a hard cap (e.g. 'at most 3 focused rounds')"),
    (r"\buntil it works\b", "infinite retry — set a hard cap and a 'read the error first' step"),
    (r"\bretry forever\b", "infinite retry — set a hard cap"),
    (r"\bmake it (?:better|nicer|good|professional|pop)\b", "fuzzy finish line — translate into a design direction + a screenshot check"),
]

# Leftover template placeholders that should never appear in a copy-ready goal.
PLACEHOLDERS = [
    (r"\[[^\]\n]{0,40}\]", "placeholder in square brackets — fill it in"),
    (r"\bTODO\b", "TODO left in — fill it in"),
    (r"\bTBD\b", "TBD left in — fill it in"),
    (r"\bFIXME\b", "FIXME left in — fill it in"),
    (r"<[^>\n]{0,40}>", "angle-bracket placeholder — fill it in"),
    (r"待定|占位", "placeholder text left in — fill it in"),
]


def find_line(text: str, match_start: int) -> int:
    return text.count("\n", 0, match_start) + 1


def lint(text: str) -> list[tuple[str, int, str]]:
    """Return a list of (severity, line_no, message)."""
    problems: list[tuple[str, int, str]] = []
    low = text.lower()

    # 1) Missing fields
    for label, pat in REQUIRED_FIELDS:
        if not re.search(pat, low):
            problems.append(("missing", 0, f"no '{label}' field found — a complete contract names all seven"))

    # 2) Weak phrases
    for pat, why in WEAK_PHRASES:
        for m in re.finditer(pat, text, flags=re.IGNORECASE):
            problems.append(("weak", find_line(text, m.start()), f"\"{m.group(0).strip()}\" — {why}"))

    # 3) Placeholders
    for pat, why in PLACEHOLDERS:
        for m in re.finditer(pat, text):
            frag = m.group(0).strip()
            problems.append(("placeholder", find_line(text, m.start()), f"\"{frag}\" — {why}"))

    return problems


def main() -> int:
    ap = argparse.ArgumentParser(description="Flag weak spots in a /goal task contract.")
    ap.add_argument("file", nargs="?", help="path to the goal file (omit to read stdin)")
    ap.add_argument("--quiet", action="store_true", help="print only problems")
    args = ap.parse_args()

    if args.file:
        try:
            with open(args.file, encoding="utf-8") as fh:
                text = fh.read()
        except OSError as e:
            print(f"could not read {args.file}: {e}", file=sys.stderr)
            return 2
    else:
        text = sys.stdin.read()

    problems = lint(text)

    if not problems:
        if not args.quiet:
            print("OK — goal looks executable: all seven fields present, no weak verification, "
                  "no placeholders, no unbounded permissions.")
        return 0

    order = {"missing": 0, "weak": 1, "placeholder": 2}
    problems.sort(key=lambda p: (order.get(p[0], 9), p[1]))
    print(f"Found {len(problems)} thing(s) to tighten:\n")
    for severity, line_no, msg in problems:
        where = f"line {line_no}" if line_no else "whole goal"
        print(f"  [{severity:<11}] ({where}) {msg}")
    print("\nFix these so the goal is safe to hand to an agent.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
