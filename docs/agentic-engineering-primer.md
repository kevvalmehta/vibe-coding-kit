# Agentic Engineering — a plain-English primer

A short tour of the big ideas in Google's **"The New SDLC With Vibe Coding"** (Addy Osmani,
Shubham Saboo, Sokratis Kartakis, 2026) that aren't already a skill or a checklist item, with what
this kit does about each. Read it once to get the mental model; you don't run it.

> **Source paper:** "The New SDLC With Vibe Coding" — https://www.kaggle.com/whitepaper-the-new-SDLC-with-vibe-coding
> This whole batch of work (evals #14, watch-after-launch #15, context engineering, Principle VIII, and
> the `/agent-eval` skill) came from a gap analysis against that paper.

(**SDLC** = *Software Development Life Cycle* — the full journey of software from idea → live → kept
running. **Agentic** = done by an *agent*, an AI that takes actions on its own, not just answers.)

---

## 1. The verification spectrum — pick your rigor for the stakes

The paper puts how-you-build on a sliding scale (*rigor* = how strict and thorough you are):

1. **Vibe coding** — casual requests, eyeball if it "seems to work", no real checking. *("Vibe" =
   gut feel.)* Fine for a throwaway experiment, a hackathon, a one-off script you'll delete.
2. **Structured AI-assisted coding** — detailed instructions, you check the important parts. Good
   for a feature inside an existing app.
3. **Agentic engineering** — written specs, automated tests AND evals, safety gates, review. The
   mode for real products people depend on.

**The point:** the thing that separates these is not whether you use AI — it's **how the output
gets verified**. And: *match the effort to the stakes.* Don't wrap a one-line throwaway in heavy
machinery, and don't vibe-code your real product.

**What the kit does:** it's built for the agentic end (spec → plan → tasks → TDD → review). For the
lighter end on purpose, the `prototype` skill builds a throwaway you then delete, and Principle V
(simple + surgical) + `/lean-review` stop you over-building. If a job is genuinely throwaway, say so
and use `prototype` instead of the full pipeline.

---

## 2. The new bottleneck is the spec, not the typing

A *bottleneck* = the slowest, most limiting step. Now that AI writes code fast, the hard part is no
longer typing code — it's deciding *clearly what to build*. So the value moves to writing a good
**spec** (a clear description of what + why, before code).

**What the kit does:** this is its whole thesis — "plan before code", `/speckit-specify` →
`/speckit-plan`. Already covered; this is just the *why*.

---

## 3. The 80% problem

AI cheerfully delivers the first ~80% of a feature fast. The last ~20% — the weird **edge cases**
(unusual situations at the edge of normal use, e.g. a name with an emoji in it), the seams where
systems join, and the parts that need real knowledge of *your* specific business — is where it
stalls and needs a human. Plan for that last 20% being the slow, human part; don't assume "80% done
in an hour" means "done in 75 minutes."

**What the kit does:** the review + verify gates and the human-approval points (checklist Factor 7)
are where that last 20% gets caught. Good to name it so expectations are honest.

---

## 4. Two ways to work: conductor vs orchestrator

- **Conductor mode** — you're hands-on, steering the AI moment by moment (like conducting an
  orchestra live). Best for exploring unfamiliar code, where you want to watch every step.
- **Orchestrator mode** — you hand the AI a well-defined goal, let it run on its own, and review
  the result afterward. *Orchestrate* = set in motion, then step back. Best for clear, repetitive
  jobs: migrations, generating tests, refactoring.

You switch between them within one work session.

**What the kit does:** most skills are orchestrator-style (give a goal, get a reviewed result).
`/loop-design` already helps you pick the right execution shape for a job, which is the same
instinct. Worth knowing the two names so you can ask for one explicitly.

---

## 5. The money curve + model routing

- **The cost curve:** vibe coding is cheap to *start* but gets expensive *later* — the paper
  estimates **3–10× more per feature** over time, because you keep paying to fix the mess
  (re-work, security clean-up, confusion). Agentic engineering costs more up front (specs, tests,
  structured context) but far less per feature after that. Past a crossover point, doing it
  properly is the cheaper path.
- **Model routing** — automatically sending each task to the right-sized AI: an expensive, powerful
  model for hard reasoning; a cheap, small model for routine grunt work (simple tests, basic
  checks). *Routing* = directing each job to the appropriate place. This is the single biggest lever
  on running cost.

**What the kit does:** `docs/token-quick-wins.md` covers cheap-tier routing and other savings, and
the `autopilot` skill already routes mechanical sub-work to the cheap model tier. The cost-curve
framing above is the *why* behind "plan before code" paying off.

---

## 6. Open standards: MCP and A2A

A *standard* = an agreed common format so different tools work together; *open* = free for anyone.

- **MCP** = *Model Context Protocol* — a standard way to plug tools and live data into an AI
  (*protocol* = agreed rules for how two things talk). The kit already uses it: the GitMCP and
  `cookbook` connections in `.mcp.json` (see `AGENTS.md` → "Grounding against real library docs").
- **A2A** = *Agent-to-Agent* — a standard for one AI agent to hand work to another. The kit doesn't
  use this today; it's worth knowing the name for if/when a project needs multiple agents that
  delegate to each other.

---

## The one-line summary

> "AI amplifies whatever engineering culture it lands in — the good parts and the bad parts both."

Generation (writing code) is largely solved. The remaining work — and where this kit focuses — is
**specification rigor** (a clear spec) and **verification** (tests for the logic, evals for the AI).
See `docs/ai-feature-checklist.md` (#14 evals, #15 watch-after-launch) and
`docs/context-engineering.md`.
