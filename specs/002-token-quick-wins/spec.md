# Feature Specification: Token Quick-Wins

**Feature Branch**: `002-token-quick-wins`

**Created**: 2026-06-10

**Status**: Draft

**Input**: User description: "Adopt 6 token quick-wins to make every Claude Code session in this kit cheaper, without changing what gets built: (1) model routing to Haiku for mechanical sub-work; (2) proactive /compact; (3) /recap on resume; (4) scope-bound prompts; (5) caveman mode; (6) prompt caching on system prompts for AI features built with the kit."

## Overview

The kit's owner pays per token. Many tokens are spent on work that does not need a premium model
or full context — mechanical summarizing, bloated context that was never compacted, re-reading whole
files when only a slice is needed, verbose responses. This feature adopts six low-effort habits and
small config changes that lower the token cost of every session **without changing what gets built
or the quality of the planning workflow**. It is mostly documentation + a small amount of config; no
new application code and no change to the spec→plan→tasks→build sequence.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - The six wins are documented as a usable habits guide (Priority: P1)

The owner (non-technical) opens one short reference and learns, in plain English, what each of the
six token wins is, when it kicks in, and what they personally need to do (often nothing — some are
automatic). This is the MVP: even with zero config wiring, having the six wins written down in one
place that any AI tool can read delivers the core value (cheaper sessions through known habits).

**Why this priority**: The wins are "mostly habits." A habit only saves tokens if it is written
down where the owner and every AI tool will see it. Documentation is the irreducible core.

**Independent Test**: Open the habits doc; confirm all six wins are present, each with a plain-English
"what / when / what you do" line, and that it is referenced from the kit's portability files so a
fresh session (Claude or other tool) discovers it.

**Acceptance Scenarios**:

1. **Given** a fresh session in any AI tool, **When** the owner reads the habits doc, **Then** they
   can state, for each of the six wins, what it does and whether they need to act.
2. **Given** the habits doc exists, **When** a session checks the portability files
   (`AGENTS.md` / `SKILL-MAP.md` / `HANDOFF.md`), **Then** the doc is registered and discoverable
   (LLM-portability Hard Rule satisfied).

---

### User Story 2 - The automatic wins are wired into config / kit defaults (Priority: P2)

The wins that can be made automatic are wired so they happen without the owner remembering:
model routing to Haiku for mechanical sub-work, and prompt caching on system prompts for any AI
feature the kit builds. Where the kit already does this (e.g. Autopilot already routes mechanical
work to Haiku), the spec records it as "already in place" rather than re-implementing it.

**Why this priority**: Automatic wins survive forgetfulness, but they depend on the documentation
existing first and must not change behavior or output quality.

**Independent Test**: Inspect the relevant config / skill defaults; confirm mechanical sub-work is
routed to the cheap tier and system-prompt caching is the documented default for AI features, with
judgment work left on the default tier.

**Acceptance Scenarios**:

1. **Given** a mechanical sub-task (classify / summarize / format), **When** the kit's guidance is
   followed, **Then** it is routed to the Haiku tier while judgment stays on the default tier.
2. **Given** an AI feature built with the kit that has a system prompt, **When** it is designed,
   **Then** prompt caching on the system prompt is the documented default.

---

### User Story 3 - Resume + scope habits reduce wasted context (Priority: P3)

The owner has clear, repeatable habits for the manual wins: run `/recap` when resuming a session,
trigger `/compact` at natural breakpoints before context bloats, write scope-bound prompts that name
only the files/scope needed, and keep caveman mode available to cut output verbosity.

**Why this priority**: These depend on the owner acting, so they are lower priority than automatic
wins, but they meaningfully cut tokens across long sessions.

**Independent Test**: Follow the habits doc to resume a session with `/recap`, compact mid-session,
and write one scope-bound prompt; confirm each step is described well enough that a non-technical
owner can do it unaided.

**Acceptance Scenarios**:

1. **Given** a resumed session, **When** the owner follows the doc, **Then** they run `/recap` (or its
   documented equivalent) and get oriented without re-reading the whole history.
2. **Given** a long session approaching context bloat, **When** a natural breakpoint is reached,
   **Then** the doc tells the owner (or the agent) to `/compact`.

---

### Edge Cases

- What happens when a "win" is already in place (e.g. Autopilot already routes to Haiku, caveman mode
  already installed)? → The spec/doc records it as already-adopted and does not duplicate it.
- What happens if a quick-win is Claude-only (e.g. `/compact`, `/recap` are Claude Code commands)? →
  Per the LLM-portability Hard Rule, the doc must give a plain-markdown manual fallback for other
  tools (e.g. "summarize and start a fresh thread").
- What happens if routing mechanical work to Haiku degrades output? → Routing applies ONLY to
  mechanical sub-work; any judgment work stays on the default tier. Quality must not change.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The kit MUST include a single plain-English habits reference (a short doc) describing
  all six token wins, each with what it does, when it applies, and what the owner must do (including
  "nothing — automatic" where true).
- **FR-002**: For each win that is Claude-Code-specific, the doc MUST provide a manual fallback for
  non-Claude tools (LLM-portability Hard Rule).
- **FR-003**: The habits doc MUST be registered in the kit's portability files (`AGENTS.md` and
  `SKILL-MAP.md`) and pointed to from `HANDOFF.md`, so any session discovers it.
- **FR-004**: Model-routing guidance MUST route mechanical sub-work (classify / summarize / format)
  to the cheap (Haiku) tier and keep judgment work on the default tier; where already implemented
  (Autopilot), the doc MUST reference it rather than duplicate it.
- **FR-005**: Prompt caching on system prompts MUST be documented as the default for AI features the
  kit builds, cross-referenced from `docs/ai-feature-checklist.md`.
- **FR-006**: The change MUST NOT alter the planning workflow (spec→plan→tasks→build), any skill's
  decision logic, or output quality — it only adds habits/config that reduce token use.
- **FR-007**: The change MUST be surgical: no new application code beyond small config/doc edits, and
  no edits to working skills' behavior.

### Key Entities

- **Habits doc**: A new reference (e.g. `docs/token-quick-wins.md`) holding the six wins, each as a
  what/when/do entry with a portability fallback where needed.
- **Portability registrations**: Lines added to `AGENTS.md` + `SKILL-MAP.md` + `HANDOFF.md` pointing
  to the habits doc.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All six token wins are present in one doc, each with a plain-English what/when/do entry
  a non-technical owner can act on without help.
- **SC-002**: 100% of Claude-only wins in the doc have a written non-Claude fallback.
- **SC-003**: The habits doc is registered in `AGENTS.md` + `SKILL-MAP.md` and referenced from
  `HANDOFF.md` (LLM-portability Hard Rule satisfied — feature is not "done" otherwise).
- **SC-004**: The planning workflow and all existing skills behave identically before and after this
  change (no behavioral diff; verified by the existing test/lint suite staying green).
- **SC-005**: Mechanical sub-work routing to the cheap tier is either newly documented or confirmed
  already-in-place, with judgment work explicitly kept on the default tier.

## Assumptions

- "Adopt" means **document the habit + wire the config that is safely automatable**, not build a
  tool that enforces the habits. The owner wanted "zero/low build."
- `/compact`, `/recap`, caveman mode, and Haiku routing already exist as Claude Code / kit features;
  this feature adopts and documents them, it does not build them from scratch.
- Caveman mode is already installed in this kit (active this session); the doc records it as a win and
  explains the on/off toggle rather than re-installing it.
- The single habits doc lives under `docs/` to match the kit's existing reference layout
  (`docs/ai-feature-checklist.md`, `docs/superpowers/...`).
- No deployment, no database, no external service is involved.
