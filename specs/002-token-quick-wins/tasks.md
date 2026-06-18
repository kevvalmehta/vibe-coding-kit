---

description: "Task list — Token Quick-Wins"
---

# Tasks: Token Quick-Wins

**Input**: Design documents from `/specs/002-token-quick-wins/`

**Prerequisites**: [plan.md](plan.md) (required), [spec.md](spec.md) (user stories)

**Tests**: REQUIRED — "TDD always" is a Hard Rule and the winning architecture is a guard test. The
guard test (`tests/test_token_quick_wins.py`) is written failing-first, then made green file-by-file.

**Organization**: grouped by the 3 user stories from the spec. One shared doc + one guard test span
all three; each story turns specific assertions green.

## Format: `[ID] [P?] [Story] Description`

## Path Conventions

Kit/tooling change — no `src/`. New files: `docs/token-quick-wins.md`, `tests/test_token_quick_wins.py`.
Edits: `AGENTS.md`, `SKILL-MAP.md`, `HANDOFF.md`, `docs/ai-feature-checklist.md`.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Confirm the build harness; no scaffolding needed beyond what exists.

- [x] T001 Confirm `pytest` runs green on the existing suite from repo root (`pytest -q`) so the new
  guard test starts from a known-green baseline (SC-004 regression net).

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Write the guard test FIRST, all assertions failing — the TDD anchor for every story.

**⚠️ CRITICAL**: No story content is written until these tests exist and fail.

- [x] T002 Write `tests/test_token_quick_wins.py` (pattern from `tests/test_autopilot_state.py`:
  pure pathlib filesystem-string reads, no mocks/network) with all 7 assertions:
  T1 six wins present + ≥1 carries an "already-in-place" label;
  T2 each Claude-only win (compact, recap, caveman) has a fallback marker;
  T3/T4/T5 doc referenced in `AGENTS.md`/`SKILL-MAP.md`/`HANDOFF.md`;
  T6 `docs/ai-feature-checklist.md` cross-refs the prompt-caching win;
  T7 negative-space — habits doc embeds no planning-workflow *change* imperative.
- [x] T003 Run `pytest tests/test_token_quick_wins.py` and CONFIRM all 7 FAIL (doc absent). Record
  the failure output. (Fail-loud: if any pass before content exists, the assertion is wrong — fix it.)

**Checkpoint**: 7 failing assertions committed — TDD ready.

---

## Phase 3: User Story 1 - Six wins documented as a usable habits guide (Priority: P1) 🎯 MVP

**Goal**: One plain-English doc holding all six wins + fallbacks + already-on labels, registered in
the portability files so any session discovers it.

**Independent Test**: `pytest tests/test_token_quick_wins.py -k "T1 or T2 or T3 or T4 or T5"` passes
— i.e. doc has 6 wins, every Claude-only win has a fallback, and AGENTS.md + SKILL-MAP.md + HANDOFF.md
all reference `token-quick-wins`. Pass/fail is objective.

- [x] T004 [US1] Create `docs/token-quick-wins.md` with six entries, each as
  **What / When / You do / Status (already-in-place | new) / Non-Claude fallback**. Word the doc to
  LINK to workflow steps, never embed "do X before /speckit-*" imperatives (keeps T7 green). Make T1
  + T2 pass.
- [x] T005 [P] [US1] Register the doc in `AGENTS.md` (one line in the portability/cold-start list).
  Makes T3 pass.
- [x] T006 [P] [US1] Register the doc in `SKILL-MAP.md` (one habits-table row). Makes T4 pass.
- [x] T007 [P] [US1] Add a "what's built" pointer to the doc in `HANDOFF.md` (outside the
  AUTOPILOT-STATE markers). Makes T5 pass.
- [x] T008 [US1] Run `pytest tests/test_token_quick_wins.py -k "T1 or T2 or T3 or T4 or T5"` → all green.

**Checkpoint**: MVP — wins documented + discoverable. Portability Hard Rule satisfied.

---

## Phase 4: User Story 2 - Automatic wins wired into config / kit defaults (Priority: P2)

**Goal**: The safely-automatable wins (Haiku routing, prompt caching on system prompts) are recorded
as kit defaults; already-in-place ones referenced, not rebuilt.

**Independent Test**: `pytest tests/test_token_quick_wins.py -k T6` passes (ai-feature-checklist
cross-refs the prompt-caching win), AND a manual read confirms Win 1 (Haiku) is labelled
"already-in-place (Autopilot)" with judgment-stays-default stated.

- [x] T009 [US2] In `docs/token-quick-wins.md`, confirm Win 1 (model routing) is labelled
  already-in-place, citing Autopilot's Haiku routing, and explicitly states judgment work stays on
  the default tier (SC-005, FR-004). No new routing code (FR-007).
- [x] T010 [US2] Add one cross-reference sentence to `docs/ai-feature-checklist.md` at the
  prompt-caching factor pointing to Win 6 in the habits doc (FR-005). Makes T6 pass.
- [x] T011 [US2] Run `pytest tests/test_token_quick_wins.py -k T6` → green.

**Checkpoint**: Automatic wins documented as defaults; nothing rebuilt.

---

## Phase 5: User Story 3 - Resume + scope habits reduce wasted context (Priority: P3)

**Goal**: Clear, repeatable habits for the manual wins (`/recap`, `/compact`, scope-bound prompts,
caveman) a non-technical owner can follow unaided.

**Independent Test**: `pytest tests/test_token_quick_wins.py -k T7` passes, AND a non-author read of
wins 2,3,4,5 confirms each has an actionable "You do" line + (where Claude-only) a fallback a
non-Claude tool can follow.

- [x] T012 [US3] In `docs/token-quick-wins.md`, ensure wins 2 (/compact), 3 (/recap), 4 (scope-bound
  prompt template — include a copy-paste block), 5 (caveman toggle) each have a concrete "You do"
  line and the fallback required by portability. Keep wording link-not-imperative (T7).
- [x] T013 [US3] Run `pytest tests/test_token_quick_wins.py` (all 7) → green.

**Checkpoint**: All six wins actionable + portable.

---

## Phase 6: Polish & Cross-Cutting Concerns

- [x] T014 [P] Run the FULL suite `pytest -q` + `ruff check .` → green (SC-004: no regression, no
  behavior change to any skill/workflow).
- [x] T015 Run `powershell -File scripts\check-plan.ps1 -Gate` → confirms every task checked + every
  Independent Test measurable (plan↔build seam).
- [x] T016 Refresh the AUTOPILOT-STATE marker + recent-decisions note in `HANDOFF.md` (post-build state).

---

## Dependencies & Execution Order

- **Setup (T001)** → **Foundational (T002–T003: failing test)** → blocks all stories.
- **US1 (T004–T008)** = MVP. T005/T006/T007 are [P] (different files). T004 before T008.
- **US2 (T009–T011)** + **US3 (T012–T013)** edit the same doc as US1 → run AFTER US1's T004 to avoid
  same-file conflict; US2 and US3 are otherwise independent.
- **Polish (T014–T016)** after all stories.

### Parallel Opportunities

- T005, T006, T007 (three different registration files) run in parallel after T004.
- US2 and US3 content slices are independent once the doc exists (but edit one file — sequence the
  writes).

---

## Implementation Strategy

**MVP = US1**: baseline green (T001) → failing guard test (T002–T003) → write doc + register
(T004–T008). At that point the wins are documented, discoverable, and portability-compliant — shippable.
Then layer US2 (automatic-win defaults) and US3 (manual-win habits), full suite green, gate check.

## Notes

- One shared doc → sequence the per-story doc writes (T004 → T009 → T012) to avoid same-file conflict;
  the [P] tasks are the separate registration files.
- TDD: T002–T003 prove the test fails before content exists (fail-loud).
- No deploy, no DB, no secrets — security review expected clean.
