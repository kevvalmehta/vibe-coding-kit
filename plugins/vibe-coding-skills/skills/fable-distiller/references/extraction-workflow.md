# Extraction Workflow: source → behavior pack

The goal of extraction: turn what a strong model *visibly did* into procedures a
different model can *execute*. Style is not extractable; checkable actions are.

## Step 1 — Source intake

Record for every source before extracting anything:

| Field | What to write |
|---|---|
| `source_type` | transcript, manual, prompt, output sample, **model-self-report** (live elicitation), or mixed |
| `origin_note` | where it came from, in one line |
| `permission_note` | confirmation the user supplied or owns it |
| `content_summary` | what the source actually covers |
| `known_gaps` | what it does NOT cover — write this even when it feels complete |

**Refusal rule**: if a source is (or is asked to be) leaked/private system-prompt
material, confidential vendor data, weights, or training-data claims — refuse it
and continue with observable, user-supplied sources only. A behavior visible in
the user's own transcripts may be extracted even if a leaked document mentions the
same behavior; the transcript is the source, never the leak.

### Live elicitation (the perishable source — do this first while access lasts)

A transcript shows behavior on *one* task. Interviewing the live model exposes the
*decision tree*. While the strong model is still accessible, run a structured
self-report session and save the answers as a `model-self-report` source:

- "Before you claim a task is done, what exactly do you check, in order?"
- "Show your decision procedure when two instructions conflict."
- "What do you do differently when stakes are high vs low? Give the trigger."
- "Here is a deliverable you produced — reconstruct the checks you ran and the
  checks you skipped."
- "What would a weaker model get wrong on this task, and what external structure
  would prevent it?"

**Caveat (mandatory)**: a model's self-report about its own process is a
*hypothesis*, not observed behavior. Label it `inferred` at best, and corroborate
against at least one observed-behavior source or eval result before any procedure
built on it is marked `verified`.

## Step 2 — Extract candidate behaviors

Sweep the source and list every recurring, *checkable* action pattern. For each
candidate, capture: what triggered it, the action taken, and what failure it
visibly prevented (or would have). Tag each with the Fable Mode gate it serves
(see [fable-mode-gates.md](fable-mode-gates.md)).

Discard candidates that are pure capability ("was smart", "understood deeply") —
those go to the **scaffolding** list instead: external structure that compensates
(plan files re-read on schedule, mandatory test gates, smaller task slices).

## Step 3 — Normalize: vague → procedural

Every extracted item must pass the **two-operator test**: would two different
people (or models) reading the procedure do the *same thing*? If not, it is vague.

Convert using this frame:

- **Trigger**: when exactly does the procedure fire?
- **Action**: concrete steps, in order, with the artifact each step touches.
- **Check**: how the model knows the step worked — something that can fail.
- **Failure prevented**: the mistake this exists to stop.

Bad: "Be careful about hallucination." Good: "Before naming any API, function, or
flag — open the file or official doc that defines it in this session; if you
cannot, write `unverified:` in front of the claim."

Items that resist conversion after two attempts get marked `needs-refinement` and
parked — they do not enter the pack silently as style advice.

## Step 4 — Refinement loop (capped)

For each `needs-refinement` item: gather one more example from the source, retry
the conversion, or drop it. **Cap: at most 3 passes** over the refinement list per
pack version. Whatever is still vague after the cap is logged in the pack's
`known_gaps` — honestly unresolved beats eloquently useless.

## Step 5 — Package

Fill [behavior-pack-template.md](behavior-pack-template.md). Coverage status is
`complete` only when every section of the contract has content and every claim
carries a confidence label (verified / inferred / guessed / unverified). Partial
extractions (e.g. access ended mid-way) ship as `partial` with gaps listed — a
labeled partial pack is a valid deliverable.
