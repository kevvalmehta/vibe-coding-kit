# AI Feature Checklist (12-Factor Agents, in plain English)

**When to use this:** any time a project's spec includes AI *inside the product* —
a chatbot, an email-drafting feature, an agent that does work for your users,
a plugin/skill that calls an LLM, or a Managed Agent. Pull this out during
`/speckit-specify` and `/speckit-plan`, and let `grill-me` use it as ammunition.

**Not needed when:** the app is ordinary software with no LLM in it. The normal
workflow already covers that.

Source: [12-Factor Agents](https://github.com/humanlayer/12-factor-agents) (CC BY-SA 4.0),
adapted for this kit.

---

## The checklist

Tick each one off in the plan, or write down why it doesn't apply.

### 1. Natural language → structured actions
- [ ] The AI's job is to turn what a user says into a *specific, structured action*
  (like "create_invoice with these fields"), not to free-wheel.
- Plain English: the AI fills in a form; your code does the work.

### 2. Own your prompts
- [ ] Every prompt lives in your repo as a file you can read, edit, and version —
  never buried inside a library or framework.
- Why: when quality drops, the prompt is the first thing you'll tune.
- Cost: cache the big, stable system prompt so you aren't re-billed full price every call —
  see `docs/token-quick-wins.md` (Win 6).

### 3. Own your context window
- [ ] You decide exactly what information the AI sees each turn — and how it's
  formatted — instead of letting a framework dump everything in.
- Why: most AI quality problems are really "it saw the wrong stuff" problems.

### 4. Tools are just structured outputs
- [ ] Treat "the AI used a tool" as "the AI produced JSON, and our tested code acted
  on it." The dangerous part (acting) is deterministic code you can test with TDD.

### 5. One source of truth for state
- [ ] The agent's progress is stored in the same place as your business data
  (for us: Supabase), not in a separate hidden "agent memory."
- Why: one place to look when debugging; nothing gets out of sync.

### 6. Pause and resume
- [ ] A long-running AI task can stop (waiting for approval, hitting an error,
  server restart) and pick up where it left off. Design this in the spec, not after.

### 7. Asking a human is a tool
- [ ] When the AI is unsure or about to do something risky (send an email, spend
  money, delete data), "ask the human" is an explicit step — with a clear approve/
  reject path. Decide in the spec which actions ALWAYS need approval.
- This is our **Security First** rule applied to AI features.

### 8. Own your control flow
- [ ] The overall flow (step A, then B, then maybe C) is written by us as ordinary
  code. The LLM makes decisions *inside* steps; it doesn't invent the pipeline.
- Plain English: deterministic rails, AI on the rails. (Exactly how our
  `idea-to-app` and `safe-change` skills already work.)

### 9. Put errors in front of the AI, compactly
- [ ] When a tool call fails, feed a short, clear error back so the AI can self-correct —
  but cap retries (e.g. 3 strikes) and then escalate to a human. Never silent infinite loops.

### 10. Small, focused agents
- [ ] Each agent does ONE job well (3–10 steps), with its own small prompt and toolset.
  Need more? Build several small agents, not one giant one.
- Mirrors our **Simple + Surgical** rule.

### 11. Trigger from anywhere
- [ ] Users can kick off the agent from where they already are (Slack, email, a button
  in the app) and get results back there too. Decide entry points in the spec.

### 12. Stateless reducer (the engine-room version of #5 and #6)
- [ ] The agent itself holds no hidden memory: give it the same history, get the same
  next step. All state lives in the database.
- Why: makes the agent testable — which means TDD works on it.

### Bonus (Factor 13): Pre-fetch context
- [ ] If you already KNOW the agent will need certain data, fetch it up front and hand
  it over — don't make the AI ask for it tool-call by tool-call. Cheaper and faster.

---

## Verification & operations (from Google's *New SDLC* whitepaper)

The 12 factors above get the AI feature *built right*. These two prove it *works and keeps
working* — and they come from a newer, separate source: Google's **"The New SDLC With Vibe
Coding"** (Addy Osmani, Shubham Saboo, Sokratis Kartakis, 2026). That paper's headline claim:
the thing that separates real engineering from guesswork is **how you verify the output** —
and for AI, ordinary tests are not enough.

### 14. Verify AI output with EVALS, not just tests
- [ ] You have **evals** for the AI parts, not only tests for the code parts.
- Plain English: a *test* checks something with one correct answer ("2 + 2 must return 4" —
  pass/fail). An **eval** (short for *evaluation*) checks fuzzy AI output that has *no single
  right answer* ("is this AI-written reply polite and on-brand?") by **scoring it against a
  *rubric*** — a written scoring guide (e.g. rate politeness 1–5, must score ≥4).
- [ ] Cover BOTH kinds of eval:
  - **Output eval** — was the final answer good?
  - **Trajectory eval** — *trajectory* = the path the AI took to get there. Did it use the right
    tools in the right order for sound reasons, or stumble into a lucky right answer? Check the
    journey, not just the destination.
- [ ] **Set the bar at the eval, not the demo.** A *demo* shows the AI working once (could be
  luck). An *eval suite* (a whole collection of these scored checks, run automatically) shows it
  works reliably. Decide the passing bar in the spec, before building.
- Build help: run **`/agent-eval`** — it scaffolds an eval set (example cases + rubric + passing
  bar), runs it for a plain-English pass/fail report, and wires it into CI as an automatic gate.
  Grounded on the Claude Cookbooks recipe `misc/building_evals.ipynb` (via the pinned `cookbook`
  GitMCP source).

### 15. Watch it after launch (AgentOps)
- [ ] You can SEE what the live AI is doing, and you'd KNOW if it quietly got worse.
- Plain English: **AgentOps** = looking after an AI agent once it's live (named after "DevOps",
  the practice of running live software). Build these in *before* launch, not after:
  - **Observability** — your ability to see inside a running system. In practice: **logs** (a
    record of what happened), **traces** (a *trace* = a step-by-step replay of one single run —
    every decision and tool call — so when something breaks you can see exactly where), and
    **metrics** (numbers over time, e.g. average response quality).
  - **Drift monitoring** — *drift* = slow, silent decline. An AI feature can get worse over time
    (inputs change, the world changes) with no error message. Watch a quality number so you catch
    the slide before customers do.
  - **LLM-as-judge** — use a cheap, fast AI to automatically *grade* a sample of your main AI's
    live output against the same rubric from #14, so a human isn't checking every single reply.
  - [ ] Decide WHO reviews the flagged cases (the human-in-the-loop), and how often.

---

## How this plugs into our workflow

| Stage | What to do with this checklist |
|---|---|
| `/speckit-specify` | Note which features involve an LLM; mark human-approval points (#7) and entry points (#11); set the eval passing bar (#14) — "done" means hitting it, not a working demo. |
| `/speckit-plan` | Walk all 13 boxes; record decisions (especially #2, #3, #5, #8) in the plan. Then decide evals (#14) and after-launch watching (#15), and do context engineering — what the AI sees each turn — using `docs/context-engineering.md`. |
| `grill-me` | Ask it to grill the plan against this file. |
| Build (Superpowers) | #4 and #12 are what make TDD possible on AI features — tests target the deterministic code around the LLM. |
| Plan + Build | Before writing code against the Claude SDK or any library, ground against its REAL current docs via **GitMCP** (`https://gitmcp.io/{owner}/{repo}`) so APIs aren't hallucinated — see `AGENTS.md` → "Grounding against real library docs". |
| Plan + Build (AI inside) | Pull a real Claude recipe from the **`cookbook`** GitMCP source (pinned in `.mcp.json` → `gitmcp.io/anthropics/claude-cookbooks`) instead of guessing the SDK. For "Managed Agents or plain Messages API?" read the tool-use recipes; for "how do I TDD an on-brand / quality check?" read `misc/building_evals.ipynb` (grade output against examples) so Superpowers builds the feature test-first. |

---

## Claude Managed Agents — what they are and when we'd use them

**Plain English:** Anthropic now offers "Managed Agents" — instead of building and
hosting your own agent loop (the program that lets Claude read files, run code,
browse, and use tools), Anthropic runs that machinery for you in a secure cloud
sandbox. You define an *agent* (model + instructions + tools + skills) once, then
start *sessions* that run tasks — even long ones lasting hours — and stream results
back to your app. Docs: https://platform.claude.com/docs/en/managed-agents/overview

**Why it fits this kit well:**
- It IS the 12-factor philosophy with the hard parts handled: the harness covers
  pause/resume (#6), context management (#3, partially), and execution. You still own
  the prompt (#2), the tools (#4), control flow (#8), and approval points (#7) via
  its permission policies.
- It supports **Skills** and **MCP servers** — the same building blocks we already
  use — so a skill prototyped here can graduate into a production Managed Agent.
- For a non-developer it removes the scariest layer (servers, sandboxes, agent loops).

**When to choose it:** building an agent *product or internal automation* that runs
on its own — long tasks, async work, triggered from your app. The agent definition
still goes through our normal pipeline: spec → plan → tasks → build → test.

**When NOT to:** a simple AI feature inside a web app (one prompt in, one answer out)
just calls the regular Messages API — no agent harness needed.

**Caveats (as of June 2026):** it's in beta; sessions and data are stored on
Anthropic's side (deletable, but not for strict data-residency needs unless you
self-host the sandbox); pricing follows API token usage.
