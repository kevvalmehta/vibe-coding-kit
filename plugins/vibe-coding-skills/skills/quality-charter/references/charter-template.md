# Charter template — copy, fill, and check in as `reference/charter.md`

Replace everything in angle brackets. Delete rules that don't apply; append new
ones at the end — **never renumber existing rules** (citations elsewhere would
break). Keep every "Why" — a rule without its scar story gets argued with;
a rule with one gets followed.

---

```markdown
# <Project> Charter

This file is the single source of truth for HOW <project's deliverable type>
is made. Every producing skill reads it before working. Reviews cite rules by
number ("fails R3"). Rules are appended, never renumbered.

## A. Audience & register

- **R1 — Write for the buyer, not the reader-in-general.**
  <one line: who actually pays/decides>
  Why: <the real failure that taught this>
- **R2 — Lock the register before drafting.**
  <e.g. "plain-spoken expert, no hype">
  Why: <…>

## B. Grounding (truth rules)

- **R3 — Never fabricate a fact, story, person, or number.** If an input is
  missing: ask up to 3 targeted questions, or insert a labelled placeholder
  from the whitelist (see Gates). Why: invented content has failed every time
  it was tried.
- **R4 — Every claim traces to an input document or is tagged as opinion.**
  Why: <…>

## C. Craft

- **R5 — <your first craft rule, stated falsifiably>.** Why: <…>
- **R6 — <…>.** Why: <…>
  <!-- Craft rules must be concrete enough to check: "≤ N colors", "no section
       may repeat the previous section's layout", "verbs over adjectives" -->

## D. Style mechanics (the machine-checkable slice)

- **R20 — <banned tokens/phrases/punctuation habits>.** Enforced by
  `<script>` — run it, don't self-certify. Why: recurred on every build until
  it became a script.
- **R21 — <required structural properties>.** Enforced by `<script>`.

## Pre-flight Brief (before ANY drafting — blocking)

Write these 5 lines at the top of the working draft. If you cannot fill a
line, STOP: an input is missing — go get it or ask.

    For:       <who this is for, one line — R1>
    Register:  <the locked register — R2>
    Owned:     <3–6 verbatim phrases/values this must use — R5>
    Nevers:    <the hard exclusions — R3, R20>
    Exemplar:  <the closest approved exemplar this must stand next to>

## Present Gate (before ANYTHING reaches the owner — blocking)

1. Run the validators: `<command(s)>` — all must report PASS.
2. Answer the gate questions (closed-ended, from sections A–C above),
   one line each, honestly:
   - <question derived from R1: "would the buyer stop scrolling?">
   - <question derived from R5>
   - Exemplar test: read yours beside the exemplar named in the brief.
     If yours reads like a competent summary and theirs like crafted work,
     redraft.
3. Score: all pass → present. One miss → fix, then present with honest notes.
   Two or more → do NOT present; rework. Same question failing twice →
   the approach is wrong; go back to the spec, don't patch symptoms.
4. If your tool supports fresh contexts/subagents, have a fresh context run
   this gate (the writer is biased toward its own work). Manual fallback:
   a deliberate second pass after a break — the fallback IS the contract.

## Self-evolution contract

- READ: step 1 of every producing skill loads this charter + the learnings
  file + the closest exemplar.
- CAPTURE: when the owner corrects anything, append the lesson to the
  learnings file in the same round. An unbanked correction is a defect.
- RECONCILE: if a new lesson contradicts a rule, rewrite the rule and mark
  the old entry SUPERSEDED — never leave two conflicting instructions live.
- PROMOTE: a correction that recurs twice (any project/client) MUST become
  a numbered rule here or a validator check, and be marked [promoted: yes].

## Portability

Everything above is plain Markdown + stdlib scripts and runs identically in
any AI tool. Every tool-dependent step states its manual fallback; the
fallback is the contract — richer tooling is an optimization.
```

---

## Filling it well — three tests

1. **The stranger test:** could a different model, with zero taste and no chat
   history, read only this file and make the same decisions? If not, a rule is
   still an adjective — make it concrete (numbers, lists, named bans).
2. **The citation test:** could a review say "fails R7" and both sides know
   exactly what that means? If a rule needs interpretation, split it.
3. **The provenance test:** does every rule carry the real failure that
   motivated it? Rules invented speculatively ("might be nice") rot; rules
   born from a rejection get kept.
