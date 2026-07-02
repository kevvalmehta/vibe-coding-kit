# tests/test_lessons_injector.py
"""The lessons injector closes the learning loop: confirmed scars/patterns from
lessons.md must reach every session's context — and unreviewed auto-captured
candidates must NOT (the capture hook demonstrably mis-captures skill text)."""
import importlib.util
import json
from pathlib import Path

from _kitpaths import scripts_dir

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location(
    "lessons_injector", scripts_dir(ROOT) / "lessons_injector.py"
)
lessons_injector = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(lessons_injector)


LESSONS = """# Lessons — The Scar Log

## The template (copy this for every new entry)

```
### L-{number} — {short name of the rule in plain English}

**Rule:** {what to do or never do, one sentence.}
```

## Entries

### L-1 — One source of truth

**Rule:** Before adding any new tool, check whether something installed does the same job.

**What broke:** 2026-06-06 — TaskMaster overlapped Spec Kit.

**Self-check (run before saying "done"):** about to install a tool? Ask if one exists.

**Linked rule:** Principle V.

---

### P-1 — Ground against real docs

**Practice:** Point the AI at live library docs before coding against a library.

**Context:** invented Streamlit APIs.

**Why it matters:** stops invented-API bugs.

**When to apply:** any new library usage.

---

## Candidate lessons (auto-captured -- review, then promote to an L-# entry or delete)

### candidate -- 2026-07-01 12:12 (session 32e1f0)
**Trigger phrase (you said):** "Base directory for this skill: garbage capture..."
**Action:** review, then promote to an L-# entry above, or delete.
"""


def test_extracts_confirmed_entries_only():
    entries = lessons_injector.extract_confirmed(LESSONS)
    ids = [e["id"] for e in entries]
    assert ids == ["L-1", "P-1"]


def test_candidates_never_injected():
    digest = lessons_injector.build_digest(lessons_injector.extract_confirmed(LESSONS))
    assert "candidate" not in digest.lower()
    assert "garbage capture" not in digest


def test_template_placeholders_never_injected():
    # The L-{number} template block must not be mistaken for a confirmed entry.
    entries = lessons_injector.extract_confirmed(LESSONS)
    assert all("{number}" not in e["id"] for e in entries)


def test_digest_carries_rule_and_selfcheck():
    digest = lessons_injector.build_digest(lessons_injector.extract_confirmed(LESSONS))
    assert "one source of truth" in digest.lower()
    assert "self-check" in digest.lower()
    assert "live library docs" in digest.lower()


def test_no_lessons_file_is_silent_noop(tmp_path):
    out = lessons_injector.process({"cwd": str(tmp_path)})
    assert out is None


def test_no_confirmed_entries_is_silent_noop(tmp_path):
    mem = tmp_path / ".specify" / "memory"
    mem.mkdir(parents=True)
    (mem / "lessons.md").write_text("# Lessons\n\n## Entries\n\n(none yet)\n", encoding="utf-8")
    assert lessons_injector.process({"cwd": str(tmp_path)}) is None


def test_process_emits_sessionstart_context(tmp_path):
    mem = tmp_path / ".specify" / "memory"
    mem.mkdir(parents=True)
    (mem / "lessons.md").write_text(LESSONS, encoding="utf-8")
    out = lessons_injector.process({"cwd": str(tmp_path)})
    ctx = out["hookSpecificOutput"]
    assert ctx["hookEventName"] == "SessionStart"
    assert "L-1" in ctx["additionalContext"]
    assert json.dumps(out)  # must be JSON-serializable
