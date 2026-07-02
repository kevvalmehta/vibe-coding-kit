# How to Use This Kit — Walked Through with a Real Example

**The app:** "GoodStreak" — people share one good deed a day, earn a streak.

**The one rule that makes everything work:** you never say "build me the app." You walk stages, and each stage hands a *verified artifact* (a file that exists and passed a check) to the next. The kit refuses to skip — that's a feature.

## Stage 0 — The front door (5 min)
Open Claude Code in an empty `GoodStreak/` folder and type **`/start`**. The Conductor reads where you are (nothing exists yet) and drives you through everything below, one stage at a time. Lost at ANY point later? Type **`/guide`** — it tells you the single next step. You never need to memorize this guide.

## Stage 1 — Is it worth building? (30-60 min) — `/discover`
Before any code: *"discover: an app where people share one good deed a day and keep a streak."* It grills you (who is this for? what do they do today instead?), then mines what real people say — Reddit threads about habit apps, reviews of streak apps people already pay for — and scores whether the need is underserved. You get a `discovery/` note with a verdict, a V1 cut (maybe: photo + one-line deed, daily streak, friends feed — and NOT comments, DMs, leaderboards), and your first 10 users. **This stage kills bad ideas for the price of a coffee instead of a month of building.**

## Stage 2 — Pressure-test + pick the stack (30 min) — `/grill-me`, `/stack`
**`/grill-me`** interrogates the plan one question at a time ("What happens to a streak at midnight in a different timezone?" — the questions that hurt later). Then **`/stack`** recommends boring, proven tech with costs: for a social app, likely Next.js (the web framework) + Supabase (the database with *Row-Level Security* — rules in the database itself so user A physically can't read user B's data) + Vercel (hosting with free preview URLs). You pick; it records why.

## Stage 3 — Plan on paper (1-2 hrs) — the `/speckit-*` chain or `/autopilot`
Type *"use autopilot"* and it runs the planning chain, stopping for your approval at each step:
- **`/speckit-specify`** — WHAT and WHY: a spec (a plain-English contract of what "done" means — "a user can post one deed per day; the streak increments only on consecutive days...").
- **`/speckit-clarify`** — asks up to 5 targeted questions about the fuzzy parts (the timezone thing surfaces here if grilling missed it).
- **`/speckit-plan`** — HOW: architecture, database tables, and the **security six-check** fires here (rate limiting? what happens when someone scripts 1,000 fake deeds?).
- **`/speckit-tasks`** — the plan chopped into small, individually testable steps.
- **`/speckit-analyze`** — consistency check across all three documents.

If you add an AI feature ("AI verifies the deed photo looks genuine") this is where **`agent-architect`** designs it and **`docs/ai-feature-checklist.md`** gets walked. No AI inside → skip both.

## Stage 4 — Build (days, mostly the AI working) — `/scaffold` then `/ship`
**`/scaffold`** writes the runnable starter (folder structure, `.env.example`, hello-world page). Then **`/ship`** drives the build task-by-task: writes a failing test, writes code to pass it, repeats. This is where your new enforcement layer earns its keep, silently, hundreds of times:
- **TDD-Guard** blocks any code written without a failing test first (now on by default).
- **Import reality check** catches an invented package the moment it's typed.
- **Done-claim verifier** blocks "tests pass" unless tests actually ran.
- **Lessons injector** keeps every past correction applied — even in a fresh session next week.

Your job here is small: review what each task produced, approve, continue.

## Stage 5 — The gauntlet before merge (automatic) — git-safety + CI
All work happened on a *branch* (a parallel copy — `main` stayed untouched and working). Pushing opens a *PR* (a proposed merge that must pass checks). GitHub then runs the gates you watched work today: full test suite, Semgrep security scan (blocking), dependency vulnerability audit (blocking), lint, and the plan gate (every task checked off, or no merge). Red → the AI fixes → green → merge.

## Stage 6 — Going live (an afternoon) — Vercel + the deploy escalation
Vercel gives a **preview URL** first — you click around GoodStreak like a real user before anything is public. When you say "make it live for everyone," **git-safety's public-deploy escalation fires** and walks two documents with you:
- `security-six-check.md` leftovers — it offers to build *attack tests* (hit login 1,000× → assert blocked; try to read another user's streak → assert denied).
- `production-readiness.md` — Sentry wired (you get an email when the app crashes for a user), backups exist and a restore was tested once, a 15-second load burst on the feed endpoint, alt-text/contrast/keyboard basics.
Each item: do it, or consciously decline and it's logged. Then deploy.

## Stage 7 — Living with it (ongoing)
- Crash appears in Sentry → *"fix: streak resets wrongly at midnight UTC"* → **`/safe-change`** maps what the fix touches, writes a regression test, fixes surgically, full suite proves nothing else broke.
- New feature → back to Stage 3 with a new spec. Never "just add it."
- **`/health`** monthly for a 0-100 score; **`/audit`** when you want a deep "what's worth fixing" list; **`/lean-debt`** to review shortcuts you took on purpose; **`/monitor`** if the AI-photo-check feature exists (catches its quality drifting).

## The shape to remember
**Validate → plan → build-with-gates → merge-through-CI → preview → escalated deploy → monitored life.** Every arrow is a skill, every skill leaves a file, and the hooks police the whole thing whether or not anyone remembers to ask. Type `/start` and the kit walks you through it.
