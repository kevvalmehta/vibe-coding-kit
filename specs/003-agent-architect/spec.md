# Feature Specification: Agent-Architect

**Feature Branch**: `003-agent-architect`

**Created**: 2026-06-10

**Status**: Draft

**Input**: User description: "Evolution B — Agent-Architect. A skill that, given an AI-containing app idea, proposes a concrete agent design (how many agents, which model per agent, managed-agent vs Messages API, where the human-approval gates go) plus a pre-filled 12-factor checklist, during /speckit-specify → /speckit-plan. Turns the passive docs/ai-feature-checklist.md into an active recommendation."

## Overview

Today, when the owner describes an app that *contains AI* (a chatbot, an agent, an LLM feature), the
kit has the right *decisions* written down in `docs/ai-feature-checklist.md` — but nothing **proposes
the agent structure**. The owner has to read the checklist and design it themselves. `Agent-Architect`
is a skill that reads an AI-app idea and emits an **opinionated, grounded recommendation**: how many
agents, one model per agent (routing cheap/mechanical jobs to Haiku), managed-agent vs Messages API
(suggested with a reason, owner decides), and where the human-approval gates belong — plus the
12-factor checklist pre-ticked with reasons, and a simple text diagram.

It is **recommendation-only** in v1 (no code generation / scaffolding). It plugs into the existing
AI-inside gate so it runs during `specify` + `plan`, and by default it offers to pressure-test the
proposed design with `grill-me`. Like every kit skill, it only *proposes*; the owner still approves
the spec/plan, and no runtime agent is built outside the normal pipeline.

### Resolved design decisions (from the brainstorm, 2026-06-10)

- **Output scope:** recommendation only (diagram + rationale + pre-ticked checklist). NO scaffolding
  in v1. The skill must REMIND the owner that scaffolding is a deferred next step when it is first
  used on a real build.
- **Managed vs Messages API:** suggest one with a plain-English reason; the owner decides. Never
  silently pick.
- **grill-me:** grill by default — after proposing, strongly offer + run `grill-me`; skip only if the
  owner explicitly declines.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Get a concrete agent design from an AI-app idea (Priority: P1)

The owner describes an AI-containing app in plain English. The skill identifies the distinct jobs the
app does and proposes a concrete agent architecture: number of agents (orchestrator + focused
subagents), one model per agent with cheap/mechanical jobs routed to Haiku, and a simple text diagram.
This is the MVP — the core "designs the agent system for you" value.

**Why this priority**: This is the whole point of the skill — turning an idea into a proposed
structure. Everything else (checklist, managed-vs-API, grilling) decorates this core output.

**Independent Test**: Give the skill a 3-job AI-app idea (e.g. "research a topic, draft a post, email
it"); confirm it returns a recommended agent count, a model per agent (with at least the mechanical
job routed to the cheap tier and a stated reason), and a readable diagram — all in plain English.

**Acceptance Scenarios**:

1. **Given** an AI-app idea with multiple distinct jobs, **When** the skill runs, **Then** it proposes
   an orchestrator + one focused subagent per job (small, focused agents — 12-factor #10), not one
   giant agent.
2. **Given** a job that is mechanical (classify, extract, format), **When** the design is proposed,
   **Then** that job's agent is routed to the cheap (Haiku) tier with a one-line reason, while
   judgment jobs stay on the default tier.
3. **Given** an idea that is NOT an AI app (ordinary CRUD), **When** the skill is considered, **Then**
   it declines / hands back ("no AI inside — skip Agent-Architect"), matching the existing AI-inside
   gate.

---

### User Story 2 - Pre-filled 12-factor checklist + managed-vs-API suggestion (Priority: P2)

Alongside the design, the skill outputs the 13-point checklist from `docs/ai-feature-checklist.md`
**pre-ticked with reasons** for this specific app, and a **suggestion** of managed-agent vs Messages
API with a plain-English why — leaving the final choice to the owner.

**Why this priority**: This is what makes the recommendation trustworthy and decision-ready — it shows
the owner the design honors the kit's existing AI rules and surfaces the one big infrastructure choice
without hiding it.

**Independent Test**: For the same idea, confirm the output addresses each of the 13 checklist factors
(tick + reason, or "N/A + why") and contains a managed-vs-API recommendation phrased as a suggestion
("recommend X because …") with the decision left to the owner.

**Acceptance Scenarios**:

1. **Given** a proposed design, **When** the checklist is emitted, **Then** every one of the 13 factors
   has a tick-with-reason or an explicit "doesn't apply because …".
2. **Given** a job that is long-running / async, **When** managed-vs-API is suggested, **Then** the
   skill recommends a Managed Agent with a reason, but states the owner decides.
3. **Given** a simple one-prompt-in-one-answer feature, **When** managed-vs-API is suggested, **Then**
   it recommends the plain Messages API with a reason.

---

### User Story 3 - Pressure-test the design with grill-me by default (Priority: P3)

After presenting the design, the skill strongly offers — and by default runs — `grill-me` to poke
holes in the proposed agent architecture before the owner accepts it. The owner can decline.

**Why this priority**: Quality gate. It catches weak designs early, but it is layered on top of the
core recommendation, so it is lowest priority.

**Independent Test**: After a design is proposed, confirm the skill offers grilling, proceeds to grill
by default (asking design-focused questions), and stops/skips cleanly when the owner says "no".

**Acceptance Scenarios**:

1. **Given** a freshly proposed design, **When** the skill finishes presenting it, **Then** it offers
   to run `grill-me` on the design and proceeds by default.
2. **Given** the owner explicitly declines, **When** they say "skip the grilling", **Then** the skill
   skips it and proceeds without grilling.

---

### Edge Cases

- **Not an AI app:** the skill must recognize an ordinary app (no LLM) and decline, deferring to the
  normal pipeline — no agent design forced onto a CRUD app.
- **Single-job AI app:** if there is genuinely one job, it should propose ONE small agent, not invent
  extra agents to look sophisticated (Simple + Surgical).
- **First real use:** the skill must surface the deferred-scaffolding reminder so the owner knows code
  generation is a future step, not part of this output.
- **Owner declines grilling:** must skip cleanly, not nag.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The skill MUST take a plain-English AI-app idea and output a recommended agent design:
  agent count (orchestrator + focused subagents), one model per agent, and a simple text diagram.
- **FR-002**: The skill MUST route mechanical jobs (classify / extract / format) to the cheap (Haiku)
  tier with a stated reason, and keep judgment jobs on the default tier.
- **FR-003**: The skill MUST output the 13-point `docs/ai-feature-checklist.md` factors pre-filled for
  the specific app (tick + reason, or explicit N/A + reason).
- **FR-004**: The skill MUST suggest managed-agent vs Messages API with a plain-English reason and
  LEAVE the decision to the owner (never silently choose).
- **FR-005**: The skill MUST, after presenting the design, offer + run `grill-me` by default to
  pressure-test it, and skip only on explicit owner decline.
- **FR-006**: The skill MUST be recommendation-only — it MUST NOT generate code / scaffold agent files
  in v1, and MUST surface a reminder that scaffolding is a deferred next step on first real use.
- **FR-007**: The skill MUST decline / hand back for non-AI apps (no LLM inside), consistent with the
  existing AI-inside gate.
- **FR-008**: The skill MUST be registered in `AGENTS.md` + `SKILL-MAP.md` and be plain-markdown
  LLM-portable (any AI tool can follow `SKILL.md`) — constitution Hard Rule VI; not "done" otherwise.
- **FR-009**: The skill MUST plug into the AI-inside gate so it is invoked during `specify` + `plan`
  for AI apps (wired via `idea-to-app`'s existing AI-inside check).

### Key Entities

- **Agent-Architect skill**: `.claude/skills/agent-architect/` — `SKILL.md` + any reference files
  (the decision routine, the recommendation/diagram format, the checklist-fill recipe).
- **Recommendation output**: the proposed design (agents, models, diagram), the pre-filled 13-factor
  checklist, the managed-vs-API suggestion, and the grill-me offer.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Given a multi-job AI-app idea, the skill produces a design naming an agent count, a model
  per agent (≥1 routed to the cheap tier with a reason), and a readable diagram — verifiable by reading
  the output.
- **SC-002**: 100% of the 13 checklist factors appear in the output with either a tick+reason or an
  explicit N/A+reason.
- **SC-003**: The managed-vs-API output is phrased as a suggestion-with-reason AND states the owner
  decides — never a silent pick.
- **SC-004**: For a non-AI (CRUD) idea, the skill declines and defers to the normal pipeline.
- **SC-005**: The skill offers + runs grill-me by default and skips on explicit decline (both paths
  demonstrated).
- **SC-006**: The skill is registered in `AGENTS.md` + `SKILL-MAP.md` and is plain-markdown portable
  (Hard Rule VI) — otherwise the feature is not done.

## Assumptions

- "Skill" here means the same plain-markdown `.claude/skills/<name>/SKILL.md` pattern every other kit
  skill uses (idea-to-app, autopilot, grill-me) — LLM-portable, no engine.
- The 12-factor knowledge and the managed-vs-API guidance ALREADY exist in
  `docs/ai-feature-checklist.md`; this skill turns them into an active recommender, it does not
  re-research them.
- Recommendation-only v1; scaffolding (prompt files, tool stubs) is explicitly deferred (tracked).
- The skill is invoked via the existing AI-inside gate in `idea-to-app` (no new gating engine).
- No application code, no database, no deployment — this is a kit skill (markdown + maybe a tiny
  helper), built and verified like the other skills.
