# Implementation Plan: Autopilot Workflow Orchestrator

**Branch**: `feat/autopilot-orchestrator` | **Date**: 2026-06-10 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/001-autopilot-orchestrator/spec.md`

## Summary

Autopilot is a Claude Code **skill** (plain-markdown `SKILL.md`) that runs the kit's
existing planning sequence (specify → clarify → plan → tasks → pre-PR checks) as one
guided flow, stopping for owner approval at every step (v1 default; v2 added opt-in
`big-3` / `auto` gate modes). The
orchestration itself is prose the agent follows. Two deterministic concerns are pulled
OUT of the prose into a small, unit-tested Python helper: (1) "which step are we on?"
(resume logic) and (2) the fixed step order. The two heavy steps use **parallel `Agent`
subagent calls** — at PLAN, 2-3 architecture drafts + 1 judge; at PRE-PR, verify +
security-review at once — with mechanical sub-work routed to the cheaper model tier.
No new external tool or install (no ruflo). Build, push, merge, and deploy stay manual.

## Technical Context

**Language/Version**: Python 3.11+ for the deterministic helper (`autopilot_state.py`);
Markdown for the skill itself. (Kit default stack is Python; CI already runs ruff + pytest.)

**Primary Dependencies**: None beyond the Python standard library for the helper. The skill
uses only Claude Code built-ins already present: the `Agent` tool (subagents), model tiers
(Haiku/Sonnet/Opus), and the existing `/speckit-*`, `/verify`, `/security-review` skills.

**Storage**: None new. Run state is DERIVED from existing artifacts — the feature's
`specs/<id>/` directory contents + the Autopilot section of `HANDOFF.md`. No hidden store
(honors constitution "one source of truth for state").

**Testing**: pytest for `autopilot_state.py` (TDD). Behavioral validation of the prose
orchestration is by the scripted scenarios in `quickstart.md` (the spec's Independent Tests),
since prose-skill behavior is not unit-testable.

**Target Platform**: Claude Code (primary). Non-Claude tools (Codex/Cursor) follow the same
`SKILL.md` steps manually where parallel-subagent automation is unavailable (portability rule).

**Project Type**: Developer-tooling skill inside this kit (not a user-facing app).

**Performance Goals**: The two parallel steps complete in ~the time of the slowest single
subagent, not the sum (SC-007). Token cost reduced by routing mechanical sub-work to Haiku.

**Constraints**: Must never push/merge/deploy (FR-009). Must fail loud — never report a step
done if a sub-step was skipped or a subagent failed (FR-010). Must be resumable cold (FR-004).

**Scale/Scope**: One skill, one small Python helper + its tests, edits to 3 existing docs
(AGENTS.md, SKILL-MAP.md, guide skill) + HANDOFF.md. Drives one feature at a time.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **I. Plan Before Code** — PASS. This plan precedes any skill/helper code; spec approved upstream.
- **II. TDD** — PASS WITH SCOPE NOTE. All *deterministic* logic (`autopilot_state.py`: step
  order + resume detection) is built test-first with pytest. Prose orchestration and
  subagent fan-out cannot be unit-tested; they are validated by `quickstart.md` scenario
  runs that map 1:1 to the spec's Independent Tests. Documented in Complexity Tracking.
- **III. Never Break Working Code** — PASS. Work is on `feat/autopilot-orchestrator`. The
  change ADDS a skill + helper and makes small additive edits to AGENTS.md / SKILL-MAP.md /
  guide. Full existing test suite must stay green; fresh-context review before merge.
- **IV. Security First** — PASS. No user input, no secrets, no DB. The skill's only "power"
  is invoking other (already-trusted) skills; it explicitly REFUSES push/merge/deploy, which
  reduces risk vs. the status quo. `/security-review` still runs on the diff before merge.
- **V. Simplicity & Surgical** — PASS. No new install; reuses existing skills and Claude
  built-ins. v1 uses parallel `Agent` calls instead of authoring Workflow scripts (less
  machinery). One gate mode only. Helper is minimal.
- **VI. LLM Portability** — PASS (enforced by FR-011/FR-012 + Phase 1 tasks): register in
  AGENTS.md + SKILL-MAP.md; SKILL.md is plain markdown runnable manually; parallel-subagent
  automation has a documented manual fallback for non-Claude tools.

**Result**: PASS. One justified scope note on TDD (below). No unjustified violations.

## Project Structure

### Documentation (this feature)

```text
specs/001-autopilot-orchestrator/
├── plan.md              # This file
├── spec.md              # Feature spec
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output (validation scenarios = Independent Tests)
├── contracts/
│   └── autopilot-skill-contract.md   # The skill's invocation + behavior contract
└── checklists/
    └── requirements.md  # Spec quality checklist (done)
```

### Source Code (repository root)

```text
.claude/skills/autopilot/
├── SKILL.md             # The orchestrator: fixed step order, stop-at-every-step gates,
│                        #   plain-English summaries, change-vs-go handling, resume, refusals
└── references/
    ├── gates.md         # Exact gate behavior + the go / change / ambiguous reply rules
    ├── parallel-plan.md # The PLAN fan-out recipe (2-3 Agent drafts + 1 judge, Haiku routing)
    └── prepr-checks.md  # The PRE-PR recipe (verify + security-review in parallel → one report)

scripts/
└── autopilot_state.py   # Deterministic: fixed STEP_ORDER + "current step" from artifacts

tests/
└── test_autopilot_state.py   # pytest — TDD target (written FIRST)
```

Edits to existing files (additive):
- `AGENTS.md` — register Autopilot + its manual fallback (portability).
- `SKILL-MAP.md` — add the "want to run the whole planning flow → autopilot" row.
- `.claude/skills/guide/SKILL.md` — point the mentor at Autopilot as the guided-run option.
- `HANDOFF.md` — Autopilot owns/updates a small "current step" section.

**Structure Decision**: A skill folder under `.claude/skills/autopilot/` (matches every
other kit skill) + one Python helper in `scripts/` with tests in `tests/` (matches the kit's
Python TDD + CI). No app source tree — this is tooling, not a deployed application.

## Background Work

None. Autopilot runs only when the owner invokes it; nothing runs on a schedule or in the
background.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| TDD does not cover the prose orchestration / subagent fan-out (only the Python helper is unit-tested) | A skill's core *is* natural-language instructions the agent follows; there is no function to assert on. | Faking unit tests around prose would be a test that "can't fail when logic changes" (constitution Rule 9 anti-pattern). Instead, all deterministic logic is extracted into `autopilot_state.py` and fully TDD'd, and behavior is validated by `quickstart.md` scenarios that equal the spec's Independent Tests. This is the honest maximum coverage. |
