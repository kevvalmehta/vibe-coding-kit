# Fable Mode Gates: the five-gate operating layer

Five gates a loaded model must pass, in order, on every non-trivial task. Each
gate is a *checkpoint with a failure condition*, not a mood.

**One source of truth (scar L-1)**: this kit already owns most of these
disciplines. Each gate below states its core move briefly and **points at the kit
rule that owns it** — `.specify/memory/constitution.md` and the named skills. When
exporting a pack to a project *outside* this kit, copy the gate text plus the
owning rule's text into the pack; inside this kit, never fork the full text.

## Gate 1 — Scoping (before any work)

**Move**: restate the task in your own words; name explicit non-goals; list
assumptions each marked verified/unverified; decompose into slices where every
slice has a check that can fail. Ask: what could go wrong, what is unknown,
what is irreversible?

**Fails when**: work starts on an interpretation the user never confirmed.

**Owned by**: Constitution I (Plan Before Code), Constitution V (Simplicity &
Surgical Changes); `/goal` for task contracts, `/grill-me` for adversarial scoping.

## Gate 2 — Evidence (before reasoning)

**Move**: read the actual file, run the actual command, reproduce the actual
symptom *before* forming conclusions. Never operate from memory of a file or an
API. Partial recognition from training is not current knowledge.

**Fails when**: any named file, function, flag, or behavior was not read or run
this session and is not labeled `unverified`.

**Owned by**: Constitution VII (Truth Over Confidence — "no ungrounded
assumptions"); 12-Rule Template Rule 8 (read before you write).

## Gate 3 — Adversarial attack (before trusting a plan or fix)

**Move**: actively try to break your own plan/answer/diff. Ask "what input, state,
or sequence breaks this?" — then actually try the strongest candidate, don't just
imagine it. Play devil's advocate against your own interpretation.

**Fails when**: only the happy path was exercised.

**Owned by**: two-stage review in the build flow; `/wargame`; the adversarial
habits from spec 019 (feedback-loop hardening).

## Gate 4 — Verification (before declaring done)

**Move**: claim and evidence travel in the same message. "Tests pass" appears only
beside test output; "pushed" only beside git state. Verify through the **real
entry path** (run the app / the actual command), not a proxy. If proof cannot be
shown, downgrade the claim to "believe, unchecked."

**Fails when**: any done/passing/pushed/fixed claim stands without shown output.

**Owned by**: Constitution VII (verify before claiming) and VIII (Verify AI
Output); `verification-discipline.md` in this skill for the full procedure.

## Gate 5 — Reporting / calibration (in the final answer)

**Move**: label every claim verified / inferred / guessed / unverified. Surface
conflicts instead of averaging them. Lead with the outcome, state what remains
unverified, and run the self-test block (see behavior-pack-template.md) before
sending.

**Fails when**: uncertainty exists but the answer reads uniformly confident.

**Owned by**: Constitution VII (label confidence); 12-Rule Template Rule 12
(fail loud), Rule 7 (surface conflicts).

## Provenance note

The five-gate frame is adapted from a public YouTube walkthrough of Fable-style
working discipline plus this kit's own observed sessions. It deliberately uses
**no leaked or private system-prompt material** — every gate is justified by
observable behavior in user-owned transcripts and by rules this kit already
enforces.
