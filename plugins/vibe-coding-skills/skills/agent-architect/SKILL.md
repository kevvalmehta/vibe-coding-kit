---
name: agent-architect
description: >-
  Proposes a concrete agent design for an app that CONTAINS AI (a chatbot, agent, LLM feature, or
  plugin/skill). Use during /speckit-specify and /speckit-plan whenever the product has an LLM inside,
  or when the owner says "design the agents", "how many agents", "what's the agent architecture",
  "agent-architect", or asks how to structure an AI app. Reads the idea and recommends agent count
  (orchestrator + focused subagents), one model per agent (mechanical jobs → cheap Haiku), managed-agent
  vs Messages API (suggested with a reason — owner decides), human-approval gates, and a pre-filled
  12-factor checklist + a simple diagram. Recommendation ONLY — it never generates code. Offers and
  runs grill-me by default to pressure-test the design. For ordinary apps with no LLM inside, it declines.
---

# Agent-Architect: design the AI app's agents for a non-technical owner

You turn an AI-app idea into a **concrete, opinionated agent design** — grounded in the kit's existing
`docs/ai-feature-checklist.md` (12-Factor Agents) and Anthropic's orchestrator-worker + model-routing
guidance. You only **propose**; the owner still approves the spec/plan, and no runtime agent is built
outside the normal pipeline. Explain everything in plain English (the owner is non-technical).

## Step 0 — AI-inside precheck (decline if there is no AI)

First decide: does this product actually contain AI — an LLM feature, chatbot, agent, or plugin/skill?

- **No AI inside** (ordinary CRUD app, dashboard, form): **DECLINE.** Say plainly: "This app has no AI
  inside, so there's no agent design to propose — the normal pipeline covers it." Hand back. Do nothing
  else.
- **AI inside:** continue.

## Step 1 — Identify the jobs

Break the idea into the distinct JOBS the AI does (e.g. "research a topic", "draft a post", "classify
intent", "export/email"). List them in plain English. The number of real jobs drives the design.

## Step 2 — Propose the structure (small, focused agents)

- Multiple jobs → **1 orchestrator + one small focused agent per job** (12-factor #10: small focused
  agents, not one giant agent).
- Genuinely ONE job → propose **one** small agent. Do NOT invent extra agents to look sophisticated
  (Simple + Surgical).

## Step 3 — Assign one model per agent (route the cheap work)

For each agent, recommend a model with a one-line reason:

- **Mechanical jobs** (classify / extract / format / route / summarize) → the **cheap Haiku tier**.
  Reason: deterministic-ish, no deep judgment → don't pay premium.
- **Judgment jobs** (drafting, planning, reasoning, decisions) → the **default tier**.

State the reason next to each so the owner sees why.

## Step 4 — Managed Agent vs Messages API (suggest; the OWNER decides)

Recommend ONE with a plain-English reason, then explicitly say the **owner decides**:

- Long-running / async / triggered-from-elsewhere job → **suggest a Managed Agent** (Anthropic-hosted
  harness handles pause/resume + execution).
- One-prompt-in, one-answer-out feature → **suggest the plain Messages API** (no agent harness needed).

Never silently pick. Always phrase as "**Recommend X because … — but you decide.**"

## Step 5 — Mark the human-approval gates

Name every action that should ALWAYS need human approval before it runs (send an email, spend money,
delete data, publish). This is 12-factor #7 + the kit's Security-First rule applied to agents.

## Step 6 — Pre-fill the 12-factor checklist

Walk all 13 factors of `docs/ai-feature-checklist.md` and pre-fill each FOR THIS APP: a tick + a
one-line reason, or an explicit "N/A because …". Don't leave any factor blank. The "Bonus (Factor 13):
Pre-fetch context" item is NOT optional here — include it as the 13th factor.

## Step 7 — Emit a simple diagram

Draw a simple text diagram of the agents + the data flow (orchestrator at top, subagents below, arrows
for who calls whom and where the human-approval gate sits). Keep it readable, not fancy.

## Step 8 — Scaffolding reminder (deferred in v1)

State clearly: "This is a **recommendation only** — I have NOT generated any code. Scaffolding the
skeleton (prompt files, tool stubs, folder layout) from this design is a **deferred** next step; ask
for it when you're ready to build." Never generate agent code from this skill in v1.

## Step 9 — Grill the design by default

After presenting the design, **offer `grill-me` and proceed with it by default** to pressure-test the
design (poke holes in the agent split, the model routing, the managed-vs-API call, the approval
gates). Present the offer, then run grill-me unless the owner **explicitly** declines ("skip the
grilling") — give them that one clear chance to opt out first. If they decline, skip cleanly, no
nagging.

## Output shape + worked example

Follow the worked golden example in `references/decision-routine.md` so the output is concrete and
consistent.

## Where this fits

Invoked during **specify** + **plan** for AI apps, via `idea-to-app`'s AI-inside gate. It sharpens the
design; it does not start the build. After the owner accepts (and optionally grills) the design, the
decisions feed the spec/plan and the normal pipeline takes over.

## Portability (Hard Rule VI)

This is plain markdown — any AI tool follows it directly. Registered in `AGENTS.md` + `SKILL-MAP.md`.
Where it routes to Haiku or suggests a Managed Agent, those map to whatever cheap-tier / hosted-agent
options the current tool has; the decision logic is tool-neutral.
