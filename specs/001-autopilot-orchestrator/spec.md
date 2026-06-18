# Feature Specification: Autopilot Workflow Orchestrator

**Feature Branch**: `feat/autopilot-orchestrator`

**Created**: 2026-06-10

**Status**: Draft

**Input**: User description: "Autopilot — a workflow orchestrator skill for this dev kit. It chains the existing spec-kit steps (specify → clarify → plan → tasks → pre-PR checks) so the non-technical owner presses 'go' instead of hand-running each skill. Default gate mode: STOP AT EVERY STEP and wait for explicit owner approval. At PLAN it fans out 2-3 subagents drafting competing architectures plus 1 judge. At PRE-PR it runs /verify and /security-review as parallel subagents and returns one combined report. Mechanical sub-steps route to Haiku; judgment stays on Opus/Sonnet. After each step it auto-updates HANDOFF.md. Built as a visible orchestrator skill using the Workflow tool only inside the heavy parallel steps. It NEVER pushes, merges, or deploys. Must be registered in AGENTS.md + SKILL-MAP.md."

## Overview

Autopilot is a guide-style skill that runs the kit's existing planning workflow as one
guided sequence, so a non-technical owner advances the project by approving each step
rather than remembering and hand-running each `/speckit-*` skill in the right order. It
adds no new planning logic — it orchestrates the skills that already exist, stops for
the owner at every step, speeds the two heavy steps with parallel subagents, keeps token
cost down by routing mechanical sub-work to a cheaper model, and keeps `HANDOFF.md`
current so any AI tool can resume cold.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Guided run with a stop at every step (Priority: P1)

The owner starts Autopilot on a feature idea. Autopilot states the current step, runs the
matching kit skill, shows the result in plain English, and **stops** — waiting for the
owner to say "go" before moving to the next step. The owner never has to remember which
`/speckit-*` skill comes next or in what order.

**Why this priority**: This is the core value — "press go instead of hand-driving." It is
also the safest mode (owner sees and approves everything), which is what the owner asked
for until the tool is trusted. Delivers a usable MVP on its own.

**Independent Test**: Start Autopilot on a trivial feature; confirm it runs specify, stops
for approval, and does not advance to clarify until the owner explicitly approves. Confirm
it can be stopped at any step and resumed later from the same step.

**Acceptance Scenarios**:

1. **Given** a feature idea and no spec yet, **When** the owner starts Autopilot, **Then**
   it runs the specify step, shows a plain-English summary, and stops for approval before
   clarify.
2. **Given** Autopilot is stopped at a step, **When** the owner says "go", **Then** it runs
   the next step in the fixed order (specify → clarify → plan → tasks → pre-PR checks).
3. **Given** Autopilot is stopped at a step, **When** the owner says "change X" instead of
   "go", **Then** it revises the current step's output and stops again — it does not advance.
4. **Given** the owner closes the session mid-run, **When** they reopen and start Autopilot,
   **Then** it reads HANDOFF.md / the spec directory and resumes at the correct step.

---

### User Story 2 - Parallel competing plans at the PLAN step (Priority: P2)

At the plan step, Autopilot produces several candidate architectures at once (via parallel
subagents), has a judge subagent score them, and presents the owner the winning plan plus
the best ideas borrowed from the runners-up — instead of a single first-draft plan.

**Why this priority**: Better plans with no extra waiting (candidates run in parallel).
High value but not required for a usable MVP, so P2.

**Independent Test**: Run Autopilot to the plan step on a feature with more than one
reasonable design; confirm it returns one recommended plan, a short note of the rejected
alternatives, and why the winner won — and that this still stops for owner approval.

**Acceptance Scenarios**:

1. **Given** the plan step, **When** Autopilot runs it, **Then** 2-3 candidate architectures
   are produced in parallel and a judge selects one with a stated reason.
2. **Given** the candidates differ, **When** the winner is chosen, **Then** the owner is
   shown the winner plus any superior ideas grafted from the runners-up.
3. **Given** a subagent fails or returns nothing, **When** the judge runs, **Then** Autopilot
   proceeds with the surviving candidates and tells the owner one candidate was dropped
   (no silent truncation).

---

### User Story 3 - One combined pre-PR check report (Priority: P2)

Before a pull request, Autopilot runs the verify check and the security review at the same
time (parallel subagents) and hands the owner a single combined report, instead of the
owner running and waiting on two separate checks.

**Why this priority**: Removes a tedious two-step manual wait and reduces the chance the
owner forgets one check. Valuable but not required for the core MVP, so P2.

**Independent Test**: Run Autopilot's pre-PR step on a branch with a known issue; confirm a
single report shows both the verify result and the security result, and that a failure in
either is clearly flagged and does NOT auto-proceed to a PR.

**Acceptance Scenarios**:

1. **Given** the pre-PR step, **When** Autopilot runs it, **Then** verify and security-review
   run in parallel and the owner receives one combined pass/fail report.
2. **Given** either check fails, **When** the report is shown, **Then** the failure is stated
   plainly and Autopilot stops — it does not open or suggest auto-opening a PR.

---

### Edge Cases

- **Owner gives an ambiguous reply** (neither clear "go" nor a clear change request):
  Autopilot asks one plain-English yes/no to confirm intent rather than guessing.
- **A required prior artifact is missing** (e.g. owner starts at plan with no spec):
  Autopilot refuses to skip, names the missing step, and offers to run it first.
- **A subagent errors or times out**: the step degrades gracefully (continue with what
  survived, report what was dropped); it never hangs silently or claims false success.
- **The owner tries to push/merge/deploy through Autopilot**: Autopilot declines and points
  them to the manual git-safety flow — these actions are out of scope by design.
- **HANDOFF.md is missing or malformed**: Autopilot still runs; it warns that resume context
  may be incomplete and recreates the section it owns rather than failing.
- **Run on a non-Claude tool (Codex/Cursor)**: the skill's plain-markdown instructions can
  be followed manually step-by-step even where the parallel-subagent automation is unavailable.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Autopilot MUST run the kit's planning steps in the fixed order
  specify → clarify → plan → tasks → pre-PR checks, using the existing kit skills for each
  step rather than reimplementing them.
- **FR-002**: Autopilot MUST stop after every step and wait for explicit owner approval
  before advancing (the v1 default and only mode). It MUST NOT advance on an ambiguous reply.
- **FR-003**: Autopilot MUST allow the owner to request a change to the current step's output;
  on a change request it MUST revise and stop again at the same step, not advance.
- **FR-004**: Autopilot MUST be resumable — on restart it MUST determine the correct current
  step from existing artifacts (HANDOFF.md and the feature's spec directory) and continue.
- **FR-005**: At the plan step, Autopilot MUST generate 2-3 candidate architectures in
  parallel and use a judge step to select one, presenting the winner, the rejected options,
  and the reason for the choice.
- **FR-006**: At the pre-PR step, Autopilot MUST run the verify and security-review checks in
  parallel and present a single combined report; a failure in either MUST stop the run.
- **FR-007**: Autopilot MUST route mechanical sub-work (classification, summarization,
  formatting) to a cheaper model tier and reserve the most capable tier for judgment, to
  reduce token cost.
- **FR-008**: Autopilot MUST update the section of HANDOFF.md it owns after each completed
  step, so any AI tool can resume cold.
- **FR-009**: Autopilot MUST NOT push to a remote, merge to main, or deploy. These remain
  manual, owner-controlled actions; Autopilot MUST decline such requests and redirect.
- **FR-010**: Autopilot MUST never report a step as complete if any sub-step was skipped or
  any subagent failed silently; it MUST surface what was skipped or dropped (fail loud).
- **FR-011**: Autopilot MUST be registered in `AGENTS.md` and `SKILL-MAP.md`, and its
  Claude-specific automation (parallel subagents) MUST have a documented manual fallback for
  non-Claude tools (LLM-portability hard rule).
- **FR-012**: Autopilot MUST be discoverable from the existing `/guide` mentor flow as the
  recommended way to run the planning sequence.

### Key Entities

- **Run state**: which feature is being driven and which step is current/next. Derived from
  existing artifacts (the feature's `specs/<id>/` directory + HANDOFF.md), not a new hidden
  store — consistent with the kit's "one source of truth for state" rule.
- **Step**: one stage in the fixed sequence, with a name, the kit skill it invokes, its
  output artifact, and whether it uses parallel subagents.
- **Combined check report**: the merged verify + security result presented at the pre-PR step.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The owner can take a feature idea from start through the full planning sequence
  by only approving or requesting changes at each step — without naming or recalling any
  individual `/speckit-*` skill.
- **SC-002**: Autopilot stops for owner approval at 100% of steps in v1 (zero steps auto-advance).
- **SC-003**: At the plan step the owner receives more than one candidate architecture and a
  stated reason for the chosen one, in a single guided step.
- **SC-004**: The pre-PR step returns one report covering both verify and security; neither
  check is silently skipped.
- **SC-005**: After any step, a fresh session (or a different AI tool) can read HANDOFF.md and
  correctly identify the current step and what to do next.
- **SC-006**: Autopilot never performs a push, merge, or deploy — verified by the absence of
  any such action in its flow and an explicit decline when asked.
- **SC-007**: The parallel steps (plan candidates, pre-PR checks) complete in roughly the time
  of the single slowest subagent, not the sum of running them one by one.

## Assumptions

- **Existing kit skills are the building blocks**: Autopilot calls `/speckit-specify`,
  `/speckit-clarify`, `/speckit-plan`, `/speckit-tasks`, `/verify`, and `/security-review`;
  it does not duplicate their logic. (Resolved decision in the workflow evolution map.)
- **v1 has one gate mode only — stop at every step.** A relaxed "big-3" or "auto" mode is an
  explicitly deferred future enhancement, not part of this spec.
- **Scope ends before build/push/merge.** Building the code (Superpowers TDD), pushing, and
  merging stay manual and owner-controlled. Autopilot covers the planning sequence plus the
  pre-PR check step only.
- **Parallel subagents and model routing use Claude Code's built-in `Agent`/`Workflow`
  tools and model tiers** (Haiku for mechanical work, Opus/Sonnet for judgment). No new
  external tool, framework, or install is introduced (no ruflo).
- **Non-Claude fallback**: where parallel-subagent automation is unavailable, the skill's
  plain-markdown steps can be run manually in order; the portability rule is satisfied by
  documenting this in AGENTS.md + SKILL-MAP.md.
- **`/guide` integration**: the existing mentor skill will point to Autopilot; deeper
  auto-routing changes to `/guide` are minimal and in scope only as a pointer.
