---

description: "Task list for Autopilot Workflow Orchestrator"
---

# Tasks: Autopilot Workflow Orchestrator

**Input**: Design documents from `specs/001-autopilot-orchestrator/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: INCLUDED — the constitution mandates TDD. The deterministic helper
(`scripts/autopilot_state.py`) is built test-first. Prose-orchestration behavior is
validated by the `quickstart.md` scenarios (the spec's Independent Tests), not unit tests.

**Organization**: Grouped by user story. Each story is an independently testable increment.

## Format: `[ID] [P?] [Story] Description`

## Path Conventions

Skill tooling lives at `.claude/skills/autopilot/`; the deterministic helper at `scripts/`;
its tests at `tests/`. No app source tree (this is kit tooling, not a deployed app).

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create the skill + helper scaffolding.

- [x] T001 Create the skill folder structure: `.claude/skills/autopilot/` and `.claude/skills/autopilot/references/`
- [x] T002 [P] Ensure `scripts/` and `tests/` exist at repo root (kit already has `scripts/`; create `tests/` if absent)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: The deterministic state helper — the resume logic every orchestration step relies on. TDD.

**⚠️ CRITICAL**: Write the tests FIRST and watch them FAIL before implementing T004.

- [x] T003 Write failing pytest cases in `tests/test_autopilot_state.py` covering the contract in `contracts/autopilot-skill-contract.md`:
  (a) missing/empty `feature_dir` → `current == "specify"`, `completed == []`;
  (b) `spec.md` + `plan.md` present, `tasks.md` absent → `current == "tasks"`;
  (c) `spec.md` with no open `[NEEDS CLARIFICATION]` markers → `clarify` counted complete;
  (d) `spec.md` present but with an open clarification marker → `current == "clarify"`;
  (e) prerequisite gap (e.g. `plan.md` exists but `spec.md` missing) → `current` is the earliest gap AND a warning is returned;
  (f) `STEP_ORDER == ["specify","clarify","plan","tasks","pre-pr-checks"]`.
- [x] T004 Implement `scripts/autopilot_state.py` (`get_current_step(...)` + `STEP_ORDER`) using only the Python stdlib, until T003 passes. Run `ruff check scripts/autopilot_state.py` clean.

**Checkpoint**: `pytest tests/test_autopilot_state.py -v` green; ruff clean. Resume logic is trustworthy.

---

## Phase 3: User Story 1 - Guided stop-at-every-step run (Priority: P1) 🎯 MVP

**Goal**: The owner advances a feature by approving each step; Autopilot runs the fixed
sequence, stops at every step, handles go/change/ambiguous, resumes cold, and refuses
push/merge/deploy.

**Independent Test**: On a trivial idea, Autopilot runs specify and STOPS before clarify;
a vague reply triggers one yes/no (no advance); "change …" revises and stops at the same
step; "go" advances. After a restart with no idea, it resumes at the correct step. (= quickstart B + C + F.)

- [x] T005 [US1] Write `.claude/skills/autopilot/SKILL.md`: name + description (triggers: "/autopilot", "run autopilot", "drive the planning", "press go"); the fixed STEP_ORDER; the stop-at-every-step gate as the only v1 mode; the plain-English per-step summary; the go / change / ambiguous-→-one-yes/no rules; the resume behavior (calls `python scripts/autopilot_state.py` to find the current step); the HARD refusals for push/merge/deploy with redirect to git-safety; the fail-loud rule (never report a step done if a sub-step was skipped). Reference `gates.md`.
- [x] T006 [P] [US1] Write `.claude/skills/autopilot/references/gates.md`: exact wording patterns counted as "go" vs "change" vs "ambiguous"; the single confirmation question; the missing-prerequisite refusal; the malformed-HANDOFF fallback.
- [x] T007 [US1] Add the HANDOFF.md upkeep instruction to SKILL.md: after each completed step, write/update a clearly delimited "Autopilot — current step" section in `HANDOFF.md` (own only that section; never rewrite the rest). Document the exact marker comment so the helper and a cold reader can find it.

**Checkpoint**: MVP — a full guided run with gates, resume, and refusals works (quickstart B, C, F pass).

---

## Phase 4: User Story 2 - Parallel competing plans at PLAN (Priority: P2)

**Goal**: At the PLAN step, produce 2-3 candidate architectures in parallel, judge them,
and present winner + rejected options + reason; drop-and-report on subagent failure.

**Independent Test**: Driving to PLAN on a multi-design idea yields >1 candidate, a stated
winner reason, and a note of any dropped candidate — still stopping for approval. (= quickstart D.)

- [x] T008 [P] [US2] Write `.claude/skills/autopilot/references/parallel-plan.md`: the fan-out recipe — spawn 2-3 `Agent` subagents in ONE message (each drafts a distinct architecture), then a judge subagent; route the complexity-classify + summary sub-steps to the Haiku model tier, keep drafting + judging on the default tier; on a subagent returning nothing, proceed with survivors and surface the drop (no silent truncation).
- [x] T009 [US2] Wire the PLAN step in `SKILL.md` to use `references/parallel-plan.md` instead of a single-shot plan, and to present winner + rejected + reason, then STOP for approval.

**Checkpoint**: US1 + US2 work; PLAN shows competing options.

---

## Phase 5: User Story 3 - Combined pre-PR check report (Priority: P2)

**Goal**: Run `/verify` and `/security-review` in parallel and present one combined report;
any failure stops the run and never suggests an automatic PR.

**Independent Test**: On a branch with a known issue, the PRE-PR step returns one report
covering both checks; a failure is flagged plainly and Autopilot stops. (= quickstart E.)

- [x] T010 [P] [US3] Write `.claude/skills/autopilot/references/prepr-checks.md`: run `/verify` and `/security-review` as parallel subagents; merge into one pass/fail report (format the merge via the Haiku tier); `overall = fail` if either fails → STOP, state the failure plainly, do NOT open or suggest auto-opening a PR.
- [x] T011 [US3] Wire the PRE-PR step in `SKILL.md` to use `references/prepr-checks.md` as the final step, then hand back to the owner for the manual build/PR decision.

**Checkpoint**: All three stories independently functional.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Portability registration (Hard Rule VI), discoverability, and final gates.

- [x] T012 [P] Register Autopilot in `AGENTS.md`: what it does, trigger words, and the
  manual fallback for non-Claude tools (follow SKILL.md step order by hand; run PLAN
  candidates + PRE-PR checks sequentially where parallel subagents are unavailable).
- [x] T013 [P] Add an Autopilot row to `SKILL-MAP.md` ("want to run the whole planning flow end-to-end → autopilot") and to the normal-order section.
- [x] T014 [P] Update `.claude/skills/guide/SKILL.md` to point the mentor at Autopilot as the guided-run option for the planning sequence.
- [x] T015 Run `pytest tests/test_autopilot_state.py` + `ruff check .` and confirm the full existing suite is still green (no regressions — constitution III).
- [x] T016 Execute every `quickstart.md` scenario (A–G) and record pass/fail; fix any gap. This is the behavioral acceptance for the prose orchestration.
- [x] T017 Run `powershell -File scripts\check-plan.ps1 -Gate` — must pass (no unchecked tasks, no vague Independent Tests) before merge.
- [x] T018 Run `/security-review` on the branch diff; confirm clean (no inputs/secrets/risky ops introduced).

---

## Dependencies & Execution Order

- **Setup (Phase 1)** → no deps.
- **Foundational (Phase 2)** → after Setup; BLOCKS all stories (resume logic).
- **US1 (Phase 3)** → after Phase 2. The MVP.
- **US2 (Phase 4)** and **US3 (Phase 5)** → after US1 (both edit `SKILL.md`'s step wiring, so they touch a shared file — do US2 then US3, not in parallel on SKILL.md). Their `references/*.md` files (T008, T010) ARE parallel-safe.
- **Polish (Phase 6)** → after the stories you intend to ship; T012–T014 parallel-safe; T015–T018 run last in order.

### Parallel Opportunities

- T006, T008, T010 (separate `references/*.md` files) can be drafted in parallel.
- T012, T013, T014 (separate files) can run in parallel.
- The PLAN-step and PRE-PR-step subagents run in parallel AT RUNTIME (that's the feature),
  but the tasks that WIRE them touch the shared `SKILL.md` → sequence T009 before/after T011.

---

## Implementation Strategy

### MVP First (User Story 1 only)
1. Phase 1 Setup → 2. Phase 2 Foundational (TDD helper) → 3. Phase 3 US1 →
**STOP and validate** quickstart B, C, F. A guided, gated, resumable, push-safe run is a
usable MVP on its own.

### Incremental Delivery
Add US2 (competing plans) → validate quickstart D. Add US3 (combined checks) → validate
quickstart E. Then Phase 6 (register for portability, run all gates). Each increment adds
value without breaking the previous.

---

## Notes
- [P] = different files, no dependencies.
- Commit after each task or logical group; never push/merge unattended (owner-controlled).
- The constitution's TDD applies fully to `autopilot_state.py`; the prose skill is validated
  by quickstart scenarios — do not fake unit tests around prose (Rule 9 anti-pattern).
- Autopilot itself must never push, merge, or deploy — verify this holds (T016 quickstart F).
