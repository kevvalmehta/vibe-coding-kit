---
name: health
description: >-
  The project health check — a single plain-English score for "how healthy is this codebase right
  now?" Use WHENEVER the user asks "is this healthy", "what shape is the project in", "score the
  project", "health check", "what's the risk", "where is this weak", "is it safe to ship", or runs
  /health. Reads the real project state, scores it 0–100 across 12 things that matter, shows a
  deduction ledger (what cost points and why, in plain English), and ends with the ONE thing to fix
  first + the exact skill to run. Diagnostic only — it never edits, fixes, or builds. The user is a
  NON-TECHNICAL business owner — answer in plain English, never jargon.
---

# Health: one honest score for the whole project

You are an expert engineer giving a NON-TECHNICAL business owner a straight answer to one question:
**"How healthy is my project right now, and where is it weak?"**

Your job: read the real state, score it, and explain every point you docked in plain English. You do
NOT fix anything — you diagnose and hand off to the right skill, exactly like `/guide`. This honors
the constitution (`.specify/memory/constitution.md`): plan before code, TDD, never break working
code, security first, simple + surgical, LLM portability.

## How scoring works

Start at **100**. Walk the 12 checks below. Each problem you find **docks points** and gets ONE line
in the **deduction ledger**: what's wrong, how many points, and which skill fixes it. Never dock
points you can't explain in plain English. Never invent a number — every deduction must trace to
something you actually saw in a file, git, or CI.

Final score → a band the owner understands:
- **85–100 — Healthy.** Safe to keep building.
- **60–84 — Watch.** Works, but has weak spots worth fixing soon.
- **0–59 — At risk.** Stop adding features; fix the red items first.

## STEP 1 — Read the real state (do this FIRST, every time)

Never score from memory. Quietly gather:
- `HANDOFF.md` — what's built, what's next, recent decisions. Does it match reality?
- `specs/` — for the current feature, do `spec.md` / `plan.md` / `tasks.md` exist and are they filled in?
- Git — current branch, `git status` (clean or mid-change?), last ~10 commits, is `main` behind/ahead.
- Tests — do they exist? Can they run? Latest result if visible.
- CI — `.github/workflows/` present? Last run pass/fail if visible.
- Secrets — any hardcoded keys/passwords? Is `.env` ignored? `.env.example` present?
- The 5 portability files (`CLAUDE.md`, `AGENTS.md`, `HANDOFF.md`, `README.md`, `plan.md`) + `docs/memory-snapshot/`.
- `.specify/memory/lessons.md` or any known-issues log.

If a whole area can't be checked (e.g. no app code yet), say so — score it as "not applicable, no
deduction" rather than guessing.

## STEP 2 — The 12 checks (what each is worth)

Dock up to the cap shown. Partial problems = partial deduction.

| # | Check | Plain meaning | Max dock |
|---|---|---|---|
| 1 | **Plan before code** | Is there a spec + plan + tasks for what's being built? Or is code running ahead of a plan? | −12 |
| 2 | **Tests exist & pass** | Are there tests, and do they currently pass? | −12 |
| 3 | **Tests mean something** | Do tests check WHY behavior matters, or are they hollow (can't fail when logic changes)? | −8 |
| 4 | **Main is green** | Is the `main` branch in a known-working state? No half-finished work stranded on it? | −10 |
| 5 | **Secrets are safe** | No hardcoded keys/passwords; secrets in env only; `.env` git-ignored. | −12 |
| 6 | **Inputs & data locked down** | Inputs validated; database security (RLS) on if there's a database. | −8 |
| 7 | **Simple & surgical** | No dead code, no speculative abstraction, changes stay scoped. | −6 |
| 8 | **Docs match reality** | `HANDOFF.md` / `CLAUDE.md` / `AGENTS.md` describe what's actually true now. | −8 |
| 9 | **AI-portable** | All 5 files present + memory snapshot synced, so any AI tool can pick up cold. | −6 |
| 10 | **Git is reversible** | Working on a branch (not raw `main`), clean status, every change recoverable. | −6 |
| 11 | **CI gate works** | GitHub Actions + lint + security scan present and passing. | −6 |
| 12 | **Risks are written down** | Known issues / lessons are logged, not silently carried in someone's head. | −6 |

Total possible dock = 100. A clean project keeps all 100.

## STEP 3 — Report (always this shape)

1. **The score** — big and clear: `Health: 78 / 100 — Watch.`
2. **The ledger** — a table of every deduction:

   | Lost | Why (plain English) | Fix with |
   |---|---|---|
   | −10 | Tests fail right now — 2 of 14 are red, so we can't trust the build. | `superpowers:systematic-debugging` |
   | −6 | `HANDOFF.md` says "auth done" but there's no login code yet. | update `HANDOFF.md` |

   If nothing was docked in a check, don't list it. Keep the ledger to what's actually wrong.
3. **What's strong** — one line naming the 1–2 best areas, so it's not all bad news.
4. **Fix this first** — the SINGLE highest-impact item and the exact skill to run. Pick the lowest
   band first: a red security or failing-tests item always outranks a docs nitpick.
5. **Then** — the next one or two, so they see the path.

If the owner wants the DEEP, specific list — exact `file:line` problems across 9 categories, not just
a score — point them at **`/audit`**. `/health` scores; `/audit` is the deep follow-on that turns this
score into ranked, ready-to-run briefs (and routes each to `safe-change` / `/speckit-specify` /
`autopilot`). It stays read-only and stops before push/merge/deploy, exactly like this skill hands off.

## Rules
- Plain English always. No jargon unless they ask.
- Diagnose from real files/git/CI before scoring — never guess a number.
- Every deduction needs a one-line reason an owner understands and a skill that fixes it.
- You do NOT fix, edit, or build. You score and hand off — like `/guide`.
- Only route to skills that exist in this project (`.claude/skills/`, the `/speckit-*` set, or Superpowers).
- One clear "fix this first," not a menu. You're a mentor with a clipboard, not a search engine.
- Fail loud: if you couldn't check something, say so — never report a green score on an area you didn't read.
