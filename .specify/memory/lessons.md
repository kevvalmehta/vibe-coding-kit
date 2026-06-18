# Lessons — The Scar Log

The constitution holds the **rules**. This file holds the **scars**: the real times a
rule got broken, what went wrong, and the quick check that stops it happening again.

**Why this file exists:** a bare rule ("don't do X") gets ignored. A rule with a real
mistake attached gets obeyed. "Don't touch the stove" is weak. "Don't touch the stove —
last June someone did, third-degree burn" is not. Every entry below is a stove someone
already touched.

**For the AI agent (read before you finish any task):**
1. Read every entry below.
2. Run each **Self-check** against the work you are about to deliver.
3. If a check fails, fix it before you say "done." Do not deliver and hope.

**For the owner:** when the AI (any tool — Claude, Codex, Cursor) makes a mistake worth
never repeating, add a new entry using the template. Over time this file teaches every
future session what already went wrong here. When a scar matters enough to be a law,
promote it into `constitution.md` and link back to the entry here.

---

## The template (copy this for every new entry)

```
### L-{number} — {short name of the rule in plain English}

**Rule:** {what to do or never do, one sentence.}

**What broke:** {date} — {what actually happened, plainly. The real mistake, not a
theory. Name the project/file if it helps.}

**Why it cost us:** {the damage — wasted time, broken build, confusion, duplicate work.}

**Self-check (run before saying "done"):** {a tiny, concrete look-before-you-send step.
Should be answerable yes/no in seconds.}

**Linked rule:** {which constitution principle / quality gate this backs, if any.}
```

---

## The template for a GOOD habit worth keeping (copy this for a pattern entry)

A scar is a mistake to never repeat. A **pattern** is the opposite: a good way of doing
something, discovered once, worth reaching for again. Scars use **L-#**; patterns use
**P-#**. Both live in the Entries section below.

```
### P-{number} — {short name of the practice in plain English}

**Practice:** {what to do, one sentence.}

**Context:** {when this came up — the situation that made it worth keeping.}

**Why it matters:** {the payoff — what it saves or prevents next time.}

**When to apply:** {the trigger — when a future session should reach for this.}

**Linked rule:** {which constitution principle / quality gate this supports, if any.}
```

---

## Entries

### L-1 — One source of truth: never add a tool that duplicates an existing one

**Rule:** Before adding any new tool, skill, or engine, check whether something already
installed does the same job. If yes, do not add it — pick one and remove the other.

**What broke:** 2026-06-06 — TaskMaster (global `task-master-ai` npm package + the
`prd-taskmaster` skill) had been installed for planning. But GitHub Spec Kit already does
planning. Two tools, same job. They overlapped and competed to be "the planner."

**Why it cost us:** confusion about which planning flow was real, two sets of templates
to keep in sync, and time spent untangling and uninstalling TaskMaster to get back to one
source of truth.

**Self-check (run before saying "done"):** about to install or adopt a tool/skill? Ask:
"Does Spec Kit, Superpowers, or an existing skill already do this?" If yes — stop, don't
add it, or replace the old one and say so.

**Linked rule:** Principle V (Simplicity & Surgical) + HANDOFF "one source of truth = Spec Kit".

---

### L-2 — EXAMPLE ONLY (delete me once you log a real scar)

**Rule:** Never say "done" while a step was silently skipped or a test was disabled.

**What broke:** {This is a placeholder showing the format. It has not happened in this
project. Replace it with a real mistake, or delete this whole entry.}

**Why it cost us:** {—}

**Self-check (run before saying "done"):** did I run the FULL test suite and a security
check, and did every Quality Gate in the constitution actually pass? If I skipped any,
say which — out loud — instead of claiming success.

**Linked rule:** Quality Gates 1-6 + global Rule 12 (Fail Loud).

---

## Candidate lessons (auto-captured -- review, then promote to an L-# entry or delete)

<!-- The learning hook (scripts/capture-lessons.ps1) appends suspects here when it
     sees you correct the AI or state a rule. These are NOT confirmed lessons.
     To confirm one: FIRST search this file for an entry on the same topic — if one
     already exists, update that entry instead of adding a duplicate (L-1: one source
     of truth). Otherwise write it up as a new L-# (scar) or P-# (good habit) entry
     above, then delete it from this candidates list. -->

_Queue empty — last reviewed 2026-06-14. Three auto-captured candidates cleared after review: a
git-learning question, a skill-invocation capture, and a revert-safety value — none a new scar or
pattern (the revert-safety value is already covered by the `git-safety` skill + the constitution's
Version Control & Recovery rules; promoting it would duplicate, L-1)._

