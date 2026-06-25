# Implementation Plan: `/start` (the Conductor)

**Branch**: `009-conductor` | **Date**: 2026-06-25 | **Spec**: [spec.md](spec.md)

## Summary

The Conductor is a **procedure skill** (`SKILL.md` + references) plus **one small SessionStart greeting
hook** — it adds NO new pipeline. It greets the owner, elicits intent in plain English, and DRIVES the
existing skills (`idea-to-app` pipeline + `guide` routing), weaving in `research-scout`/`loop-design`/a
light stack suggestion at the right stages, with a checkpoint at each stage and a never-push/merge/deploy
wall. Built as an orchestrator/router (Anthropic *Building Effective Agents* — composable, not a new
engine). Protected the kit's standard way: guard tests on the SKILL.md content + the hook behavior.

## Technical Context

**Language/Version**: Markdown (skill) + Python 3.11 (the greeting hook + guard tests only).
**Primary Dependencies**: none new. Hook is stdlib Python (mirrors `recommender_nudge.py`).
**Storage**: a per-project marker file so the greeting fires once (git-ignored, like `.recommender-nudged`).
**Testing**: pytest guard tests — (a) SKILL.md states the required behaviors + routes to existing skills;
(b) the hook fires once + is deterministic. Pure filesystem/stdlib, no network/model.
**Target Platform**: any AI tool (portable SKILL.md); the hook is Claude-only with a documented manual fallback.
**Project Type**: a kit skill (procedure) + a SessionStart hook.
**Constraints**: plain English; checkpoints + bypass; never auto push/merge/deploy; greet once.

## Constitution Check

| Principle | Compliance |
|---|---|
| I. Plan before code | spec + plan first. |
| II. TDD | guard tests written FIRST (skill content + hook behavior), red → build → green. |
| III. Never break working code | branch `009-conductor`; full suite green; PR. Additive (new skill + new hook); no change to idea-to-app/guide behavior, only references them. |
| IV. Security first | hook is read-only/stdlib; no secrets; only injects a one-line offer (like recommender-nudge). |
| V. Simplicity & surgical | NO new pipeline, NO runner — reuse idea-to-app + guide. Smallest new surface: SKILL.md + 1 hook + references. |
| VI. LLM portability | SKILL.md portable; registered in AGENTS/SKILL-MAP/README; Claude-only hook has a documented manual fallback. |
| VII. Truth over confidence | says so + continues if a resource is unavailable; never pretends. |
| VIII. Verify AI output | N/A (kit procedure, not a product AI feature). |

**Result: PASS.**

## Project Structure

```text
specs/009-conductor/  — spec.md, plan.md, tasks.md, research.md, checklists/

.claude/skills/start/
├── SKILL.md                  # the Conductor procedure (greet, elicit, drive, weave, checkpoint)
└── references/
    └── stage-resource-map.md # the stage → skill/resource table (the conductor's core knowledge)

scripts/conductor_greeting.py # SessionStart hook: one-line offer, once per project (marker-deduped)

tests/test_conductor.py       # guard tests: SKILL.md required behaviors + routes; hook fire-once logic
```

**Structure Decision**: new skill `start` under `.claude/skills/` + a SessionStart hook in `scripts/`
(mirrors `recommender_nudge.py`). The marker file (e.g. `.claude/.conductor-greeted`) is git-ignored.

## Background Work

The SessionStart greeting hook (fires on session start; injects a one-line offer; writes a marker so
it fires once per project). Same shape as `recommender_nudge.py`.

| Worker | Function | Trigger |
|---|---|---|
| SessionStart hook (`scripts/conductor_greeting.py`) | inject a one-line "say start" offer | session start, once per project (marker) |

## Complexity Tracking

No violations — deliberately reuses idea-to-app + guide rather than adding a pipeline.
