# Gate behavior (gate modes)

## Gate modes (default is the safe one)

Autopilot supports three gate modes. The **default is `stop-at-every-step`** — the original v1
behavior. The relaxed modes are **opt-in**: use them ONLY when the owner explicitly asks (e.g. "run
autopilot in big-3 mode", "use auto mode", "don't stop at every step"). If the owner does not say,
stay in `stop-at-every-step`. State which mode is active when the run starts.

- **`stop-at-every-step`** (DEFAULT) — stop after every step and wait for an explicit "go". Never
  auto-advance. This is the safe default and the only mode unless the owner opts in.
- **`big-3`** — auto-advance through the small steps but STOP for approval at the three that matter:
  **spec** (after specify+clarify), **plan**, and **pre-PR checks**. Tasks and clarify flow through
  without a stop (still summarized). Good once the owner trusts the flow.
- **`auto`** — run the whole sequence end-to-end, stopping ONLY on an ambiguous reply, a needed
  clarification, or a failure. Most hands-off; use when the owner says so.

**In every mode, the hard rules still hold:** never advance on ambiguity, never skip a step, never
push/merge/deploy, fail loud. Relaxed modes change WHEN Autopilot stops for approval — never WHAT it
is allowed to do. A failure or ambiguity always forces a stop, regardless of mode.

## Classifying the owner's reply

**Advance (treat as "go")** — only on a clear affirmative with no new instruction:
`go`, `yes`, `y`, `next`, `continue`, `proceed`, `looks good`, `approved`, `lgtm`, `ship the step`.

**Revise (treat as "change") — stay on the same step:** any reply that asks for a different outcome:
`change …`, `no, …`, `redo …`, `instead …`, `can you make …`, `add …`, `remove …`, `not quite`,
`I'd rather …`. Apply the change to THIS step's artifact, re-summarize, STOP again. Do NOT advance.

**Ambiguous — ask ONE yes/no:** anything that is neither a clear affirmative nor a clear change
(`hmm`, `ok sure maybe`, `interesting`, a question about the result, silence-then-unrelated). Ask a
single confirmation question, e.g.:
> "Just to confirm — move on to **<next step>**, or change something here first? (go / change)"
Never guess-advance on ambiguity. Defaulting to "stay" is always safe.

## Missing prerequisite (out-of-order)

If `autopilot_state.py` returns a warning that a later artifact exists while an earlier step is
incomplete (e.g. `plan.md` present but `spec.md` missing), DO NOT skip. Tell the owner plainly which
earlier step must run first and offer to run it:
> "I found a plan but no spec — we need the spec first. Run specify now? (go / not yet)"

## Malformed or missing HANDOFF marker

If the `<!-- AUTOPILOT-STATE -->` block is missing or malformed, still proceed using the filesystem
(the helper already falls back). Recreate the block on the next HANDOFF update. Warn once, do not fail.

## Starting point

- New idea + no active feature (`.specify/feature.json` absent or its dir empty) → start at `specify`.
- Resume (no new idea given) → resume at `current` from the helper.

### New idea while another feature is mid-flight

If the owner gives a NEW idea but the active feature is **incomplete / mid-flight** (the helper's
`current` is not the terminal step and not all artifacts exist), do NOT silently switch and do NOT
silently resume the old one. STOP and offer the choice in plain English:

> "You're mid-flight on **<active feature>** (currently at: <current step>). Do you want to **finish**
> that first, or **park** it and start the new idea? (finish / park-and-start)"

- **finish** → resume the active feature at `current`.
- **park-and-start** → leave the parked feature's artifacts untouched (they stay on disk + in its
  branch; nothing is deleted), create a new feature branch for the new idea, point
  `.specify/feature.json` at the new feature dir, and start at `specify`. Note in the HANDOFF marker
  that the previous feature was parked at its step so it can be resumed later.

If the active feature is already COMPLETE (terminal step reached / all artifacts present), a new idea
just starts fresh at `specify` — no need to ask. Never mix two features' artifacts in one dir.

## Never

- Never advance two steps in one turn.
- Never advance on an ambiguous reply.
- Never push, merge, or deploy (see SKILL.md Refusals).
