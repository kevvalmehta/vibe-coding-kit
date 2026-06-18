---
name: goal
description: >-
  Turn a vague or messy request into a clear, executable "task contract" before any building
  starts — outcome, concrete verification evidence, constraints, write boundaries, an iteration
  policy, a done-when line, and explicit pause/stop conditions for risky work. Use when a request
  is fuzzy ("make me an app", "fix this", "make it look professional"), when you want guardrails
  on what the agent may touch and when it must stop and ask, or when the user says "write a goal",
  "/goal", or "turn this into a goal". A lightweight FRONT DOOR — it does NOT start the build, and
  for anything substantial it routes into /speckit-specify.
argument-hint: "The rough request to turn into a goal (e.g. 'a booking app that looks professional')"
user-invocable: true
disable-model-invocation: false
---

# Goal: turn a vague ask into an executable task contract

> Original to this kit. Inspired by the *idea* behind qiaomu-goal-meta-skill (MIT) — specifically
> its insistence on real verification evidence and explicit stop/pause conditions — but rebuilt
> tool-agnostic and wired into this project's pipeline. We did **not** install that repo.

## User Input

```text
$ARGUMENTS
```

Treat the input above as the rough request to convert into a task contract. If it's empty, ask the
user for the one-line request first.

Most agent tasks fail not because the model can't code, but because the goal was too loose from
the start: "make it nicer", "build me an app", "fix the bug". Those mean something to a human but
leave an agent without the four things it actually needs: how to verify it's done, what it must
not touch, how to recover when a step fails, and when it must stop and ask a human.

This skill takes the messy request and hands back a **task contract**: a short, plain-English
block that makes the work executable and safe. It defaults to a recommended version you can use
immediately — it does not make the user fill out a form first.

## Fit with this project
- This is the **front door**, used at the very start (before or as the opening move of
  brainstorm / `/speckit-specify`). The user is non-technical: keep it plain, lead with a
  recommended version, explain choices in one line.
- It honors the constitution: **Plan before code** (a goal is planning, never the build),
  **Security first** (risky work goes into pause conditions), **Simple & surgical** (write
  boundaries keep the agent in its lane), and **verification with proof** (mirrors `/verify`).
- **One source of truth.** The goal does not replace the spec. For anything substantial it ends
  by pointing at `/speckit-specify`; only small, self-contained jobs (a bug fix, a tiny script,
  a Chrome extension) are run straight from the contract.

## How to respond (default-first, never a form)

1. **Lead with a recommended, copy-ready contract.** Pick conservative defaults, fill in every
   field, no placeholders. The user can run it as-is.
2. **Add one line of reasoning** — why you chose those defaults, in a single sentence.
3. **Offer numbered options** for the few choices that actually matter, so the user can reply
   "use defaults" or "1B 2A" instead of writing prose.
4. **End with the next step** — `/speckit-specify` for substantial work, or "this is small enough
   to run directly" for tiny jobs.

## The task contract (the seven fields)

```
Outcome:        One sentence — what exists and works when this is done. Concrete, not "nicer".
Verification:   The PROOF it works — specific commands to run, logs to read, a screenshot to take,
                a test that passes, a file that appears. Never "make sure it works".
Constraints:    What must NOT happen — no fabricated facts, no copyrighted assets, no new login/
                backend/paid API in v1, no real user data, etc.
Boundaries:     Which files/areas the agent may write to. Never "edit anything" — name the lane.
Iteration:      How to recover on failure, and a hard cap (e.g. "read the error log first; at most
                3 focused rounds") so it can't loop forever.
Done when:      The finish line — every verification step passes, or the missing piece is named.
Pause / Stop:   The high-risk triggers where the agent must stop and ask a human (see below).
```

## Built-in principles

**Default forward on low risk.** Don't stop the user to fill in blanks for low-stakes unknowns.
State a clear assumption and pick the best default.

**Stop on high risk.** These ALWAYS go into the Pause/Stop line — the agent must stop and ask:
- credentials, accounts, passwords, payment
- production data, or any destructive / irreversible operation
- legal, medical, financial, or other regulated judgment
- copyrighted assets or official trademarks/IP
- publishing, real deployment, or pushing/merging to `main`
- unclear ownership or product direction

**Discover-first in unfamiliar domains.** Don't pretend to know a specialist field (medical,
finance, compliance, niche data). Write a "discovery-first" goal: read the project docs, sample
data, and existing scripts first; list working assumptions; then build one verifiable slice.

**Don't delete fuzzy words — translate them into verification.** "Professional", "polished",
"like a real site" aren't bad goals, they're bad *finish lines*. Turn them into a design
direction plus a screenshot check (hierarchy, spacing, type, readability) and a cap of ~3 focused
visual rounds.

## Worked example

User says: *"make me a booking app, make it look professional"*

```
Outcome:      A working v1 web app where a visitor picks a service, picks an open time slot, enters
              name + email, and gets an on-screen confirmation; bookings are saved and visible to me.
Verification: Start the app locally; in the browser complete one booking end-to-end (pick service →
              pick slot → submit → see confirmation); reopen the app and confirm the booking is still
              listed; take a screenshot of the confirmation. Run the test suite — all green.
Constraints:  v1 has no login, no payments, no email-sending, no real customer data. No copyrighted
              logos, fonts, or images. Don't invent business rules — ask if a rule is unclear.
Boundaries:   Only the booking UI, the booking data store, styling, and their tests. Don't touch
              unrelated modules, CI config, or secrets.
Iteration:    Build the core booking flow first, then styling. On any runtime/browser error, read the
              console log before changing code. At most 3 focused rounds on look-and-feel.
Done when:    A booking can be made, saved, and re-seen; tests pass (or the missing piece is named);
              desktop + mobile layouts checked, no broken layout.
Pause / Stop: Stop and ask before adding accounts, payments, sending real email, using anyone's brand
              assets, deploying live, or handling real customer data.

Default reasoning: kept v1 to "browse → book → confirm" with no auth/payments, because that proves
the core value fastest and avoids the riskiest, slowest parts.

Options:
  1. Storage:    A) local file/SQLite (default)   B) Supabase from day one
  2. Look:       A) clean minimal (default)        B) match an existing brand
  3. v1 scope:   A) single service (default)       B) multiple services + staff
Reply "use defaults" or e.g. "1B 2A".

Next: this is substantial → run /speckit-specify to turn this contract into a full spec.
```

## Check it (optional)
Run the linter to catch weak verification, placeholders, and unbounded permissions:
```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/lint-goal.py" goal.txt
```
It flags (it does not fix): vague verification like "make sure it works", leftover placeholders
like `[outcome]`/`TODO`/`TBD`, unbounded boundaries like "edit anything", and infinite-retry
language like "keep trying". In the spirit of Gate 1 — the script decides, not the agent's word.

## Boundaries of this skill
- It produces a task contract; it does **not** run the build itself.
- It never writes around credentials, payments, production data, copyright, or regulated judgment —
  those go into the Pause/Stop line.
- It defaults to MVP-level goals; full product strategy, monetization, and deployment need an
  explicit ask (and the `/speckit-*` pipeline).
