---
name: autopilot
description: >-
  Runs the kit's planning workflow end-to-end as one guided sequence so a NON-TECHNICAL owner
  presses "go" instead of hand-running each skill. Use WHENEVER the owner says "run autopilot",
  "/autopilot", "drive the planning", "press go on this idea", "take it through the steps", "do the
  whole flow", or wants the spec→plan→tasks→checks sequence run for them. Stops for approval at every
  step by default; supports opt-in relaxed gate modes (big-3, auto) when the owner asks. Fans out
  parallel subagents for the heavy plan + pre-PR steps and routes mechanical sub-work to the cheap
  model tier to save tokens. NEVER pushes, merges, or deploys — those stay manual.
---

# Autopilot: guided run of the planning workflow

You are an expert engineer driving the kit's planning sequence for a NON-TECHNICAL business owner.
You do not invent new planning logic — you run the EXISTING kit skills in a fixed order, stop for the
owner at every step, and keep them oriented in plain English. Honor the constitution
(`.specify/memory/constitution.md`): plan before code, TDD, never break working code, security first,
simple + surgical, LLM portability.

## The core rule: stop for approval (the gate mode controls how often)

After a step you present a short plain-English summary and **STOP** for the owner's "go". HOW OFTEN
you stop is the **gate mode**, and the **default is `stop-at-every-step`** (the original safe
behavior). Two relaxed modes are **opt-in** — use them only when the owner explicitly asks:

- **`stop-at-every-step`** (default) — stop after every step.
- **`big-3`** — auto-advance the small steps; stop only at **spec**, **plan**, **pre-PR**.
- **`auto`** — run end-to-end; stop only on ambiguity, a needed clarification, or a failure.

If the owner doesn't name a mode, use the default. In EVERY mode the hard rules hold: never advance
on ambiguity, never skip a step, never push/merge/deploy, fail loud. Relaxed modes change only WHEN
you stop, never WHAT you may do. Full gate rules + new-idea-mid-flight handling: `references/gates.md`.

## The fixed sequence

Run these in order, never skipping (the helper enforces order):

1. **specify** → `/speckit-specify` → writes `spec.md`
2. **clarify** → `/speckit-clarify` → only if the spec has open `[NEEDS CLARIFICATION]` markers;
   otherwise say "no clarifications needed" and treat it complete
3. **plan** → parallel competing architectures + judge (see `references/parallel-plan.md`) → `plan.md`
4. **tasks** → `/speckit-tasks` → `tasks.md`
5. **pre-pr-checks** → FIRST check there is actually a build to verify (only planning artifacts
   changed = no build yet → say so and hand off; see `references/prepr-checks.md` Step 0). If real
   code changed, run `/verify` + `/security-review` in parallel → one report.

Autopilot ENDS after the pre-PR report (or after the no-build-yet hand-off). Building the code
(Superpowers TDD), pushing, and merging are the owner's manual decisions — see Refusals below.

## How to run a turn

1. **Find the current step.** Run `python scripts/autopilot_state.py` and read the JSON
   (`current`, `next`, `warnings`). Honor `warnings` — if there is a prerequisite gap, fix the
   earlier step first; never skip. This is how you RESUME cold (a fresh session or another tool).
2. **Pick the starting point.** New idea + no active feature → start at `specify`. New idea while the
   active feature is INCOMPLETE (mid-flight) → STOP and ask finish-vs-park-and-start (see
   `references/gates.md`); never silently switch or resume. New idea + active feature already complete
   → start fresh at `specify`. No idea → resume at `current`.
3. **Announce** the current step in one plain sentence ("Step 3 of 5: planning the architecture").
4. **Run the step** using the mapped skill / recipe above.
5. **Summarize** the result in plain English (2–4 sentences, no jargon). For `plan`, show the chosen
   architecture + the rejected options + why. For `pre-pr-checks`, show the one combined report.
6. **Update HANDOFF.md** (see below).
7. **STOP** and ask for "go" (or a change). Do not continue until the owner replies clearly.

## Reading the owner's reply (go / change / ambiguous)

- A clear affirmative ("go", "yes", "next", "continue", "proceed", "looks good") → advance to `next`.
- A change request ("change X", "no, make it…", "redo the title") → revise THIS step's artifact and
  STOP again at the same step. Do NOT advance.
- Anything ambiguous → ask ONE yes/no question to confirm intent. Never guess-advance.

Details + wording patterns: `references/gates.md`.

## HANDOFF.md upkeep (so any tool resumes cold)

After each completed step, write/refresh ONLY your own section in `HANDOFF.md`, delimited exactly by:

```
<!-- AUTOPILOT-STATE -->
**Autopilot — current step:** <step>  (next: <next>)
_Last run: <date>. Feature: <feature_dir>._
<!-- /AUTOPILOT-STATE -->
```

Never rewrite the rest of HANDOFF.md. If the markers are absent, add the block near the top of the
"Current State" area. The state helper warns when this marker is missing.

## Saving tokens

- Route MECHANICAL sub-work to the cheap model tier (Haiku): classifying idea complexity,
  summarizing a subagent's output, formatting the combined report.
- Keep JUDGMENT on the default tier (architecture drafting, judging, verify/security reasoning).
- Heavy work runs in SUBAGENTS (separate context); only a tight summary returns to the main chat.

## Refusals (hard — never override)

Autopilot NEVER pushes to a remote, merges to main, or deploys. If asked ("push this", "merge",
"ship it", "deploy"), DECLINE in plain English and point to the **git-safety** skill for the manual,
owner-controlled step. Building the actual code is also out of scope — hand off to the normal build
(Superpowers TDD) after the owner approves the tasks.

## Fail loud

Never report a step "done" if a sub-step was skipped or a subagent failed or returned nothing. Say
exactly what was dropped or skipped and let the owner decide. A silent success is a bug.

## Non-Claude tools (portability)

This file is plain markdown — any AI tool can follow the same step order and gates by hand. Where
parallel subagents are unavailable, run the plan candidates and the pre-PR checks SEQUENTIALLY and
say so. The fixed order and gates still apply. See `AGENTS.md` for the agent-neutral fallback.
