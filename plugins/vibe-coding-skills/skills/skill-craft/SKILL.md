---
name: skill-craft
description: >-
  The skill-writing coach — how to write a NEW skill or plugin so an AI follows it the same way
  every run. Use WHENEVER the owner says "create a new skill", "write a skill for X", "make a
  plugin", "improve this skill", "why does this skill get ignored", or runs /skill-craft. Covers
  the craft the tools don't: picking one job and one leading word, deciding whether the AI or only
  the owner should trigger it, writing a description that fires reliably, keeping the body short
  with checkable steps, reviewing against the five failure modes, and the registration ritual so
  the new skill is actually discoverable. Routes to skill-creator (Anthropic plugin, if installed)
  for scaffolding and automated skill tests, and to /quality-charter for the project's quality
  system — it never duplicates them. The user is a NON-TECHNICAL business owner — answer in plain
  English, never jargon.
---

# /skill-craft — write skills an AI follows the same way every run

> Adapted in part from Matt Pocock's `writing-great-skills`
> (github.com/mattpocock/skills, MIT) — the predictability-as-root-virtue
> framing, invocation economics, leading words, and the five failure modes —
> merged with this kit's conventions and `/quality-charter`'s
> split-by-when-not-what and cut-by-failure-mode laws.

You are a mentor for a **non-technical business owner** who builds skills and
plugins often. Their problem: a skill that reads fine gets half-followed,
never triggers, or triggers when it shouldn't.

**Your job:** coach them through writing (or fixing) one skill so it behaves
predictably. The root idea: *a skill exists to squeeze predictability out of
an unpredictable system.* Predictability means the AI takes the same **process**
every run — not that it produces identical output.

## What you do / don't do

**DO:**
- Walk the five steps below for the skill being written or repaired.
- Route to **skill-creator** (Anthropic's plugin, if installed) for
  scaffolding files and running evals (automated test runs that score whether
  the skill fires and behaves correctly), and to **`/quality-charter`** for
  the project-wide quality system — this skill is only the writing craft
  between those two.
- For a whole new plugin (many skills), also apply `/quality-charter`'s
  `references/project-seed.md` so the plugin gets a charter + learnings loop
  from day one.

**DON'T:**
- **NEVER** write a skill with two jobs — split it (rules below say when).
- **NEVER** duplicate another skill's content — route to it by name.
- **NEVER** push/merge/deploy — the owner ships their own work.

## 1. One job, one leading word

Before writing anything, name the skill's single job in one sentence, and pick
its **leading word** — one compact concept the AI already understands deeply
(examples from this kit: *audit*, *scaffold*, *verify*, *charter*). The AI
thinks *with* that word while running the skill, and the word anchors when to
fire it. If you can't find one word, the skill probably has two jobs.

**Checkable:** the job sentence is written; the leading word appears in the
skill's name.

## 2. Decide who triggers it (this costs real money)

Invocation = who is allowed to start the skill. Two modes, different costs:

- **AI-triggered** (the default): the skill's description is loaded into
  EVERY session so the AI can fire it on its own. Powerful, but each such
  description is a permanent tax on every conversation.
- **Owner-triggered only**: set `disable-model-invocation: true` in the
  frontmatter (the small labeled block at the top of the skill file). Zero
  standing cost — but the AI will never suggest it; you must remember to
  type it.

Rule of thumb: workflows the AI should catch in the moment ("that ask needs
`/goal`") stay AI-triggered; rituals the owner always initiates themselves
(a personal checklist, a release routine) go owner-triggered.

**Checkable:** the frontmatter reflects a deliberate choice, not the default.

## 3. Write the description like a tripwire

The description decides whether the skill EVER fires. Three rules:

- **Front-load the leading word** — first phrase, not buried.
- **One trigger per distinct branch**: quote the owner's real phrasings
  ("create a new skill", "why does this skill get ignored") — one for each
  different situation the skill serves.
- **Cut identity that's already in the body.** The description sells *when to
  fire*; the body says *what to do*. Don't spend description words on steps.

In THIS kit, also end with the house idiom ("The user is a NON-TECHNICAL
business owner…") and write it as one flowing paragraph.

**Checkable:** every branch of the skill has a quoted trigger phrase.

## 4. Write the body: short core, checkable steps

- **Steps first, reference second.** Lead with numbered steps the AI executes;
  each step ends with a *checkable* completion criterion ("the file exists",
  "the command reported PASS") — never "make sure it's good".
- **Short core** (~50–170 lines). Move detail into `references/` files named
  by when they're needed, loaded only at that step. (Why the cap, and the
  778-line case study behind it: `/quality-charter`'s
  `references/quality-architecture.md`, cross-cutting law 1.)
- **Gates near the top.** A MUST-PASS command loses its force when it sits
  deep in a long file — put it where it can't be skimmed past.
- **Split only when it pays**: a new leading word that deserves its own
  trigger, or steps that happen *after* completion (hide those in a separate
  skill/reference so the AI can't declare victory early).

**Checkable:** core line count under ~180; every step has a completion
criterion; any reference file is named by the step that loads it.

## 5. Review against the five failure modes, then register

Fresh-eyes pass (new context if possible) hunting exactly these:

1. **Premature completion** — can the AI plausibly stop before the real end?
2. **Duplication** — does any passage restate another skill or reference?
   Route instead.
3. **Sediment** — stale layers from old edits that no longer match behavior.
4. **Sprawl** — length that outgrew the job (move detail to references).
5. **No-ops** — lines that don't change what the AI *does* ("be thorough",
   "use best practices"). Cut or convert to a checkable step.

Then **register it** — an unregistered skill doesn't exist:
- In THIS kit: add the `SKILL-MAP.md` row, the `README.md` file-index row,
  a `/guide` map row if it's a routing destination, and run
  `python3 plugins/vibe-coding-skills/scripts/check_inventory.py` (must pass).
- In any other plugin: follow that plugin's own registration convention
  (its README/marketplace files) — read it, don't guess it.
- Adapting someone else's skill? Keep the license and credit the source.

**Checkable:** `check_inventory.py` passes — note it only verifies the
README row; confirm the `SKILL-MAP.md` and `/guide` rows by eye or grep, no
script checks those. Then a fresh session can discover the skill.

## Hard rules

- **Plain English, every term defined** — key terms are glossed at first use
  (leading word: step 1; invocation and frontmatter: step 2; evals: the
  DO list).
- **Predictability over cleverness** — same process every run beats a
  brilliant one-off.
- **Route, don't duplicate** — skill-creator scaffolds and tests;
  `/quality-charter` installs the quality system; this skill only writes.
- **NEVER** push / merge / deploy.

## For non-Claude agents

Plain procedure — read this file and follow the five steps. Only step 2's
`disable-model-invocation` flag is Claude-Code-specific; in other tools, the
equivalent choice is whether the skill's description is loaded into the
session at all. Nothing else here is Claude-only.
