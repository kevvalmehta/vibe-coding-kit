# Implementation Plan: `/research-scout`

**Branch**: `008-research-scout` | **Date**: 2026-06-25 | **Spec**: [spec.md](spec.md)

## Summary

`/research-scout` is a **procedure skill** — a plain-markdown `SKILL.md` (plus small reference files)
that any AI tool can follow, exactly like `/discover`, `guide`, and `agent-architect`. It is NOT a
Python tool: there is no runner. In Claude Code it uses web search + GitMCP and may fan out helper
subagents; the procedure itself is the deliverable. It gathers cited prior-art evidence, writes a
`research/<topic>.md` note + a plain-English summary, and is callable standalone or (with consent)
from grill-me / the plan / the future conductor.

Because it's a procedure (no deterministic runtime logic), it's protected the kit's standard way: a
**guard test** (`tests/test_research_scout.py`) that asserts the SKILL.md contains every
non-negotiable rule + the registrations — so the spec's FRs can't silently rot. (Same pattern as
`test_agent_architect.py`, `test_health_skill.py`.)

## Technical Context

**Language/Version**: Markdown (the skill) + Python 3.11 only for the guard test (pytest).

**Primary Dependencies**: none new. Runtime uses existing web search + GitMCP (already in the kit).

**Storage**: a `research/<topic>.md` note in the project (owner-readable). No database.

**Testing**: pytest guard test (pure filesystem string-reads, no network/model) — the kit convention
for procedure skills.

**Target Platform**: any AI tool (portable SKILL.md). 

**Project Type**: a kit skill (procedure).

**Performance/Constraints**: quick default + hard ceiling on searches/cost (runaway guard); plain
English; never fabricate; injection-safe; cite everything.

## Constitution Check

| Principle | Compliance |
|---|---|
| I. Plan before code | spec + this plan before the skill is written. |
| II. TDD | Guard test written FIRST, asserting required SKILL.md content + registration; red → write skill → green. (No runtime logic to unit-test — it's a procedure, like /discover.) |
| III. Never break working code | isolated branch `008-research-scout`; full suite must stay green; merge via PR. Additive only. |
| IV. Security first | fetched content treated as DATA not instructions (injection-safe); no secrets; sources are public. |
| V. Simplicity & surgical | NO Python runner (YAGNI) — a procedure skill + 2 reference files. Lean. |
| VI. LLM portability | plain-markdown SKILL.md; registered in AGENTS.md + SKILL-MAP.md + README. Non-Claude agents follow it by hand. |
| VII. Truth over confidence | never fabricate a source/quote/finding; cite every claim; graceful fetch ladder (say so + stop if unavailable); surface source disagreement. |
| VIII. Verify AI output | N/A — research-scout isn't an AI feature in a product; it's a kit procedure. (Its own correctness is guarded by the guard test + eye-checked at verify.) |

**Result: PASS.**

## Project Structure

```text
specs/008-research-scout/
├── plan.md, spec.md, tasks.md, research.md (the cited sources gathered before speccing)
└── checklists/requirements.md

.claude/skills/research-scout/
├── SKILL.md                    # the procedure (decline/ask/consent, depth tiers + ceiling,
│                               #   source quality, citation pass, STOP, advise, plain English)
└── references/
    ├── source-quality.md       # the source-tier ladder + triage + injection-safe rule
    └── note-template.md        # the research/<topic>.md cited-note template

tests/test_research_scout.py    # guard test (filesystem string-reads)
```

**Structure Decision**: new procedure skill under `.claude/skills/research-scout/` (travels into
stamped projects via `new-project.ps1`). No runner — the runtime is the AI following the markdown.

## Background Work

None. (research-scout runs on demand; it does no scheduled/background work.)

## Complexity Tracking

No violations — deliberately simpler than `/agent-eval` (no runner).
