# Token Quick-Wins — cheaper sessions, same quality

Six habits that lower the token cost of every session **without changing what gets built** or the
quality of the planning workflow. Most are already on or automatic — you act on only a couple.

**How to read each win:** *What it is · When it helps · What you do · Status · Non-Claude fallback.*

- **Status: already-in-place** = the kit already does this; nothing to set up.
- **Status: new habit** = a habit worth adopting (small, manual).

These wins are tool-portable: where a win relies on a Claude Code command, a plain fallback is given
so Codex / Cursor / Gemini get the same benefit.

---

## Win 1 — Route mechanical work to the cheap model (Haiku)

- **What it is:** send grunt sub-work — classifying, summarizing a subagent's output, formatting a
  report — to the cheap Haiku tier. Judgment work (architecture, decisions, security reasoning) stays
  on the default tier, so quality does not change.
- **When it helps:** any task with a mechanical sub-step; especially multi-step flows.
- **What you do:** nothing — it is built into how the kit fans out work.
- **Status: already-in-place.** Autopilot already routes mechanical sub-work (complexity
  classification, plan-summary formatting, the combined report) to Haiku while keeping drafting and
  judging on the default tier.
- **Non-Claude fallback:** for grunt sub-tasks, pick the cheaper model manually before starting them;
  keep the premium model for the thinking.

## Win 2 — Compact context at natural breakpoints

- **What it is:** `/compact` squeezes the running history so a long session stops dragging a huge,
  expensive context along.
- **When it helps:** at a clean breakpoint — a step finished, a decision made — before the chat grows
  bloated.
- **What you do:** type `/compact` when you finish a chunk of work and are about to start the next.
- **Status: existing Claude command** (no setup).
- **Non-Claude fallback:** paste a 3-sentence summary of where things stand into a fresh thread and
  carry on there.

## Win 3 — Recap on resume

- **What it is:** `/recap` gives a quick state summary when you pick a session back up, so you orient
  without re-reading the whole history.
- **When it helps:** every time you resume cold.
- **What you do:** run `/recap` first thing when returning to a session.
- **Status: existing Claude command** (no setup).
- **Non-Claude fallback:** paste the opening of `HANDOFF.md` into the new thread — it is the kit's
  cross-tool state-of-play.

## Win 4 — Scope-bound prompts

- **What it is:** name only the files / scope the task needs, so the assistant does not read or reason
  over the whole project. Fewer tokens in, tighter answers out.
- **When it helps:** any focused change — far cheaper than an open-ended "look at the app and…".
- **What you do:** copy this template and fill the blanks:

  ```
  Goal: <one sentence — what done looks like>
  Touch only: <file(s) / folder — nothing else>
  Do not change: <areas that must stay as-is>
  Done when: <objective check — a test passes / the screen shows X>
  ```

- **Status: new habit** (just how you phrase a request).
- **Non-Claude fallback:** none needed — it is plain text, works in any tool.

## Win 5 — Caveman mode for compressed output

- **What it is:** caveman mode makes replies ultra-terse (drops filler, articles, pleasantries) to cut
  output tokens, keeping the technical substance.
- **When it helps:** working sessions where you want answers, not prose. Off for anything you will
  read carefully or share.
- **What you do:** toggle with `/caveman` (levels: `lite` / `full` / `ultra`); say "stop caveman" to
  return to normal.
- **Status: already-in-place** (installed in this kit).
- **Non-Claude fallback:** ask the tool to "answer in bullets only, no preamble."

## Win 6 — Prompt caching on system prompts

- **What it is:** when you build an app that *contains* AI, mark the big, unchanging system prompt as
  cached so you are not re-billed full price for it on every call.
- **When it helps:** any AI feature with a stable system prompt (the common case).
- **What you do:** make system-prompt caching the default when designing an AI feature — see the
  AI-feature checklist.
- **Status: new default** for AI features built with the kit.
- **Non-Claude fallback:** this is a model-API setting (the `cache_control` block on the system
  prompt), not a Claude Code feature — it applies wherever you call the model.

---

## Where this fits

These are habits and defaults, not a step in the build. They run alongside the normal workflow — see
`SKILL-MAP.md` for the full map of skills and when to use them, and `docs/ai-feature-checklist.md`
for Win 6 in the AI-feature context.
