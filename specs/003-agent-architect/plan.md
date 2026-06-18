# Implementation Plan: Agent-Architect

**Branch**: `003-agent-architect` | **Date**: 2026-06-10 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/003-agent-architect/spec.md`

## Summary

Build `agent-architect` as a **plain-markdown skill** (`.claude/skills/agent-architect/SKILL.md` + one
reference file) that reads an AI-app idea and emits a recommended agent design + pre-filled 12-factor
checklist + managed-vs-API suggestion, then offers `grill-me` by default. Recommendation-only (no
code-gen) in v1. Wire it into `idea-to-app`'s existing AI-inside gate (GATE 3/5) and register it in
`AGENTS.md` + `SKILL-MAP.md`. Protect structure + registration with one `pytest` guard (same pattern
as `tests/test_token_quick_wins.py` / `tests/test_autopilot_state.py`).

**Architecture choice (judged inline, no competing-draft panel):**
- **Chosen — pure-markdown skill + guard test.** Matches every other kit skill (idea-to-app, autopilot,
  grill-me are all markdown procedures). The skill's core act is *judgment* (read an idea → identify
  jobs → propose structure), which is exactly what a markdown procedure the LLM follows is for.
- **Rejected — markdown + a Python helper** (e.g. a job-type→model-tier mapper). Over-engineering: the
  job→model decision is judgment with a one-line rule, not a deterministic transform worth a module.
  Violates Simple + Surgical. (Skipping the subagent design panel here is itself token quick-win #1 —
  don't spend premium tokens judging a clear-cut, low-variance choice.)

## Technical Context

**Language/Version**: Markdown skill; Python 3.x for the guard test only.
**Primary Dependencies**: pytest, pathlib (already in repo). No new deps.
**Storage**: N/A.
**Testing**: pytest — `tests/test_agent_architect.py` (structure + registration guard).
**Target Platform**: the kit itself; LLM-portable (any AI tool follows `SKILL.md`).
**Project Type**: kit skill — markdown + guard test.
**Constraints**: recommendation-only (no code-gen, FR-006); surgical wiring into existing gate; no
behavior change to other skills.
**Scale/Scope**: 1 skill dir (SKILL.md + 1 reference), 1 guard test, ~3 small registration edits.

## Constitution Check

- **Plan before code** ✓ — this plan precedes the build; spec approved.
- **TDD always** ✓ — guard test written failing-first, then green; full suite stays green.
- **Never break working code** ✓ — additive skill + prose edits to `idea-to-app`/`AGENTS.md`/
  `SKILL-MAP.md`; no logic change to existing skills. Existing CI is the net.
- **Security first** ✓ — no inputs/secrets/network/DB. The skill only *proposes*; builds still go
  through the normal gated pipeline (FR-006 forbids code-gen).
- **Simple + surgical** ✓ — pure markdown; rejected the Python-helper option as over-engineering.
- **LLM portability** ✓ (Hard Rule VI) — plain-markdown `SKILL.md`; registered in `AGENTS.md` +
  `SKILL-MAP.md` (FR-008); not done otherwise.

No violations → Complexity Tracking empty.

## Project Structure

```text
specs/003-agent-architect/
├── spec.md      # done
├── plan.md      # this file
└── tasks.md     # next (/speckit-tasks)

.claude/skills/agent-architect/
├── SKILL.md                 # NEW — trigger + the decision routine + output format + reminders
└── references/
    └── decision-routine.md  # NEW — the detailed step-by-step recipe + a worked golden example

tests/
└── test_agent_architect.py  # NEW — structure + registration guard

# EDITED (surgical):
.claude/skills/idea-to-app/SKILL.md   # GATE 3/5: when AI-inside=YES, invoke agent-architect
AGENTS.md                              # register the skill + AI-inside paragraph pointer
SKILL-MAP.md                           # one row: "designing an AI app's agents → agent-architect"
```

### SKILL.md content (the decision routine)

1. **AI-inside precheck** — if the app has no LLM inside, DECLINE and defer to the normal pipeline
   (FR-007 / SC-004). No agent design forced on a CRUD app.
2. **Identify the jobs** — break the idea into distinct jobs (research / draft / classify / export…).
3. **Propose structure** — 1 orchestrator + 1 small focused agent per job (12-factor #10). One job →
   one agent (don't invent agents — edge case).
4. **Assign a model per agent** — mechanical jobs (classify/extract/format) → cheap Haiku tier with a
   one-line reason; judgment jobs → default tier (FR-002 / SC-001).
5. **Managed-vs-API suggestion** — long/async/triggered job → suggest Managed Agent; one-prompt
   feature → suggest Messages API. Always "recommend X because…", owner decides (FR-004 / SC-003).
6. **Pre-fill the 13-factor checklist** — each factor ticked-with-reason or explicit N/A+reason, drawn
   from `docs/ai-feature-checklist.md` (FR-003 / SC-002).
7. **Emit a simple text diagram** of the agents + data flow.
8. **Scaffolding reminder** — state that generating prompt files / tool stubs is a deferred next step,
   not part of this output (FR-006).
9. **Offer + run grill-me by default** — pressure-test the design; skip only on explicit decline
   (FR-005 / SC-005).

A **worked golden example** ("research → draft → email" → orchestrator + 3 subagents, classify→Haiku,
email→Managed Agent) lives in `references/decision-routine.md` so the output shape is concrete and the
guard test can assert it exists.

### Guard test assertions (TDD targets)

- **T1** `SKILL.md` exists with valid frontmatter (`name: agent-architect`, non-empty `description`).
- **T2** `SKILL.md` covers the non-negotiable rules: a decline-if-no-AI rule, the Haiku model-routing
  rule, managed-vs-API as **suggest (owner decides)**, grill-by-default, and the scaffolding-deferred
  reminder. (String/section checks.)
- **T3** the 13-factor checklist is referenced (links `docs/ai-feature-checklist.md`).
- **T4** a worked golden example exists in `references/decision-routine.md`.
- **T5/T6** registered in `AGENTS.md` + `SKILL-MAP.md` (FR-008).
- **T7** wired into `idea-to-app` (the SKILL.md references `agent-architect` at the AI-inside gate).

## Background Work

None.

## Complexity Tracking

No violations — empty.

## Known risk (plain English)

A skill's *behavior* (the model actually following the routine well) can't be fully unit-tested — the
guard test proves structure + wiring, not output quality. Mitigation: ship a worked golden example in
the skill and, at the verify step, RUN the skill on a sample AI-app idea and eye-check the output
against SC-001/002/003. (Same limitation every markdown skill has.)
