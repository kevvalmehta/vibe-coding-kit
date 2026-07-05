# Gates & validators — design rules for the enforcement layer

The enforcement layer has three tiers, each catching what the tier below
can't. Every check declares which tier it belongs to and what it can NOT
catch — honest scope is what keeps the tiers from cannibalizing each other.

| Tier | Catches | Form |
|---|---|---|
| 1. Validators | mechanical defects (banned strings, missing files, structure) | deterministic scripts, MUST PASS |
| 2. Gate questions | judgment defects (generic, off-voice, rushed) | closed-ended scored checklist |
| 3. Exemplar comparison | "competent but not crafted" | side-by-side read |

## The partition test (do this first)

For every charter rule ask: *does this failure have a mechanical signature?*
A string that shouldn't appear, a file that must exist, a count with a cap, a
value that must match a source of truth. If yes → Tier 1 script. If no →
Tier 2 question. Two failure modes to avoid:

- **Wasting a gate question on regex work.** A recurring correction that could
  be a script MUST become a script — prose reminders about mechanical defects
  recur forever.
- **Pretending judgment is mechanical.** "Does this sound like the client?"
  cannot be a regex. Don't fake it with keyword counting; put it in the gate.

## Validator design rules (Tier 1)

1. **Stdlib only, no network, no third-party deps.** The script must run
   identically on any machine, driven by any model, forever.
2. **Deterministic:** identical input → identical output. No timestamps, no
   randomness, no "current date" logic.
3. **Test-first:** write the failing test, then the validator (route to
   `/ship`). Every exemption gets its own test carrying the rationale — that's
   how "why is this allowed?" survives the author's context.
4. **Honest scope in the docstring:** "Taste is NOT checked here — this
   supplements the Present Gate, it never replaces it."
5. **Whitelist the loud placeholders.** Allow exactly a small recognizable
   set of known-gap markers (`missing-photo`, `missing-asset`, `TODO-OWNER`);
   fail *everything else* placeholder-shaped (`PLACEHOLDER`, `lorem ipsum`,
   `example.com`, `YOUR_…`) — the dangerous placeholder is the one that reads
   as real.
6. **One CLI, subsettable.** A single runner with an `--only <checks>` flag
   lets the mid-work self-check reuse the exact same code as final QA.

## Status vocabulary (non-negotiable)

Four statuses, never collapsed:

- **PASS** — the check ran and found nothing.
- **FAIL** — defect found, automation may attempt a fix.
- **FLAG** — defect found, must go to a human, never auto-patched
  (secrets, legal text, anything about real people).
- **COULDN'T-CHECK** — the check did not actually run (missing tool, needs a
  browser, unreadable input). *Never report this as PASS.* "No false PASS" is
  the rule that keeps the whole report trustworthy.

## Gate design rules (Tier 2)

1. **Closed-ended questions only.** Not "does this look good?" but "cover the
   logo — does anything remain that couldn't be any company's?" Each question
   derives from a charter rule and cites it, so gate and charter can't drift.
2. **Fixed length, numeric bar.** e.g. 12 questions, present at 12/12, fix and
   note at 10–11, rework below 10. The bar routes work *backward*, never
   forward with apologies.
3. **Mechanical checks run first** so the gate never re-litigates what a
   script already caught.
4. **Escalation rule:** the same question failing twice means the approach is
   wrong — return to the spec/skeleton, don't patch the symptom. This is what
   prevents an infinite polish loop.
5. **Fresh context where possible** — the writer is biased toward its own
   work. Manual fallback (and the fallback is the contract): a deliberate
   second pass, ideally after unrelated work.
6. **Weaker model? Trust the checklist MORE, not less** — the questions encode
   the judgment so the executor doesn't have to have it.

## The never-fabricate branch (wire into every producing skill)

Every input gap takes exactly one of two branches — there is no third:

1. **Bounded ask:** up to 3 short, targeted questions. One round of questions
   beats three rejected drafts. If the user says "just write it": proceed from
   documented facts only, and tag every dramatized line as such.
2. **Labelled placeholder / explicit flag:** the whitelisted loud marker, or a
   plain statement — "could not read source X, it is not reflected here."
   Never pretend to have read something. Never invent a person, quote, number,
   or endpoint. Partial results with a `sources_failed` list beat a complete-
   looking result that's quietly wrong.

## Advisory calibration (the guardrail you must not delete)

Some work has no mechanical check AND no crisp gate question — depth of
thought, pacing, "did you actually digest the inputs." The only defense is an
advisory anchor in the instructions: "Time: 20–30 minutes. Faster usually
means a phase got rushed." These lines look like padding; they are
load-bearing. Before cutting ANY line from an instruction file, name the
failure it prevents and what still prevents it after the cut — if the answer
is "nothing," it stays.
