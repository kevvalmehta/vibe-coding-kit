---

description: "Task list — Agent-Architect"
---

# Tasks: Agent-Architect

**Input**: Design documents from `/specs/003-agent-architect/`

**Prerequisites**: [plan.md](plan.md) (required), [spec.md](spec.md) (user stories)

**Tests**: REQUIRED — "TDD always". Guard test `tests/test_agent_architect.py` written failing-first,
then made green file-by-file. Behavior quality is eye-checked at verify (a skill's output can't be
fully unit-tested — see plan risk).

**Organization**: grouped by the 3 user stories. One skill (SKILL.md + a reference) + the registrations
span all three; each story turns specific assertions green.

## Format: `[ID] [P?] [Story] Description`

## Path Conventions

Kit skill — no `src/`. New: `.claude/skills/agent-architect/SKILL.md`,
`.claude/skills/agent-architect/references/decision-routine.md`, `tests/test_agent_architect.py`.
Edits: `.claude/skills/idea-to-app/SKILL.md`, `AGENTS.md`, `SKILL-MAP.md`.

---

## Phase 1: Setup

- [x] T001 Confirm `pytest -q` is green from repo root (known-green baseline before adding the guard).

---

## Phase 2: Foundational (Blocking — write the failing guard)

**⚠️ CRITICAL**: write the test first; no skill content until it fails.

- [x] T002 Write `tests/test_agent_architect.py` (pattern from `tests/test_token_quick_wins.py`: pure
  pathlib reads) with 7 assertions:
  T1 `SKILL.md` exists + frontmatter `name: agent-architect` + non-empty `description`;
  T2 `SKILL.md` contains the non-negotiable rules — decline-if-no-AI, Haiku model-routing, managed-vs-API
  as *suggest (owner decides)*, grill-by-default, scaffolding-deferred reminder;
  T3 `SKILL.md` references `ai-feature-checklist.md`;
  T4 `references/decision-routine.md` exists with a worked golden example;
  T5/T6 `agent-architect` registered in `AGENTS.md` + `SKILL-MAP.md`;
  T7 `idea-to-app/SKILL.md` references `agent-architect` (wired into the AI-inside gate).
- [x] T003 Run `pytest tests/test_agent_architect.py` → CONFIRM all FAIL (skill absent). Fail-loud: if
  any pass before content exists, fix the assertion.

---

## Phase 3: User Story 1 - Concrete agent design from an idea (Priority: P1) 🎯 MVP

**Goal**: SKILL.md emits a recommended design (agent count, model per agent w/ Haiku routing, diagram)
and declines for non-AI apps.

**Independent Test**: `pytest tests/test_agent_architect.py -k "T1 or T2"` passes; AND an eye-check
confirms the routine produces agent count + per-agent model (≥1 Haiku with reason) + a diagram, and a
decline path for non-AI apps.

- [x] T004 [US1] Write `.claude/skills/agent-architect/SKILL.md` — frontmatter + trigger; the decision
  routine steps 1-4 + 7 (AI-inside precheck/decline, identify jobs, orchestrator+subagent-per-job,
  model-per-agent with Haiku-routing rule + reason, text diagram). Make T1 pass; partial T2.
- [x] T005 [US1] Run `pytest tests/test_agent_architect.py -k "T1"` → green.

**Checkpoint**: core design routine exists.

---

## Phase 4: User Story 2 - Pre-filled checklist + managed-vs-API suggestion (Priority: P2)

**Goal**: output the 13-factor checklist pre-ticked-with-reasons + a managed-vs-API suggestion (owner
decides).

**Independent Test**: `pytest tests/test_agent_architect.py -k "T2 or T3"` passes; eye-check confirms
all 13 factors get tick+reason or N/A+reason and managed-vs-API is phrased suggest-not-decide.

- [x] T006 [US2] In `SKILL.md`, add routine steps 5-6 + 8: managed-vs-API suggestion rule (suggest with
  reason, owner decides), the 13-factor pre-fill recipe referencing `docs/ai-feature-checklist.md`, and
  the scaffolding-deferred reminder. Make T2 + T3 pass.
- [x] T007 [US2] Write `.claude/skills/agent-architect/references/decision-routine.md` — the detailed
  recipe + a worked golden example ("research → draft → email": orchestrator + 3 subagents,
  classify→Haiku, email→Managed Agent, checklist filled, diagram). Make T4 pass.
- [x] T008 [US2] Run `pytest tests/test_agent_architect.py -k "T2 or T3 or T4"` → green.

**Checkpoint**: recommendation is decision-ready.

---

## Phase 5: User Story 3 - Grill-by-default + wiring + registration (Priority: P3)

**Goal**: design is pressure-tested by default; skill is wired into the gate and registered (portability).

**Independent Test**: `pytest tests/test_agent_architect.py -k "T5 or T6 or T7"` passes; eye-check
confirms SKILL.md offers+runs grill-me by default and skips on explicit decline.

- [x] T009 [US3] In `SKILL.md`, add routine step 9: offer + run `grill-me` by default, skip on explicit
  decline (FR-005). (Covered by T2's grill-by-default check.)
- [x] T010 [P] [US3] Wire into `.claude/skills/idea-to-app/SKILL.md` GATE 3/5: when AI-inside=YES,
  invoke `agent-architect`. Make T7 pass.
- [x] T011 [P] [US3] Register `agent-architect` in `AGENTS.md` (skill list + AI-inside paragraph
  pointer). Make T5 pass.
- [x] T012 [P] [US3] Register `agent-architect` in `SKILL-MAP.md` (one row: designing an AI app's
  agents → agent-architect). Make T6 pass.
- [x] T013 [US3] Run full `pytest tests/test_agent_architect.py` → all 7 green.

**Checkpoint**: wired, registered, portable.

---

## Phase 6: Polish & Cross-Cutting

- [x] T014 [P] Full suite `pytest -q` + `ruff check .` → green (no regression).
- [x] T015 Behavior verify: run the skill on a sample AI-app idea + a non-AI idea; eye-check SC-001/002/
  003/004/005 (design+routing+diagram; checklist filled; suggest-not-decide; declines non-AI; grills).
- [x] T016 `powershell -File scripts\check-plan.ps1 -Gate` → PASS.
- [x] T017 Update `HANDOFF.md` (built list + recent decision) + `docs/superpowers/...map` (B = built).

---

## Dependencies & Execution Order

- T001 → T002–T003 (failing guard) → blocks stories.
- US1 (T004–T005) before US2/US3 (same SKILL.md file → sequence the writes: T004 → T006 → T009).
- T010/T011/T012 are [P] (different files) after the skill exists.
- Polish after all stories.

## Notes

- One SKILL.md → sequence its writes (T004 → T006 → T009); [P] tasks are separate files.
- TDD: T002–T003 prove red before content.
- Behavior quality is eye-checked (T015), not unit-tested — documented plan limitation.
- No deploy, no DB, no secrets — security review expected clean. Skill is recommendation-only (no code-gen).
