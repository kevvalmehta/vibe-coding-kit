# Feature Specification: `/start` — the Conductor (proactive front-door mentor)

**Feature Branch**: `009-conductor`

**Created**: 2026-06-25

**Status**: Draft

**Input**: User description: "A proactive front-door mentor that greets a non-technical owner, figures out what they want to build, and DRIVES the whole journey in plain English — weaving in the right skill/resource at each step — so even a beginner can build by talking to the kit."

## Context (plain English)

The owner's north star: **a non-technical person can build whatever they want by talking to the kit.**
Honest gap today: the kit has the tools (~80%) but not the guided experience (~25%) — "great kitchen,
no chef." The Conductor is the chef.

Crucially, it does **not** add a new pipeline. The kit already has `idea-to-app` (a gated
intake→…→ship pipeline) and `guide` (a "what's my next step?" router). The problem is they feel
*mechanical* — they name the next tool and leave you. The Conductor is the **mentor layer on top**: it
greets you, elicits what you want, and **drives** idea-to-app + guide in plain English, **weaving in**
the right resource at each moment (research-scout, loop-design, a stack suggestion, and — named at
their moment — the recommender, GitMCP, cookbook, agent-architect, agent-eval). It keeps you in
control with a checkpoint at every stage.

Design grounded in cited research (saved in `research.md`): Anthropic's *Building Effective Agents*
(orchestrator + routing; "simple composable patterns beat frameworks"), peer-reviewed conversational-
onboarding work (state capabilities/limits, dynamic questions, keep the user able to redirect), and
2026 stack-selection guidance ("boring, proven tech; match the project type").

**This is step 2 of a multi-version arc** (step 1 = `research-scout`, shipped). v1 = the core guided
spine; later versions deep-wire every resource (v2), add a full stack-decider (v3), and end-to-end
build→bugfix→security auto-chaining (v4). See "Later phases".

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A beginner is greeted and guided from zero (Priority: P1)

A non-technical owner opens a fresh project. A **one-line greeting** offers the Conductor ("New here?
Say **start** and I'll walk you through building something — no commands to memorize"). They say
start. The Conductor greets them, says in plain English what it can and can't do, asks what they want
to build, and — one friendly step at a time — drives the journey, explaining each stage and routing to
the right skill, until they have a plan (and then a build) without ever needing to know a command.

**Why this priority**: This IS the feature — turning "great kitchen, no chef" into a guided
experience. It's the whole reason the owner asked.

**Independent Test**: On a fresh project, confirm the greeting appears once; saying "start" launches a
plain-English guided flow that elicits the goal and walks the owner to a plan, routing to existing
skills, with no command knowledge required.

**Acceptance Scenarios**:

1. **Given** a fresh project, **When** a session starts, **Then** a single one-line offer to run the
   Conductor appears (once per project; never nags again).
2. **Given** the owner says "start" (or `/start`), **When** the Conductor runs, **Then** it greets,
   states capabilities + limits, and asks what they want to build in plain English.
3. **Given** the owner describes a vague idea, **When** the Conductor proceeds, **Then** it routes
   into the existing grilling/discovery flow rather than guessing — and explains why in one line.

### User Story 2 - It weaves in the right resource at the right moment (Priority: P1)

As the journey moves, the Conductor pulls in the right tool at each stage and says, plainly, what it is
and why now: `/discover` (is it worth building?), `grill-me` + `research-scout` (pin the plan with
cited evidence, with consent), `loop-design` (how the build runs), a **light stack suggestion**, then
the build (speckit + Superpowers) → `/verify` → `/security-review` → `git-safety`. Optional extras
(recommender, GitMCP, cookbook, agent-architect, agent-eval) are **named at their moment**.

**Why this priority**: This is the exact "what fits where" gap the owner hit. P1 alongside Story 1.

**Independent Test**: Walk a sample build; confirm at each stage the Conductor names + routes to the
correct skill with a plain-English reason, weaves in research-scout/loop-design/stack-suggestion, and
mentions the optional extras at the right time.

**Acceptance Scenarios**:

1. **Given** any stage, **When** the Conductor advances, **Then** it names the right skill/resource for
   that stage and explains in plain English what it does and why now.
2. **Given** a decision that evidence would sharpen, **When** at the plan stage, **Then** it OFFERS
   `research-scout` (with consent) and folds cited findings in.
3. **Given** the owner asks "what should I build this with?", **When** at the plan stage, **Then** it
   gives a light stack suggestion (sensible default + one-line why), noting the full decider is later.

### User Story 3 - The owner stays in control (Priority: P1)

The Conductor **checkpoints at every stage** — explains, does/routes, then stops for the owner's OK
before the next. The owner can say "just run it" to **bypass** checkpoints and move faster. But it
**never pushes, merges, or deploys** on its own — even in bypass mode — those stay the owner's manual
action.

**Why this priority**: Control + safety for a non-technical learner is non-negotiable; it's also the
"keep me in control" rule. P1.

**Independent Test**: Confirm the Conductor stops at each gate by default; "just run it" makes it skip
checkpoints; and in BOTH modes it stops before any push/merge/deploy and hands that to the owner.

**Acceptance Scenarios**:

1. **Given** default mode, **When** a stage finishes, **Then** the Conductor stops and asks before the
   next stage.
2. **Given** the owner says "just run it", **When** bypass is on, **Then** it proceeds through stages
   without stopping — except it still STOPS before push/merge/deploy.
3. **Given** any mode, **When** it reaches push/merge/deploy, **Then** it never does it automatically.

### Edge Cases

- **Two SessionStart offers** (recommender-nudge + Conductor greeting) → keep each a single line,
  once-per-project, marker-deduped; acceptable minor overlap (owner already accepted this for the
  recommender).
- **Owner pastes a half-built project** → the Conductor routes to `safe-change`/`/health` instead of
  the new-build pipeline (don't force idea-to-app on existing code).
- **Owner tries to skip to building** → it gently explains why a plan comes first (idea-to-app's gate),
  but respects "just run it" bypass for the *checkpoints*, never for the safety wall.
- **A resource isn't available** (e.g. GitMCP/cookbook not connected) → it says so plainly and
  continues, rather than pretending.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: A new skill `start` (the Conductor) MUST exist as a plain-markdown `SKILL.md` at
  `.claude/skills/start/`, runnable by any AI tool (Principle VI).
- **FR-002**: A SessionStart hook MUST offer the Conductor with a **single line, once per project**
  (marker-deduped; never nags), and the owner MUST also be able to invoke it via `/start` anytime.
- **FR-003**: The Conductor MUST greet, state its **capabilities + limits**, and elicit what the owner
  wants to build with **dynamic plain-English questions** — not a static form.
- **FR-004**: The Conductor MUST **drive existing skills**, not reimplement them: it routes through
  `idea-to-app`'s gated pipeline and uses `guide`'s routing logic.
- **FR-005**: At each stage the Conductor MUST name the right skill/resource and explain, in plain
  English, what it is and why now — defining every term (non-technical owner).
- **FR-006**: The Conductor MUST weave in, at their moment: `/discover`, `grill-me`, **`research-scout`**
  (offered with consent), `loop-design`, a **light stack suggestion**, build (speckit + Superpowers),
  `/verify`, `/security-review`, `git-safety`.
- **FR-007**: The Conductor MUST **name** (not necessarily deep-wire, in v1) the optional extras at the
  right moment: the `claude-code-setup` recommender, GitMCP, cookbook, `agent-architect`, `agent-eval`.
- **FR-008**: The Conductor MUST **checkpoint at every stage** (explain → do/route → stop for OK),
  with an **opt-in bypass** ("just run it") that skips checkpoints.
- **FR-009**: The Conductor MUST NEVER push, merge, or deploy automatically — in EITHER mode; those
  stay the owner's manual action (same wall as `autopilot`/`safe-change`).
- **FR-010**: The light stack suggestion MUST use the kit's defaults nudged by project type, with a
  one-line "why", and state that the full stack-decider is a later version.
- **FR-011**: If a routed skill or resource is unavailable, the Conductor MUST say so plainly and
  continue — never pretend (Principle VII).
- **FR-012**: For existing-code projects, the Conductor MUST route to `safe-change`/`/health`, not the
  new-build pipeline.
- **FR-013**: The Conductor MUST be registered in `AGENTS.md`, `SKILL-MAP.md`, and the `README.md`
  index; the SessionStart hook is Claude-only and MUST have a documented manual fallback (Principle VI).

### Key Entities *(include if feature involves data)*

- **Stage**: one step of the journey (discover, plan, build, …) with the skill/resource that serves it.
- **Stage → resource map**: the Conductor's core knowledge — which skill/resource fits which stage.
- **Checkpoint**: the stop-for-OK gate between stages (skippable via bypass; never for push/merge/deploy).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A non-technical owner who knows zero commands can, from the greeting alone, reach an
  approved plan — guided the whole way, never needing to name a skill.
- **SC-002**: At every stage the Conductor states the right next skill/resource + a plain-English why
  (verifiable by walking a sample build) — directly closing the "what fits where" gap.
- **SC-003**: Every technical term the Conductor uses is defined in plain English at first use.
- **SC-004**: The Conductor stops at each checkpoint by default; "just run it" bypasses checkpoints;
  in both modes it never pushes/merges/deploys.
- **SC-005**: The greeting appears once per project and never nags again.
- **SC-006**: It reuses existing skills (no duplicated pipeline) — reachable from SKILL-MAP/AGENTS/README.

## Assumptions

- **Mentor layer, not a new pipeline** — drives `idea-to-app` + `guide` + the stage skills; its own
  new code is the `SKILL.md`, a small SessionStart greeting hook, and references. (Principle V.)
- **Procedure skill** (like `research-scout`/`guide`) — no Python runner; the greeting hook is the only
  script (deterministic, stdlib, mirrors `recommender_nudge.py`).
- Non-technical owner: plain English throughout.
- Ships to both repos (PCK + VCK), same as every kit feature.

## Later phases (recorded — see memory `conductor-roadmap`)

- **v2 — full resource map:** deep-wire the recommender, GitMCP, cookbook, agent-architect, agent-eval
  (not just name them).
- **v3 — stack-decider:** full per-project stack selection + setup, not just a light suggestion.
- **v4 — end-to-end auto-chaining:** build → test → fix bugs → harden security, hand-held throughout.
