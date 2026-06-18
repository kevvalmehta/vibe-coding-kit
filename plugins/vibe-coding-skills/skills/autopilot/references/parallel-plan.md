# PLAN step — parallel competing architectures + judge

Goal: at the plan step, give the owner a JUDGED choice, not a single first draft — in roughly the
time of one plan (the drafts run at once).

## Recipe

1. **Classify complexity (cheap).** With the Haiku tier, read the spec and decide: 2 candidates for
   a simple feature, 3 for a non-trivial one. (Mechanical → cheap model.)
2. **Draft in parallel (default tier).** Spawn N subagents IN ONE message (so they run concurrently),
   each told to produce a DISTINCT architecture for the spec — give each a different lens, e.g.
   "simplest thing that works", "most robust / testable", "fastest to ship". Each returns a short
   structured plan (approach, key components, trade-offs, risks).
3. **Judge (default tier).** Spawn one judge subagent: given the spec + all candidates, score them on
   fit-to-spec, simplicity (constitution Rule V), testability (TDD), and risk; pick a winner and name
   the single best idea worth grafting from each runner-up.
4. **Summarize (cheap).** With the Haiku tier, format the judge's output into plain English for the owner.
5. **Write `plan.md`** from the winner (plus grafted ideas), via `/speckit-plan` conventions.
6. **Present + STOP**: show the chosen architecture, the rejected options (one line each), and WHY the
   winner won. Wait for go / change.

## Degrade gracefully (fail loud)

- A draft subagent that returns nothing or errors → proceed with the survivors and TELL the owner one
  candidate was dropped and why. Never silently shrink the field (FR-010).
- If only ONE candidate survives, say so plainly; the judge step is skipped and the owner decides.

## Non-Claude fallback

If parallel subagents are unavailable, draft the candidates SEQUENTIALLY (still distinct lenses), then
judge. Slower, same result. Say that it ran sequentially.
