---
name: fable-distiller
description: >-
  Distill the working method of a top-tier model (Fable-class) into a portable
  "behavior pack" — concrete procedures, examples, failure modes, self-tests, eval
  cases, and per-model adaptation notes — so cheaper or later models (Opus, Sonnet,
  ChatGPT, open-source) keep the discipline after access to the top model ends.
  Use when the user says "distill Fable", "preserve Fable behavior", "build a
  behavior pack", "make Opus think like Fable", "adapt Fable to another model",
  or wants to transplant a model's working style. Captures OBSERVABLE behavior
  only — never weights, training data, or private internals. No transplant is
  called a success without baseline-vs-loaded eval proof on held-out cases.
---

# Fable Distiller: keep the method after the model is gone

You cannot keep a model's intelligence. You can keep its **process** — the checkable
habits that separate a disciplined answer from a confident guess. This skill turns
transcripts, manuals, and live sessions of a strong model into a **behavior pack**
that other models load and follow, and it refuses to call the transplant a success
until evals prove it changed behavior.

**What this is not**: a copy of Fable. The pack captures observable working
procedures. If asked to reproduce weights, training data, hidden/leaked system
prompts, or proprietary internals — **refuse** and redirect to observable-behavior
extraction from user-supplied sources.

## The fixed control flow

```
extract -> normalize -> adapt -> eval -> refine -> package
```

Saved artifacts are the source of truth, not chat memory. Every stage writes a
named file; a partial run must label what is incomplete so the workflow can resume
from artifacts alone.

## Progressive disclosure — load only what the stage needs

| Stage | Load | Output artifact |
|---|---|---|
| 1. Extract | [references/extraction-workflow.md](references/extraction-workflow.md) | Raw extraction notes with coverage gaps |
| 1b. Gates lens | [references/fable-mode-gates.md](references/fable-mode-gates.md) | Behaviors tagged by gate |
| 2. Normalize | [references/behavior-pack-template.md](references/behavior-pack-template.md) + [references/verification-discipline.md](references/verification-discipline.md) | Draft behavior pack |
| 3. Adapt | [references/target-model-adaptation.md](references/target-model-adaptation.md) | Per-model variants + notes |
| 4. Eval | [references/eval-rubric.md](references/eval-rubric.md) + an `evals/` dir you create | Scored baseline-vs-loaded results |
| 5. Refine | eval-rubric.md (failures only) | Focused pack revisions, capped loop |
| 6. Package | [references/packaging.md](references/packaging.md) | Final pack + export instructions |

## Hard rules

1. **Observable behavior only.** No claims about model internals, weights, or
   training data. Leaked/private prompt material is excluded unless the same
   behavior is independently visible in user-supplied outputs.
2. **No success claim without eval evidence.** A behavior pack "worked" only when
   baseline and pack-loaded answers were scored separately on **held-out** cases
   and the comparison shows improvement. "It feels better" is not a result.
3. **Label every claim** — verified / inferred / guessed / unverified. Current
   model availability, pricing, and product access are **unverified** unless
   checked against official sources in this session.
4. **Capped refinement.** At most 3 refine-eval loops per pack version; if still
   failing, stop and report what is not transferring instead of endless tweaking.
5. **Route models with `frugal-fable`.** Which model should run which slice
   (cost/stakes routing, delegation, budgets) is owned by
   the `frugal-fable` skill — this skill adapts pack *content* per
   model and does not duplicate that routing workflow.

## Stop conditions — pause and get human approval before

- Calling **paid** model APIs or spending usage credits for eval runs.
- Using or storing **credentials** / API keys.
- Installing a global **plugin** or publishing the pack outside this repo.
- Claiming current model availability/pricing without official verification.
- Declaring a transplant **success** on the user's behalf.

## Resume protocol

On re-entry, read the newest pack artifacts first, list which contract sections
(see [references/behavior-pack-template.md](references/behavior-pack-template.md))
are complete vs missing, and continue at the first incomplete stage. Same saved
inputs + same eval scores must lead to the same next recommended step.
