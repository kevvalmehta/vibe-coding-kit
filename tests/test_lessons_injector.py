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


# ---------------------------------------------------------------------------
# Evolve-loop nudges (Hermes-style: capture without distillation just rots).
# WHY these matter: the capture hook demonstrably logged the same junk candidate
# 14 times — nothing ever told the session "there is a pile to distill." These
# lock in (1) a pending-candidates nudge, (2) a capacity nudge past 80% of the
# char budget (consolidation-by-constraint), (3) silence when there is nothing
# to do, so the nudge never becomes noise.
# ---------------------------------------------------------------------------

CANDIDATES_ONLY = """# Lessons — The Scar Log

## Entries

## Auto-captured candidates (review before trusting)

### candidate -- 2026-07-14 13:17 (session 0dc9ac)
**Trigger phrase (you said):** "junk junk junk"
**Action:** review, then promote or delete.

### candidate -- 2026-07-15 01:39 (session 392949)
**Trigger phrase (you said):** "more junk"
**Action:** review, then promote or delete.
"""


def _ctx(tmp_path, text):
    d = tmp_path / ".specify" / "memory"
    d.mkdir(parents=True)
    (d / "lessons.md").write_text(text, encoding="utf-8")
    out = lessons_injector.process({"cwd": str(tmp_path)})
    if out is None:
        return None
    return out["hookSpecificOutput"]["additionalContext"]


def test_pending_candidates_trigger_evolve_nudge(tmp_path):
    ctx = _ctx(tmp_path, LESSONS + "\n" + CANDIDATES_ONLY.split("## Entries", 1)[1])
    assert ctx is not None
    # LESSONS ships one candidate example of its own + my two -> 3 pending
    assert "[evolve]" in ctx and "3 unreviewed candidate" in ctx


def test_candidates_nudge_fires_even_without_confirmed_entries(tmp_path):
    """A pile of unreviewed candidates must surface even when no L-#/P-# exist yet —
    otherwise a brand-new project accumulates junk invisibly forever."""
    ctx = _ctx(tmp_path, CANDIDATES_ONLY)
    assert ctx is not None and "[evolve]" in ctx


def test_capacity_nudge_past_80_percent(tmp_path):
    filler = "x" * int(lessons_injector.LESSONS_CAP_CHARS * 0.85)
    ctx = _ctx(tmp_path, LESSONS + "\n" + filler)
    assert ctx is not None
    assert "budget" in ctx and "consolidate" in ctx


def test_no_nudge_when_clean_and_small(tmp_path):
    # LESSONS carries a candidate example by design, so strip the candidates
    # section to get a genuinely clean file for the silence check.
    clean = LESSONS.split("### candidate")[0]
    ctx = _ctx(tmp_path, clean)
    assert ctx is not None  # confirmed L-1 still injected
    assert "[evolve]" not in ctx
