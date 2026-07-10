# Behavior Pack Template

Copy this file to start a new pack. A pack is `complete` only when every section
has real content and every claim carries a confidence label. The authoritative
shape is `specs/020-fable-distiller/contracts/behavior-pack-contract.md`.

---

## 1. Source and Scope

- **Pack name**:
- **Source summary**: <which transcripts/manuals/self-reports fed this pack>
- **Coverage status**: complete | partial | exploratory
- **Known gaps**: <what the sources did not cover>
- **Claim labels**: every statement below is marked verified / inferred /
  guessed / unverified. Self-reported procedures start at `inferred` until
  corroborated by observed behavior or eval results.

## 2. Operating Procedures

Repeat this block per procedure. Every procedure must contain a concrete action —
a trait or style adjective ("be rigorous") is not a procedure.

- **Name**:
- **Layer**: procedure (the model follows it) | **scaffold** (structure built
  around the model — plan files, forced re-reads, external test gates). Weaker
  target models need more of the scaffold layer; see
  [target-model-adaptation.md](target-model-adaptation.md).
- **Gate covered**: scoping | evidence | adversarial attack | verification |
  reporting/calibration
- **Trigger** (when it fires):
- **Action** (steps, in order):
- **Check** (how the model knows it worked — must be able to fail):
- **One short example**:
- **Failure prevented**:
- **Confidence label**:

### Self-test block (goes at the tail of every generated prompt variant)

Before the final answer, the loaded model answers in one line each:

1. Did I run what I claim runs? (point to where)
2. Did I read what I claim to know? (point to where)
3. What is the strongest thing that would break this?
4. What am I still guessing about? (label it)
5. Is any claim in my answer standing without evidence beside it?
6. Did I surface every conflict I found, or did I quietly average one away?
7. What here is irreversible, and did I gate it behind explicit approval?

## 3. Target Model Variants

For each target model (see [target-model-adaptation.md](target-model-adaptation.md)):

- **Compact system prompt** (numbered, priority-ordered, self-test tail):
- **Full manual prompt**:
- **Examples-first variant** (default for weaker models):
- **Model-specific adaptation notes** (observed strengths/failure modes):
- **Model-routing notes** (cost / intelligence / taste scores, each labeled
  observed / inferred / unverified):

## 4. Eval Suite

Lives in `evals/fable-distiller/cases.yaml` (or a per-pack copy). Requirements:

- At least 20 cases; trap type on every case.
- No more than 25% of cases share one trap type; at least 5 distinct trap types.
- Every case marked `split: training | validation | holdout`.
- Holdout cases are NEVER used to tune the pack.
- Each case: expected behavior + critical failures + scoring dimensions.

## 5. Rubric

Lives in [eval-rubric.md](eval-rubric.md) + `evals/fable-distiller/rubric.md`.
Must include output-quality dimensions, trajectory-quality dimensions, the 80%
passing bar, and critical-failure vetoes.

## 6. Results Log

One row per case per run:

| Case ID | Split | Baseline score | Loaded score | Outcome (improved/degraded/unchanged) | Notes |
|---|---|---|---|---|---|

- **Overall verdict**: improved | degraded | unchanged — computed on **holdout
  cases only**.
- **Refinement notes**: what was changed between pack versions and why.

---

## Completion checklist

- [ ] Every procedure passes the two-operator test (two readers act identically)
- [ ] Every procedure has an example or a failure-prevented entry
- [ ] Procedures and scaffolds are separated by the `Layer` field
- [ ] No claim about private internals, weights, or training data anywhere
- [ ] Every claim labeled; self-reports not marked `verified` without corroboration
- [ ] Eval suite meets count/diversity/split rules
- [ ] Results log filled from actual runs — no success claim without it
