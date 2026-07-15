#!/usr/bin/env python3
"""recall.py -- search your saved memory AND past session transcripts by keyword.

The "goldfish" fix. Claude Code already stores every session's FULL transcript on disk
(``~/.claude/projects/<project>/*.jsonl``) plus your saved memories as markdown -- but nothing
searches them, so a decision from weeks ago feels lost. This greps both and prints dated, readable
matches, so "what did we decide about X?" returns an answer instead of a shrug.

Local-only by design: no network, no AI call, no telemetry -- it only reads files already on your
disk. Any AI tool (Claude, Codex, Cursor) can run it; that is why it is a script, not a Claude rule.

Usage:
  python scripts/recall.py ponytail statusline   # AND-match: text containing BOTH words
  python scripts/recall.py --all supabase         # search EVERY project, not just this one

Always exits 0 -- a search with no results is not an error.
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

MAX_HITS = 40  # cap output so a common word can't dump the whole (68 MB+) history
SNIPPET = 240  # chars of context shown around a match
_REMINDER = re.compile(r"(?s)<system-reminder>.*?</system-reminder>")
_WS = re.compile(r"\s+")


def claude_home() -> Path:
    return Path(os.environ.get("CLAUDE_CONFIG_DIR") or (Path.home() / ".claude"))


def project_slug(cwd: Path) -> str:
    # Claude Code names each project dir by replacing every non-alphanumeric char with '-'
    # (e.g. C:\Projects\My App -> C--Projects-My-App). Mirror that to find THIS project's dir.
    return re.sub(r"[^A-Za-z0-9]", "-", str(cwd))


def _matches(text: str, needles: list[str]) -> bool:
    low = text.lower()
    return all(n in low for n in needles)


def _snippet(text: str, needles: list[str]) -> str:
    low = text.lower()
    pos = min((low.find(n) for n in needles if n in low), default=0)
    start = max(0, pos - SNIPPET // 3)
    body = _WS.sub(" ", text[start : start + SNIPPET]).strip()
    return ("..." if start else "") + body


def _transcript_messages(jsonl: Path):
    """Yield (role, date, text) of real user/assistant text; skip tool blocks + injected reminders."""
    try:
        raw = jsonl.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if obj.get("type") not in ("user", "assistant"):
            continue
        content = (obj.get("message") or {}).get("content")
        if isinstance(content, str):
            text = content
        elif isinstance(content, list):
            text = "\n".join(
                b.get("text", "") for b in content
                if isinstance(b, dict) and b.get("type") == "text"
            )
        else:
            continue
        text = _REMINDER.sub(" ", text).strip()
        if text:
            yield obj.get("type", "?"), (obj.get("timestamp") or "")[:10], text


def search(needles: list[str], all_projects: bool) -> list[tuple[str, str, str, str]]:
    """Return (kind, date, location, snippet) hits: memory files first, then transcripts."""
    home = claude_home()
    projects = home / "projects"
    hits: list[tuple[str, str, str, str]] = []

    # 1. Saved memory (clean, high-signal): auto-memory dir(s) + this repo's memory files.
    md_dirs: list[Path] = []
    if all_projects:
        md_dirs += [p / "memory" for p in projects.glob("*") if (p / "memory").is_dir()]
    else:
        md_dirs.append(projects / project_slug(Path.cwd()) / "memory")
    md_dirs += [Path.cwd() / ".specify" / "memory", Path.cwd() / "docs" / "memory-snapshot"]

    for d in md_dirs:
        if not d.is_dir():
            continue
        for md in sorted(d.rglob("*.md")):
            try:
                lines = md.read_text(encoding="utf-8", errors="ignore").splitlines()
            except OSError:
                continue
            for ln in lines:
                if _matches(ln, needles):
                    hits.append(("memory", "", str(md), _WS.sub(" ", ln.strip())[:SNIPPET]))

    # 2. Transcripts (the COMPLETE record -- reaches things never saved as a memory).
    if all_projects:
        transcript_files = sorted(projects.glob("*/*.jsonl"))
    else:
        pdir = projects / project_slug(Path.cwd())
        transcript_files = sorted(pdir.glob("*.jsonl")) if pdir.is_dir() else []

    seen: set[str] = set()
    for jsonl in transcript_files:
        for role, date, text in _transcript_messages(jsonl):
            if not _matches(text, needles):
                continue
            snip = _snippet(text, needles)
            key = snip[:120]
            if key in seen:  # dedupe near-identical hits (transcripts repeat context across turns)
                continue
            seen.add(key)
            hits.append((role, date, jsonl.stem[:8], snip))
    return hits


def main(argv: list[str]) -> int:
    try:  # Windows cp1252 consoles crash on emoji/smart quotes from transcripts; never crash recall.
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
    all_projects = "--all" in argv
    needles = [a.lower() for a in argv if not a.startswith("--")]
    if not needles:
        print("usage: python scripts/recall.py [--all] <keyword> [keyword ...]")
        return 0  # not an error -- just nothing to search for

    hits = search(needles, all_projects)
    scope = "all projects" if all_projects else "this project"
    if not hits:
        print(f"No memory or transcript match for {needles} ({scope}).")
        print("Try fewer/different words, or add --all to search every project.")
        return 0

    shown = hits[:MAX_HITS]
    print(f"{len(hits)} match(es) for {needles} ({scope}), showing {len(shown)}:\n")
    for kind, date, loc, snip in shown:
        tag = f"{date} " if date else ""
        print(f"  [{kind:9}] {tag}{loc}\n    {snip}\n")
    if len(hits) > len(shown):
        print(f"... {len(hits) - len(shown)} more hidden (cap {MAX_HITS}); narrow your keywords.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
