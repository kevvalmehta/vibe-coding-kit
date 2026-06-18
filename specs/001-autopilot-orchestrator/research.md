# Research — Autopilot Workflow Orchestrator

Phase 0. Resolves the open technical choices before design.

## Decision 1 — Fan-out mechanism: parallel `Agent` calls (not authored Workflow scripts)

- **Decision**: For the PLAN candidates and the PRE-PR checks, the skill instructs the
  agent to make **multiple `Agent` subagent calls in a single message** (parallel), then
  a follow-up judge/merge step.
- **Rationale**: Same parallelism as the `Workflow` tool, but no JavaScript workflow script
  to author, version, and maintain — simpler and more visible (constitution Rule V). The
  agent and owner can see each subagent invocation in the flow.
- **Alternatives considered**: The `Workflow` tool (deterministic fan-out + judge in one
  script). More powerful and resumable, but heavier for a 3-draft-plus-judge step and adds a
  code artifact. **Deferred** as a documented future optimization, not v1.
- **Supersedes** the earlier map-doc wording ("Workflow tool inside heavy steps"). Flagged
  per Rule 7 (surface conflicts, don't blend). Map doc + HANDOFF note this refinement.

## Decision 2 — Model routing tiers

- **Decision**: Route mechanical sub-work (classify the idea's complexity, summarize a
  subagent's output, format the combined report) to **Haiku**; keep architecture drafting,
  judging, and the verify/security reasoning on the default capable tier (Opus/Sonnet).
- **Rationale**: Industry-documented ~50% cost cut from tiered routing; Haiku ~15× cheaper
  for simple transforms. Matches constitution Rule 5 (model for judgment, code/cheap-model
  for mechanical work).
- **Alternatives considered**: All-Opus (simpler, ~2× cost). Rejected on cost. A code-only
  classifier (no model) for complexity — rejected: idea complexity is a judgment call, but a
  cheap one, so Haiku fits.

## Decision 3 — Resume / "which step are we on?"

- **Decision**: A deterministic Python helper `autopilot_state.py` reads the feature's
  `specs/<id>/` directory (which of spec.md / plan.md / tasks.md exist) plus the Autopilot
  marker section in `HANDOFF.md`, and returns the current step + next step from a fixed
  `STEP_ORDER` list.
- **Rationale**: Resume detection is a deterministic transform — constitution Rule 5 says
  code, not the model, should do it; and it gives a genuine TDD target (Rule II). One source
  of truth for state (no hidden store) — Factor 5 of the AI checklist.
- **Alternatives considered**: Let the model infer the step by reading files each time.
  Rejected — non-deterministic, untestable, and wastes tokens re-reading.

## Decision 4 — Gate handling (go / change / ambiguous)

- **Decision**: After every step, present a plain-English summary and stop. A clear "go"
  (or "yes"/"continue"/"next") advances; a change request revises the current step and stops
  again; **anything ambiguous triggers one yes/no confirmation**, never an auto-advance.
- **Rationale**: Owner asked for maximum control until tested (FR-002/FR-003). Fail-safe
  default = do not proceed (Rule 12 fail loud; AI checklist Factor 7 "asking a human is a tool").
- **Alternatives considered**: Heuristic intent-guessing on ambiguous replies. Rejected —
  risk of advancing without consent.

## Decision 5 — TDD scope for a prose skill

- **Decision**: Unit-test (pytest, test-first) ALL deterministic logic in
  `autopilot_state.py`. Validate prose orchestration + fan-out via `quickstart.md` scenarios
  that map 1:1 to the spec's Independent Tests.
- **Rationale**: There is no function to assert on for natural-language instructions; faking
  one violates Rule 9 (a test that can't fail when logic changes). Extracting the
  deterministic parts maximizes honest coverage.
- **Alternatives considered**: Skip tests entirely (violates Rule II). Snapshot-test the
  SKILL.md text (brittle, asserts wording not behavior). Both rejected.

## Decision 6 — No new dependency / no external harness

- **Decision**: Use only Claude Code built-ins + Python stdlib. Explicitly NOT adopting
  ruflo or any agent framework.
- **Rationale**: Constitution Rule V + the ruflo evaluation (alpha, audited fabrications).
  Map doc records the rejection.
