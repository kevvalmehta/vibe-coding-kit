# Workflow Evolution Map — Autopilot vs Agent-Architect

_Date: 2026-06-10. Status: exploration map for a build decision (not yet a spec)._

## Why this doc exists

The owner wants to evolve this dev kit in two directions that surfaced in one
conversation. They are **related but separate builds**. This doc maps both at the
level needed to choose which to build first. After the choice, the chosen one gets
its own full spec → plan → tasks → build cycle.

The trigger question was: "use agents/subagents to smooth my workflow, save tokens,
and also help me design agents for the AI apps I build."

It split cleanly into two evolutions:

| | Smooths what | One-line |
|---|---|---|
| **A — Autopilot** | The owner's *dev workflow* | Drives the spec-kit steps, runs heavy work in subagents, saves tokens |
| **B — Agent-Architect** | The *AI apps* the owner builds | Reads an AI-app idea and proposes its agent/subagent/managed-agent design |

Neither requires a new external install (no ruflo, no framework). Both use tools
Claude Code already ships: the `Agent` tool (subagents), the `Workflow` tool
(deterministic fan-out), hooks, and model routing (Haiku/Sonnet/Opus).

---

## Shared foundation — quick wins to adopt regardless of choice

These need **no build**. They are habits/config that cut token cost on everything,
and both evolutions lean on them:

1. **Model routing** — send cheap, mechanical work (classify, extract, lint, format,
   summarize) to **Haiku** (~15× cheaper than Opus); keep planning/architecture on
   Opus/Sonnet. Documented industry result: ~51% cost cut vs all-Opus.
2. **`/compact` proactively** — compress the chat before it bloats, not after.
3. **`/recap` on resume** — summary of where you left off without replaying the session.
4. **Scope-bound prompts** — "fix the login function in auth.ts," not "refactor auth."
5. **Caveman mode** — already on; ~75% chat compression.
6. **Prompt caching** — Claude Code already caches stable system prompts automatically.

The build-time lever both evolutions share:

7. **Subagents with structured handoffs** — heavy reading/analysis runs in a *separate*
   context window; only a tight result returns to the main chat. Keeps the main context
   lean (saves tokens, lasts longer) and is more reliable. Anthropic's own data: an
   Opus lead with Sonnet subagents beat a solo Opus by ~90% on their research eval.

---

## Evolution A — Autopilot (the workflow orchestrator)

### The friction it removes
Today the owner hand-drives the chain: run `/speckit-specify`, read it, run
`/speckit-clarify`, read it, run `/speckit-plan`… then manually run `/verify` and
`/security-review` before a PR, waiting on each. Lots of manual "next, next, next."

### What it is
A single orchestrator skill (working name `autopilot`) that:
- **Chains** the spec-kit steps for the owner, stopping only at chosen approval gates.
- **Spawns subagents** for the heavy links so the main chat stays light:
  - *Plan step* → fan out 2–3 subagents drafting competing architectures + 1 judge
    that scores them → owner gets the winner plus the best ideas from the runners-up
    (this is the "parallel planning" the owner asked for).
  - *Pre-PR step* → run `/verify` and `/security-review` as parallel subagents → one
    combined report instead of two manual waits.
- **Routes by model** — mechanical sub-steps to Haiku, judgment to Opus/Sonnet.
- **Auto-updates `HANDOFF.md`** after each step so any tool (Codex, Cursor) resumes cold.

### Approval gates (to be finalized at spec time)
Three candidate modes — full stop-every-step / stop-at-the-big-3 (after plan, before
build, before PR) / roll-through-unless-failure. Leaning to **stop-at-the-big-3** for a
non-technical owner: smooth but never silently ships.

### What gets built
- One orchestrator skill (`.claude/skills/autopilot/`).
- A subagent definition or two for the parallel-planning and the checks fan-out
  (or use the existing `cavecrew` agents + the `Workflow` tool).
- A small HANDOFF.md auto-writer step.
- Registration in `AGENTS.md` + `SKILL-MAP.md` (Hard Rule #6, LLM portability).

### Effect
- Less manual driving (the core ask).
- Better plans (panel beats single-shot).
- Lower token cost (subagent isolation + Haiku routing).
- Tighter cross-tool handoff (auto HANDOFF.md).

### Risk / effort
- **Effort: Medium.** It orchestrates existing skills; it does not reinvent them.
- **Risk: Low–Medium.** Main risk is the orchestrator making a bad decomposition and
  subagents faithfully doing the wrong thing — mitigated by keeping the owner at the
  big-3 gates and by a tested orchestrator prompt.
- Reversible: it's a skill; deleting the folder removes it.

### Open questions for the spec — RESOLVED 2026-06-10
- **Gate mode: stop at EVERY step (max control).** Owner wants full control until the
  autopilot is tested and trusted. A `--gates big3` / `--gates auto` relaxation is a
  later enhancement, NOT in v1. Default = stop at every step, wait for explicit "go".
- **Build: a visible orchestrator skill for the chain + gates, using the `Workflow`
  tool only inside the heavy steps** (parallel architecture drafting + parallel
  verify/security). Owner sees every gate; parallelism stays under the hood. No new install.
- **Scope: drives specify → clarify → plan → tasks → pre-PR checks.** Heavy subagent
  fan-out at **plan** (3 architectures + 1 judge) and **pre-PR** (verify + security in
  parallel). Build, push, and merge stay manual (owner-controlled).

---

## Evolution B — Agent-Architect (designs the AI apps you build)

### The friction it removes
When the owner wants to build an AI app ("a thing that researches a topic, drafts a
post, and emails it"), nothing today *proposes the agent structure*. The
`docs/ai-feature-checklist.md` holds the right *decisions* but is passive — you read it.

### What it is
A skill (working name `agent-architect`) that runs during `/speckit-specify` →
`/speckit-plan` for any **AI-containing** app. It reads the idea and **proposes a
concrete agent design**, e.g.:

> "Your app has three jobs: research, draft, export. **Recommended:** 1 orchestrator +
> 3 small focused subagents (one per job). Route the 'classify topic' step to **Haiku**
> (cheap, mechanical). The export job is long/async → make it a **Managed Agent**.
> Here is the diagram, and the 12-factor checklist boxes pre-ticked with reasons."

It turns the passive checklist into an active recommendation, grounded in:
- The 12-factor checklist already in the repo (small focused agents, own your prompts,
  human-approval points, deterministic control flow).
- The orchestrator-worker pattern and model routing from current Anthropic guidance.
- The existing Managed-Agents decision section (when to use hosted vs Messages API).

### What gets built
- One skill (`.claude/skills/agent-architect/`) that emits a recommended architecture
  (text + a simple diagram) and the pre-filled checklist.
- A short decision routine: how many agents, which model per agent, managed vs API,
  where the human-approval gates go.
- Wiring into `idea-to-app` GATE for AI apps (it already has an "AI-inside check").
- Registration in `AGENTS.md` + `SKILL-MAP.md`.

### Effect
- The kit now *designs* agent systems, not just ordinary apps — the owner's stated goal.
- Better, cheaper AI apps by default (routing + small-agents baked into the proposal).
- A prototyped skill can graduate into a production Managed Agent (same building blocks).

### Risk / effort
- **Effort: Medium.** Most of the knowledge already exists in the checklist; the work
  is turning it into an active, opinionated recommender and wiring it into the gates.
- **Risk: Low.** It only *proposes* a design; the owner still approves spec/plan. No
  runtime agent is built without going through the normal pipeline.
- Reversible: it's a skill.

### Open questions for the spec — RESOLVED 2026-06-10
- **Output scope:** **Recommendation only** (diagram + rationale + pre-ticked 12-factor
  checklist). NO scaffolding in v1. Owner note: *remind to add scaffolding when the skill is
  first used on a real AI app* (deferred enhancement, tracked in memory).
- **Managed Agents vs Messages API:** **Suggest with a plain-English reason; owner decides.**
  Never silently pick.
- **grill-me:** **Grill by default.** After proposing the design, strongly offer + run `grill-me`
  to pressure-test it every time; skip ONLY if the owner explicitly declines.

---

## Decision matrix

| Factor | A — Autopilot | B — Agent-Architect |
|---|---|---|
| Pays off on… | every project (incl. building B) | only AI-app projects |
| Token savings to owner's own usage | direct (subagents + routing) | indirect |
| Net-new capability for the kit | smoother/cheaper building | **designing agent systems** (a new power) |
| Builds on existing assets | skills + Workflow tool + cavecrew | `ai-feature-checklist.md` (half-done already) |
| Effort | Medium | Medium |
| Risk | Low–Medium | Low |
| Reversible | yes (delete skill) | yes (delete skill) |

## Recommendation

**Build A (Autopilot) first.** It compounds — it makes *every* later build (including B)
faster and cheaper, and model-routing alone roughly halves token cost. Then build B,
using the now-smoother workflow to build it.

Counter-case for **B first:** if the owner has a concrete AI app to design *right now*,
B delivers visible value immediately and A can follow.

Either way: adopt the **shared quick wins** today — they cost nothing and help both.

## Decision (2026-06-10)

**Owner chose A — Autopilot first.** B (Agent-Architect) is deferred but fully
documented below so it can be started cold in a new chat.

**UPDATE 2026-06-10: B (Agent-Architect) is now BUILT** — skill at
`.claude/skills/agent-architect/`, on branch `003-agent-architect`
(`specs/003-agent-architect/`). Shipped recommendation-only (open questions resolved
above); scaffolding deferred (tracked in memory). Wired into `idea-to-app` GATE 5 +
registered in `AGENTS.md`/`SKILL-MAP.md`; guard test green; behavior-verified PASS.

## Next step after the owner picks

The chosen evolution goes through the normal kit flow:
`brainstorm (resolve the open questions above) → /speckit-specify → /speckit-clarify →
/speckit-plan → /speckit-tasks → build with Superpowers`. This doc becomes the seed
for that spec.

---

## How to start B (Agent-Architect) cold in a new chat

B is NOT started yet. To begin it later (in this tool or any other AI tool):

1. Open the project. Read `CLAUDE.md` + `HANDOFF.md` (and for non-Claude tools, the
   switching prompt in `README.md`).
2. Read **this file** — the "Evolution B — Agent-Architect" section above is the seed.
3. Say: *"Start Evolution B (Agent-Architect) from the workflow evolution map."*
4. Resolve B's three open questions (recommendation-only vs scaffold; how opinionated
   on Managed-Agents vs Messages API; whether `grill-me` pressure-tests the design).
5. Then run the normal kit flow: `/speckit-specify` → `/speckit-clarify` →
   `/speckit-plan` → `/speckit-tasks` → build with Superpowers.
6. B must be registered in `AGENTS.md` + `SKILL-MAP.md` when done (Hard Rule #6).

Everything needed to design B is already in the "Evolution B" section and the shared
foundation section of this doc — no need to re-research.
