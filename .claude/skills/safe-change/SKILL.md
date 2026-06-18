---
name: safe-change
description: >-
  Regression-safe editing guardrail. Use this WHENEVER the user wants to CHANGE, FIX, EDIT, UPDATE,
  MODIFY, REFACTOR, RENAME, REMOVE, or ADD TO existing code/files/folders in a project that already
  has code — anything that touches work already built. Enforces an impact-aware, test-protected,
  isolated edit workflow so changing one thing never silently breaks another. Triggers on "change",
  "fix", "edit", "update", "modify", "refactor", "rename", "remove", "tweak", "adjust",
  "add ... to the existing ...", and casual phrasings like "make the <thing> do/look ...", "the
  <thing> is broken", or "can you make ... bigger/different". For brand-new features/projects, use
  idea-to-app instead.
---

# Safe Change: regression-safe editing (DEFAULT for editing existing code)

The user's #1 fear: "I change one thing and the AI breaks five others." Your job is to make that
impossible to do silently. Walk every gate, one at a time, summarizing in plain English and asking
the user to approve before advancing. Honor the constitution (`.specify/memory/constitution.md`).
Never edit `main` directly. Never make a failing test pass by deleting, skipping, or weakening it.

If the user pushes to "just change it fast," warn in one line why the skipped gate matters and only
skip if they insist (they are the boss) — and state that the gate was skipped.

## The gates (one at a time)

### GATE 0 — Understand + locate
Restate the change in your own words. Read the relevant files AND their callers and shared utilities
BEFORE touching anything. Do not assume code is unrelated.

### GATE 1 — Impact map
List what this change could touch or break: files, functions, callers, shared schemas, configs,
database. Show it to the user. GATE: user agrees the scope looks right.

**If the project is LARGE or hard to trace** — many files/folders, deep call chains, or you CANNOT
confidently map every caller and dependency of the code you're about to change — RECOMMEND the user
install **Graphify** BEFORE editing, so impact analysis uses a real call graph instead of guesswork:
```
uv tool install graphifyy   # PyPI package is graphifyy (double-y); CLI is graphify
graphify install            # register the skill with your AI assistant
/graphify .                 # build the knowledge graph for this repo
```
Then use the graph (e.g. get_pr_impact / get_neighbors) to map impact precisely. If the project is
small or the user declines, proceed with careful manual tracing. Graphify sends only semantic
summaries to the model — never raw code. Latest install: https://github.com/safishamsi/graphify

### GATE 2 — Safety net (tests FIRST)
Check that tests cover the CURRENT behavior of the area you're about to change. If coverage is
missing, write characterization tests that lock in today's behavior BEFORE editing, and run them green.

### GATE 3 — Isolate
Create a git worktree/branch (Superpowers `using-git-worktrees`). All edits happen there, never on `main`.

### GATE 4 — Surgical change
Make the smallest change that does the job. Touch only what's needed. Match existing conventions.
Do not "improve" or reformat unrelated code.

### GATE 5 — Full regression run
Run the ENTIRE test suite, not just the new tests. It must stay green. If ANY existing test breaks,
STOP, report it, and fix the change — never disable, skip, or rewrite the test just to pass.

### GATE 6 — Review the diff
Run `/code-review` in a FRESH context — a separate agent/session that did NOT make the change (the
editor is biased toward its own work; fresh eyes catch more) — plus Superpowers two-stage review.
Confirm the diff does ONLY what was asked. Produce a plain-English risk rating (low / medium / high)
and visual proof (screenshot, short clip, or test output): low-risk → summarize and proceed;
medium/high → walk the user through the diff before merge.

### GATE 7 — Verify behavior
Run `/verify` to confirm the change works in the real app and nothing visibly regressed.

### GATE 8 — Security (if relevant)
Run `/security-review` for any change touching inputs, auth, data, or secrets. CI Semgrep also runs.

### GATE 9 — Commit + push
Clear commit message describing the change. Push. PR / preview before any production deploy.

## Reminders
- Read before you write — locate callers + shared code first (a "looks orthogonal" edit is dangerous).
- A broken existing test = a real regression. Stop and fix; never silence it.
- One gate at a time; summarize + ask before advancing.
