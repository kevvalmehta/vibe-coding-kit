# Quickstart — Validating Autopilot

These scenarios ARE the spec's Independent Tests. Run them by hand (the prose-orchestration
parts) plus `pytest` (the deterministic helper). Each maps to a user story / FR.

## Prerequisites

- On a feature branch (not `main`).
- Python 3.11+ available (`uv`/system python) for the helper tests.

## A. Helper unit tests (automated — TDD target)

```bash
pytest tests/test_autopilot_state.py -v
ruff check scripts/autopilot_state.py
```

**Expected**: all tests green; ruff clean. Covers: empty feature dir → `specify`;
spec+plan present, no tasks → `tasks`; clarify auto-skip when no markers; missing
prerequisite → earliest gap is `current` + a warning. (Story 1 resume, FR-004.)

## B. Guided stop-at-every-step run (Story 1 / FR-001,002,003)

1. Start Autopilot on a trivial idea ("a page that shows today's date").
2. **Expect**: it runs specify, prints a plain-English summary, and STOPS before clarify.
3. Reply with a vague message ("hmm ok sure maybe").
4. **Expect**: it asks ONE yes/no to confirm — does NOT advance.
5. Reply "change the title to X".
6. **Expect**: it revises the spec and STOPS again at specify (no advance).
7. Reply "go".
8. **Expect**: it advances to the next step.

## C. Resume cold (Story 1 / FR-004, SC-005)

1. After step B, close the session.
2. Reopen; run Autopilot with no idea.
3. **Expect**: it reads HANDOFF + the spec dir, states the current step correctly, continues.

## D. Parallel competing plans (Story 2 / FR-005, SC-003, SC-007)

1. Drive Autopilot to the PLAN step on an idea with more than one reasonable design.
2. **Expect**: 2-3 candidate architectures produced in parallel, a judge picks one with a
   stated reason, and the owner sees winner + rejected options + any grafted ideas.
3. **Expect (failure path)**: if one candidate subagent returns nothing, it proceeds with
   the survivors and SAYS one was dropped (no silent truncation, FR-010).

## E. Combined pre-PR report (Story 3 / FR-006, SC-004)

1. On a branch with a known issue, run Autopilot's PRE-PR step.
2. **Expect**: ONE report showing both verify and security results.
3. **Expect**: a failure in either is flagged plainly and Autopilot STOPS — no PR opened
   or suggested as automatic.

## F. Refusal of push/merge/deploy (FR-009, SC-006)

1. Ask Autopilot to "push this" or "merge to main".
2. **Expect**: it declines and points to the manual git-safety flow. No remote/main action.

## G. Portability (FR-011)

1. Confirm `AGENTS.md` and `SKILL-MAP.md` list Autopilot with its manual fallback.
2. Read `SKILL.md` as a non-Claude tool would: the steps are followable manually in order.
