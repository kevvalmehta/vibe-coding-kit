# Context Engineering (in plain English)

**When to use this:** any project with AI *inside the product*, during `/speckit-plan` and when
building the AI feature. Pairs with `docs/ai-feature-checklist.md` and the `agent-architect` skill.

**Not needed when:** ordinary software with no LLM in it.

Source: Google's **"The New SDLC With Vibe Coding"** (Addy Osmani, Shubham Saboo, Sokratis
Kartakis, 2026), adapted for this kit.

---

## What "context" means

**Context** = everything you put in front of the AI *before* it answers — its instructions, the
relevant files, examples, the tools it can use. **Context engineering** = deliberately deciding
*exactly* what goes in, every turn. (*Engineering* here = doing it on purpose with care, not
dumping everything in and hoping.)

Why it matters: most AI mistakes are not "the AI is dumb" mistakes — they are **"it was shown the
wrong stuff"** mistakes. Real use: a support agent gives a wrong refund answer. The model is fine;
it was never given the current refund policy. That's a context problem, fixed by feeding it the
right document — not by switching to a bigger AI.

A useful rule of thumb from the whitepaper: **an agent is roughly 10% the model (the raw AI brain)
and 90% the *harness*** — the *harness* (also called the *scaffold*) being everything around the
brain: its instructions, tools, memory, and rules. Get the harness right and an ordinary model
performs well; get it wrong and the best model still fails. ("Most agent failures are
*configuration* failures.")

---

## The 6 types of context to plan for

When you design an AI feature, decide what fills each of these:

1. **Instructions** — what the AI is told to do and how to behave (its system prompt, rules).
2. **Knowledge** — facts it needs (your policies, product data, documentation).
3. **Memory** — what it remembers across turns or sessions (e.g. this user's past orders).
4. **Examples** — sample inputs and the ideal outputs, so it copies the right pattern.
5. **Tools** — the actions it can take (look up an order, send an email) — see checklist Factor 4.
6. **Guardrails** — the hard limits ("never give legal advice", "never spend money without
   approval") — see checklist Factor 7.

---

## Static vs dynamic context (and why it saves money)

You pay for every word the AI reads, every turn. So split context by *how often it's needed*:

| **Static context** (load every turn) | **Dynamic context** (load only when needed) |
|---|---|
| *Static* = unchanging, always on | *Dynamic* = changes per task, on demand |
| System instructions | A skill's full instructions (loaded when that task comes up) |
| Rule files (`AGENTS.md`, `CLAUDE.md`) | Results that come back from a tool call |
| Core guardrails | A document fetched to answer one specific question |
| Costs tokens on *every* interaction | Costs tokens only when actually used |

**Progressive disclosure** is the technique that makes this work. *Disclosure* = revealing;
*progressive* = step by step. The AI gets a tiny summary up front (just enough to know a thing
*exists*), and only pulls in the heavy detail when a task actually needs it. Real use: an agent
"knows" about 30 skills but only reads the full instructions for the one skill the current task
needs — so it carries lots of ability while paying for almost none of it until used. (This kit's
own skills work exactly this way: `SKILL.md` files are read on demand, not all at once.)

---

## Treat context boundaries like code

The whitepaper's last point: decisions about what the AI sees are **first-class design
decisions**, not afterthoughts. So:

- [ ] Write down, in the plan, what fills each of the 6 context types.
- [ ] Mark each piece **static** or **dynamic** — and prefer dynamic + progressive disclosure to
  keep token cost (and confusion) down.
- [ ] **Review context boundaries in the PR.** A *PR* (Pull Request) = the "please review and
  approve my change" step before code goes in. Changing what the AI sees can change its behavior
  as much as changing code — so review it the same way, and version it (keep it in the repo).

---

## How this plugs into our workflow

| Stage | What to do |
|---|---|
| `/speckit-plan` | Fill the 6 context types; mark each static/dynamic; note where progressive disclosure applies. Record it in the plan. |
| `agent-architect` | When it proposes the agent design, have it state the context plan per agent. |
| Build (Superpowers) | Keep prompts/rule files in the repo (checklist Factor 2). Changing them = a reviewable change. |
| PR review | Review changes to what the AI sees, not just code. |
