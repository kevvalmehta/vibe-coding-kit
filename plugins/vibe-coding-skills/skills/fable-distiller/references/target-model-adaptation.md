# Target-Model Adaptation: shape the pack per model

The same pack content must arrive in the form each model actually follows.
Adaptation is about **form and scaffolding density**, not new rules.

## The core axis: scaffold density scales inversely with model tier

Two layers exist in every pack (see the `Layer` field in
[behavior-pack-template.md](behavior-pack-template.md)):

- **Procedures** — rules the model follows inside its own reasoning.
- **Scaffolding** — structure built *around* the model: plan files it must re-read
  every N steps, external test gates it cannot skip, task slices kept small,
  hooks that block done-claims without proof.

Capability gaps do not transfer by prompt. Long-horizon coherence, knowing when
it's wrong, taste — a weaker model cannot be instructed into these, but scaffolds
compensate:

| Capability gap | Compensating scaffold |
|---|---|
| Long-horizon coherence (plan drift) | External plan file + mandatory re-read every N steps; smaller slices |
| Metacognition (knowing when wrong) | External verification gates (tests, scripts, hooks) — never trust self-report |
| Taste / judgment under ambiguity | Worked examples + escalation rule: "if ambiguous, stop and ask" |

Rule of thumb: **stronger model → mostly procedures; weaker model → the
scaffolding does most of the work.**

## The three prompt variants (produce all three per target)

1. **Compact system prompt** — numbered, priority-ordered rules with an explicit
   line: "If you can only keep three rules, keep 1–3." Ends with the self-test
   block from the template. Why the ordering: long instruction lists degrade via
   *middle-loss* — models follow the first and last rules and silently drop the
   middle. The self-test tail forces re-touching every gate that middle-loss
   dropped.
2. **Full manual** — the complete pack prose for models that follow long
   instruction sets well.
3. **Examples-first variant** — one worked example per procedure, rule stated
   after the example. **Default recommendation below Sonnet-class capability**:
   small models imitate worked examples far more reliably than they follow
   abstract rules.

## Instruction-length fallback (never expand a failing prompt)

If a target model ignores or over-follows parts of the pack, the fix is a
**shorter, higher-priority version — never a longer one**. Cut to the top rules,
keep the self-test tail, move the cut material into scaffolding. Record what was
cut and why in the model's adaptation notes.

## Per-model starting notes (labels mandatory)

These are starting hypotheses — replace with **observed** eval behavior and
relabel as you go:

- **Opus-class** *(inferred)*: follows long manuals well; full manual + minimal
  scaffolding. Watch for over-verification on trivial tasks — include the
  effort-matching procedure so it scales down too.
- **Sonnet-class** *(inferred)*: compact numbered variant + self-test tail +
  real scaffolding (plan re-reads, test gates). Middle-loss is real here.
- **Haiku / small-model class** *(inferred)*: examples-first variant; treat the
  model as an executor inside gates it cannot skip.
- **GPT-class / other vendors** *(guessed — verify against the actual model)*:
  reportedly strong literal instruction-following, weaker at knowing when to
  deviate; conflict-surfacing rules and stop conditions matter most. Do not trust
  this note without eval evidence.

**Current model claims**: availability, pricing, and product access change under
you. Every such claim in adaptation notes is labeled **verified** (checked against
official sources this session), **inferred** (from observed behavior), or
**unverified**. Unlabeled pricing/availability claims are contract violations.

## Model-routing table (for the pack's routing notes)

Fill per environment; scores are relative, each labeled observed/inferred/unverified:

| Model | Cost score (higher = cheaper) | Intelligence | Taste | Best for | Avoid for |
|---|---|---|---|---|---|
| <name> | | | | | |

- **Intelligence**: reasoning, planning, code review, instruction depth.
- **Taste**: judgment-heavy creative/UI/writing/product choices.

**Do not duplicate routing machinery.** Which model runs which slice at runtime —
stakes/reversibility/ambiguity floors, delegation, budget discipline, context
firewall — is owned by `.claude/skills/frugal-fable/SKILL.md`. This file shapes
pack *content* per model; frugal-fable decides *who does the work*. If the two
ever disagree about routing, frugal-fable wins and this file gets fixed.
