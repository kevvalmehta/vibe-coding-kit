# Project seed — the starter AGENTS.md for any new project

You cannot finetune a commercial model, and you don't need to. What made the
good sessions good was never the model alone — it was the *files the model was
made to read and obey*. This seed is how a brand-new project gets that
environment from day one, for any model, any vendor, any year.

Copy the block below into `AGENTS.md` (or `CLAUDE.md`) at the project root,
fill the brackets, then create the four files it names. Keep it under ~60
lines — length degrades compliance; detail lives in the referenced files, not
here.

---

```markdown
# <Project name>

<Two sentences: what this project produces, and who approves it.>

## Quality contract (binding, in precedence order)

1. `reference/charter.md` — the numbered house rules (R1–Rn). Read before
   ANY producing work. Reviews cite rule numbers.
2. `reference/learnings.md` — Rules layer + feedback log. Read at step 1;
   append the round a correction happens; two recurrences → promote.
3. `reference/exemplars/` — approved output = the bar. Fetch the closest
   exemplar before producing; compare side-by-side before presenting.
4. `<spec/contract file for the current piece of work>` — decisions are
   written HERE before generation. Not in the file = a default = slop.

## Gates (blocking — nothing skips these)

- Pre-flight: fill the 5-line brief (charter) before drafting. An
  unfillable line = STOP, an input is missing.
- Validators: `<command>` — all PASS before the Present Gate.
- Present Gate: the charter's scored checklist, fresh context if the tool
  allows. Below the bar = rework, never present.

## Truth rules

- Never fabricate a fact, person, quote, number, or working-looking
  endpoint. Gap → ask up to 3 targeted questions, or insert a labelled
  placeholder from the whitelist. "Couldn't check" is its own status —
  never report it as a pass.
- Report outcomes honestly: failing tests are reported as failing;
  skipped steps as skipped.

## Portability

Plain Markdown + scripts that need nothing installed. Every tool-dependent
step states its manual fallback; the fallback is the contract.
```

---

## Why this works on any model (the "finetuning" you actually wanted)

A strong model with no contract produces variable output — great when it
happens to make good decisions, slop when it defaults. A mediocre model with
this contract produces *consistent* output, because:

- decisions are forced into files **before** generation (nothing to "forget"),
- the mechanical slice is checked by scripts (no diligence required),
- the judgment slice is checked by closed-ended questions (no taste required —
  "a model with weaker taste should trust the checklist MORE, not less: the
  questions encode the judgment so you don't have to have it"),
- the bar is communicated by exemplars (no interpretation required),
- corrections compound in learnings files (the system gets better even if the
  model never does).

The model is a replaceable executor. The quality lives in the repo.

## Growing a new project's charter from zero

Day one, you have no scar stories. Seed the charter three ways:

1. **Steal from siblings.** Any rule already promoted in another project's
   charter that plausibly applies here comes across — with its provenance
   ("imported from <project>: <the original failure>").
2. **Mine the owner.** Ask: "what do you always end up correcting?" Every
   answer is a rule with provenance.
3. **Leave the rest to the loop.** Don't invent speculative rules — rules
   born from rejection get kept, rules invented "to be safe" rot. The
   capture/promote loop will grow the charter honestly from real corrections.

## Skill-file hygiene for the new project

- Core instruction file ≤ ~180 lines: context loading, the one overriding
  rule, the phase sequence, hard gates. Phase detail goes in per-phase
  reference files loaded when that phase runs.
- Every MUST-PASS command appears in the core file, near the top, not at
  line 650 of anything.
- After any slimming/refactor claiming "nothing deleted": independent
  fresh-eyes content-loss diff before merging.
- If the project ships as a plugin with a separate installed copy: a
  one-command sync script + "run after every merge" note here in AGENTS.md.
  "Merged" and "live" are different facts.
