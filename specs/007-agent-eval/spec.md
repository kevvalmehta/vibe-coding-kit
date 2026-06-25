# Feature Specification: `/agent-eval` — make evals runnable, not just documented

**Feature Branch**: `007-agent-eval`

**Created**: 2026-06-24

**Status**: Draft

**Input**: User description: "A new kit skill /agent-eval that scaffolds and runs evaluations for AI-inside features, so checklist #14 (evals) and constitution Principle VIII become doable instead of manual."

## Context (plain English)

The kit just made **evals** a hard rule. An **eval** (short for *evaluation*) is a scored check on
AI output that has no single right answer — e.g. "is this AI-written reply on-brand and correct?" —
graded against a **rubric** (a written scoring guide, like "rate 1–5, must score ≥4"). Tests check
fixed right/wrong answers; evals check fuzzy AI answers.

Right now the kit only *describes* evals (in `docs/ai-feature-checklist.md` #14/#15 and constitution
Principle VIII). There is no tool to actually create or run one — an owner would have to hand-build
it from a Claude Cookbooks recipe. For a non-technical owner that's a wall. `/agent-eval` removes the
wall: it sets up a starter eval for an AI feature and lets it be run and checked automatically.

This skill pairs with `agent-architect` (which designs the AI agents) and the AI feature checklist
(which says you need evals). It is to evals what the kit's other skills are to their jobs: a guided,
plain-English, portable procedure.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Set up a starter eval for an AI feature (Priority: P1)

A non-technical owner has an app feature that uses AI (e.g. a support-reply generator). They run
`/agent-eval`. The skill asks, in plain English, what the AI feature does and what "good output"
looks like, then creates a ready-to-fill **eval set**: a place to put example inputs, the rubric to
grade against, and the passing bar — plus the machinery to score outputs automatically. The owner is
left with a working starting point they can extend, not a blank page.

**Why this priority**: Without the starter set, evals stay theoretical. This is the core value — it
turns "you should have evals" into "you have evals." It is the minimum that delivers the whole point
of the feature.

**Independent Test**: Run `/agent-eval` against a sample AI feature; confirm it produces an eval set
(example cases + rubric + passing bar + a way to score) and an explanation of how to add more cases
and run it — with no further skills needed.

**Acceptance Scenarios**:

1. **Given** a project with an AI feature, **When** the owner runs `/agent-eval`, **Then** a new
   eval set is created for that feature with at least one example case, a rubric, and a stated
   passing bar, and the skill explains in plain English what each part is.
2. **Given** the owner has no idea what to grade, **When** the skill asks what "good" means, **Then**
   it proposes a sensible default rubric they can accept or edit, never leaving them stuck.
3. **Given** an app with no AI feature in it, **When** the owner runs `/agent-eval`, **Then** the
   skill declines and explains that evals are only for AI-inside features (mirrors `agent-architect`).

### User Story 2 - Run the eval and get a clear pass/fail against the bar (Priority: P1)

The owner (or the AI building the feature) runs the eval set. Each example input is sent to the AI
feature, the output is scored against the rubric (using a cheap AI as the **judge** — *LLM-as-judge*:
a second, inexpensive AI grades the main AI's output), and the result is a plain-English report:
which cases passed, which failed and why, and whether the whole set cleared the passing bar.

**Why this priority**: A scaffold you can't run proves nothing. "Set the bar at the eval, not the
demo" only means something if the bar can actually be measured. P1 alongside Story 1.

**Independent Test**: Run the created eval set against a feature whose output is deliberately good,
then again deliberately bad; confirm the report passes in the first case and fails (with reasons) in
the second, and that the overall pass/fail correctly reflects the passing bar.

**Acceptance Scenarios**:

1. **Given** an eval set and an AI feature, **When** the eval is run, **Then** each case gets a score
   against the rubric and the report states overall pass/fail versus the bar in plain English.
2. **Given** a case fails, **When** the report is produced, **Then** it says *why* it failed (the
   rubric points it missed), not just that it failed.
3. **Given** the judge model is unavailable or a call errors, **When** the eval runs, **Then** it
   reports the problem plainly and does not silently report a false pass (fail loud).

### User Story 3 - Make the eval an automatic gate on every change (Priority: P2)

The owner wants the eval to run by itself whenever the project changes, so an edit that quietly makes
the AI worse is caught before it ships — the same way tests already run automatically. `/agent-eval`
wires the eval set into the project's existing automatic checks, so a drop below the passing bar
blocks the change.

**Why this priority**: This is what stops silent decline (the "drift" problem from checklist #15). It
is high value but depends on Stories 1–2 existing first, so P2.

**Independent Test**: With an eval set wired in, make a change that worsens the AI output below the
bar; confirm the automatic check fails and explains why. Make a change that keeps quality above the
bar; confirm the check passes.

**Acceptance Scenarios**:

1. **Given** a wired-in eval set, **When** a change drops AI quality below the bar, **Then** the
   automatic check fails and names the cause in plain English.
2. **Given** running the full eval automatically would be slow or costly on every change, **When** it
   is wired in, **Then** the skill states clearly how often/when it runs and flags any cost so the
   owner is not surprised (no hidden token spend).

### Edge Cases

- **No AI in the app** → the skill declines politely (evals are only for AI-inside features).
- **No example cases yet** → the skill still creates the structure and a starter case, and tells the
  owner the eval is only as good as the cases they add (no false confidence from an empty set).
- **Cost/runtime of judging** → the skill surfaces that each eval run costs tokens and may be slow,
  and offers a cheaper/faster option (e.g. run a small sample frequently, the full set less often).
- **Trajectory evals** (did the AI use the right steps/tools, not just give a good final answer) →
  acknowledged with a placeholder the owner can grow into; full support is a later phase, stated
  honestly, not silently dropped.
- **Non-determinism** → because AI output varies run to run, the report should not treat a single
  lucky pass as proof; the skill explains running more cases gives a more trustworthy result.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The skill MUST create a starter **eval set** for a named AI feature: example input
  cases, a rubric to grade against, and an explicit passing bar.
- **FR-002**: The skill MUST, in plain English, explain every part it creates and define each
  technical term inline (eval, rubric, passing bar, LLM-as-judge, trajectory) for a non-technical
  owner.
- **FR-003**: The skill MUST support **output evals** (grade the final answer) in v1, and MUST at
  least acknowledge **trajectory evals** (grade the steps/tools used) with a clearly-marked
  placeholder for a later phase — never silently omitting them.
- **FR-004**: The skill MUST support **LLM-as-judge** scoring (a cheap model grades output against
  the rubric) because eval outputs are usually non-deterministic.
- **FR-005**: The skill MUST produce a plain-English result report stating per-case scores, reasons
  for any failures, and overall pass/fail versus the passing bar.
- **FR-006**: The skill MUST fail loud — if the judge or a model call errors, it reports the problem
  and never reports a false pass (constitution Principle VII, Rule 12).
- **FR-007**: The skill MUST surface the cost and runtime of running evals (token spend, time) as an
  up-front estimate, offer a cheaper sampling option, and support a **hard cost cap** the owner sets
  so a run can never quietly exceed it — no hidden spend.
- **FR-008**: The skill MUST decline for apps with no LLM inside, explaining why (consistent with
  `agent-architect`). When it is **unsure** whether a feature uses AI, it MUST ASK the owner in plain
  English and decline only on a clear "no" (grill 2026-06-25) — never guess silently.
- **FR-009**: The skill MUST be a plain-markdown `SKILL.md` under `.claude/skills/agent-eval/` that
  any AI tool can read and follow (LLM portability, constitution Principle VI).
- **FR-010**: The skill MUST be registered in `AGENTS.md` and `SKILL-MAP.md`, and referenced from
  `docs/ai-feature-checklist.md` #14, so it is discoverable and not orphaned (Principle VI).
- **FR-011**: Any system prompt the skill generates MUST use prompt caching (cost rule from
  `docs/token-quick-wins.md`).
- **FR-012**: The passing bar MUST be recorded with the eval set (decided in the spec/plan of the
  feature being evaluated), embodying "set the bar at the eval, not the demo."
- **FR-016** *(grill 2026-06-25)*: The passing bar MUST be a **percentage of cases** clearing a
  per-case score (default target ~80%), AND the eval set MUST support a **"critical cases" tier**
  that must never fail — if any critical case fails, the whole set fails regardless of the
  percentage. The skill MUST set the percentage with **headroom** (e.g. aim ~85%) so normal AI
  variation stays above the bar.
- **FR-017** *(grill 2026-06-25)*: To stay reliable despite non-determinism, the skill MUST grade
  with the judge at its most consistent setting (**temperature 0**) and MUST **re-run once** when a
  result lands borderline (within a small margin of the bar) before reporting a fail — so a single
  unlucky run never blocks a change.
- **FR-018** *(grill 2026-06-25)*: The automatic gate MUST, on every change, run a **representative
  sample + all critical cases** (cheap/fast), while the **full set** runs on demand and before merge
  to `master`. The skill MUST always offer a full run, and MUST proactively recommend a full run when
  a change warrants it (e.g. the AI's prompt/instructions changed).
- **FR-019** *(grill 2026-06-25)*: Starter cases — the skill MUST auto-generate a few **clearly
  labelled "starter" example cases** from the feature description + rubric (never a blank set), warn
  they are training wheels, and offer to turn the owner's pasted **real** examples into real cases.
- **FR-020** *(grill 2026-06-25)*: Eval cases MUST be stored as **plain, human-readable files the
  non-technical owner can read and edit directly** (no coding required to add/change a case), kept in
  an obvious `evals/` location — while the owner can also ask an AI tool to write cases for them.
- **FR-013** *(resolved: v1 = Standard)*: The skill MUST both SCAFFOLD the eval set AND run it,
  producing a real plain-English pass/fail report (per User Story 2). Scaffold-only is not enough.
- **FR-014** *(resolved: v1 = Standard)*: The skill MUST wire the eval set into the project's
  automatic checks (CI) so a drop below the passing bar blocks a change (per User Story 3). The
  skill MUST state how often the gate runs and flag token cost (FR-007), and SHOULD offer a sampled
  (cheaper/faster) run for the automatic gate while the full set runs on demand.
- **FR-015** *(resolved: deferred to a later phase)*: After-launch watching (#15 — logging real
  interactions, sampling live output, judging it, tracking a quality metric, drift alerts, and
  feeding real failures back into the eval set) is explicitly OUT of v1 scope and a documented later
  phase. v1 stays focused on build-time evals + the CI gate. The skill MUST name this later phase in
  its output so the boundary is honest, not silently dropped. See "Later phases" below.

### Key Entities *(include if feature involves data)*

- **Eval set**: the collection for one AI feature — its example cases, rubric, and passing bar.
- **Eval case**: one example — an input to the AI feature plus what "good" looks like for it.
- **Rubric**: the scoring guide the judge applies to an output.
- **Passing bar**: the threshold the whole set must clear to count as "passing."
- **Eval report**: the plain-English result — per-case scores, failure reasons, overall pass/fail.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A non-technical owner can go from "my feature uses AI" to "I have a runnable eval set
  with at least one case, a rubric, and a passing bar" in a single `/agent-eval` session, without
  hand-writing eval code.
- **SC-002**: For a feature with deliberately good output the eval reports pass; for deliberately bad
  output it reports fail with the reason — i.e. the eval actually discriminates quality, it is not a
  rubber stamp.
- **SC-003**: Every technical term in the skill's output is defined in plain English at first use (no
  unexplained jargon), verifiable by reading any run's output.
- **SC-004**: The skill is reachable from `SKILL-MAP.md`, `AGENTS.md`, and the AI feature checklist —
  a cold owner or any AI tool can find it without prior knowledge.
- **SC-005**: Running an eval never reports a false pass on error; an induced model/judge failure
  produces a clear failure message, not a green result.

## Assumptions

- **Scaffolds files (writes), not recommendation-only.** Unlike `agent-architect` (which only
  proposes), `/agent-eval` creates real eval files in the project, because an empty recommendation
  wouldn't remove the wall for a non-technical owner. Its writes are confined to an `evals/`-style
  area plus the registration edits in FR-010.
- **Python default stack** for any runner it generates (kit default), with the Anthropic SDK for the
  judge — but the spec stays outcome-focused; exact format/location is a `/speckit-plan` decision.
- **Cheap model for the judge by default** (cost rule) — e.g. the Haiku tier — overridable.
- **v1 = "Standard" scope** (owner decision 2026-06-24): create eval files + run them + report +
  wire an automatic CI gate. Build-time evals only. Deeper trajectory evals and live after-launch
  monitoring are explicitly later phases (see "Later phases").
- **Eval-case quality is the owner's job**; the skill provides structure and a starter case but
  cannot invent representative real-world inputs — it says so plainly to avoid false confidence.
- Pairs with, and does not duplicate, `agent-architect`, the AI feature checklist, and
  `docs/context-engineering.md`.

## Later phases (out of v1 scope, recorded so they aren't lost)

- **Phase 2 — After-launch watching (#15), for when a real app is deployed.** Once a feature is live
  and serving real users, add a second eval layer over real traffic: (1) log each real interaction
  (input + output) to the project's database; (2) sample a slice (e.g. 50/day) to control cost;
  (3) judge the sample with the same rubric + LLM-as-judge; (4) roll scores into a quality metric
  over time; (5) alert on drift (sustained decline below a threshold); (6) human-in-the-loop review
  of the lowest-scoring real cases; (7) feed real failures back into the build-time eval set so the
  CI gate keeps getting smarter. Mechanism on the kit's stack: store interactions in Supabase, run
  the sampled judging on a schedule (cron / scheduled job), alert by email/Slack. This phase only
  becomes buildable/testable once there is a deployed app with real traffic.
- **Phase 3 — Fuller trajectory evals.** Grade not just the final answer but the path the AI took
  (which tools, in what order, for sound reasons). v1 leaves a marked placeholder; this phase fills
  it in.
