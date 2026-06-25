---
name: monitor
description: Live post-launch monitoring (Conductor v5) — after an AI app is deployed, keep watching its AI output for DRIFT (getting worse over time) by sampling recent real outputs, grading them against the same agent-eval rubric, and alerting if quality drops below the bar. Use WHENEVER the owner has a LIVE app with an AI feature and says "monitor the AI", "is the AI still good", "watch for drift", "/monitor", "set up monitoring", "check the live output", or asks what to do after launch to keep the AI honest. It reuses agent-eval's tested runner (no new judge) via scripts/monitor_sample.py, and documents the switch-on recipe (Supabase log table + scheduled job + alert). HONEST BOUNDARY: the live log + schedule need a DEPLOYED app — if there's no app live yet, it says so and points to the recipe, never pretends to monitor. The user is a NON-TECHNICAL business owner — plain English, define every term, "make sense?" checks.
---

# /monitor — keep the AI good after launch (Conductor v5)

The owner is a **non-technical business owner**. This is the **after-launch** check. `/agent-eval` and
`/ship` prove the AI is good *when you build it*; `/monitor` answers: *once real people are using it, is
the AI's output still good — or is it drifting?* *Drift = the AI's answers slowly getting worse* (a
model update, changing user questions, a prompt that no longer fits). Define every term; "make sense?".

**Honest boundary first:** you can only watch an app that's actually **live** (deployed, real users).
If there's no deployed app yet, say so plainly and point to the recipe below for when there is —
**never pretend to monitor** something that isn't running (Principle VII). There's nothing wrong with
"not yet" — it just means this is a switch-on step for later.

It **reuses `agent-eval`** — the same rubric and judge you already set up at build time become the
standard for the live check (one source of truth). No new judge engine.

## What's ready now vs what you switch on at deploy

**Ready now (tested):** `scripts/monitor_sample.py` — hand it a batch of recent logged outputs + your
rubric, and it grades them and reports a **drift verdict**: *OK* (still meets the bar) or *DRIFT
DETECTED* (dropped below it, with the failing cases named). It fails loud on any judge error — never a
false "all good."

**Switch on when the app is live (the recipe):**
1. **Log table (Supabase):** every time your AI answers, save a row — the user's input + the AI's
   output (a *table* = a spreadsheet-like store; *Supabase* = your hosted database). Turn on
   row-level security so only you can read it.
2. **Scheduled job (cron):** a task that runs on a timer — *cron = a clock-based scheduler*. Use
   GitHub Actions (free) to, say, once a day: pull a sample of recent rows → write them to a
   `records.json` → run `python scripts/monitor_sample.py records.json eval-config.json`.
3. **Alert:** if the run prints **DRIFT DETECTED** (exit shows failing cases), have the job email/ping
   you. That's your "go look at the AI" signal.

Walk the owner through wiring these against THEIR app + Supabase when they deploy — it's about a
one-session job at that point, not something pre-built here.

## Optional: the LLM-judge can also double-check `/ship`'s fixes

The same judge can read a `/ship` fix and flag reward-hacking the deterministic diff-check might miss
(the heavier anti-cheat layer mentioned in `/ship`). This is **optional** — `/ship`'s built-in
diff-check (test files read-only, reject hardcoded/skipped tests) already covers the common case. Offer
it only when the owner wants belt-and-suspenders on a high-stakes change.

## Hard rules
- **Plain English, every term defined**; "make sense?" checks.
- **Never monitor a non-deployed app** — say "not live yet" + give the recipe (Principle VII).
- **Reuse `agent-eval`** — same rubric/judge, one source of truth; no second judge engine.
- **Fail loud** — a grading error is exit 2, never a false "all good."
- It **never** pushes/merges/deploys; setting up the live wiring stays the owner's call.

## For non-Claude agents
Plain procedure — to grade a batch now: `python scripts/monitor_sample.py <records.json> <config.json>`
(reuses agent-eval's `eval_runner`). The live log + scheduled job are the deploy-time recipe above.
Nothing here is Claude-only.
