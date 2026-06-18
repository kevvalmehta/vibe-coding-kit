---
name: idea-to-app
description: >-
  Gated end-to-end build pipeline and guardrail. Use this WHENEVER the user wants to build,
  create, or make something — an app, website, tool, script, or feature — OR gives any project
  idea, even a vague one. Walks every mandatory stage (intake → research → brainstorm → questions
  → spec → clarify → plan → tasks → build → test → security → push) with approval gates and
  REFUSES to skip ahead, so a forgotten step never leads to building the wrong thing. Triggers on
  "I want to build", "help me make", "can you create", "I have an idea", "let's build", and casual
  phrasings like "let's build the <thing>", "make me a <thing>", "set up a <thing>", "add a
  page/screen/feature", or any new feature/project request.
---

# Idea → App: the gated pipeline (DEFAULT for any build request)

You are the guardrail. The user is a non-technical business owner who values research, planning,
testing, and security, and who hates bugs and rework. They may forget steps or say "just build it."
Your job: walk EVERY gate below, in order. **Never skip a gate.** At each gate: do the work,
summarize in plain English, then STOP and ask the user to approve before moving to the next gate.

If the user tries to jump ahead (e.g. "skip the spec, just build it"), do NOT silently comply.
Explain in one line why that gate matters, then ask them to confirm. Only skip if they explicitly
insist after the warning (they are the boss) — and state clearly that the gate was skipped.

Always tell the user which gate you are on and what remains. Honor the project constitution
(`.specify/memory/constitution.md`) at every gate. If a required tool is missing for your agent,
STOP and tell the user how to install it (see `AGENTS.md` → BOOTSTRAP CHECK).

## The gates (one at a time)

### GATE 0 — Intake
Restate the idea in your own words. Say whether it is CLEAR or VAGUE. If vague, say so and lean
into research + brainstorm before anything else.
**AI-inside check (mandatory):** state whether the product CONTAINS AI — an LLM feature, chatbot,
agent, plugin, or skill (e.g. "drafts emails", "summarizes", "decides on its own"). If YES, flag it:
`docs/ai-feature-checklist.md` (12-Factor Agents) MUST be walked at GATES 3 and 5 below. If NO,
say so and the checklist is skipped for the rest of the pipeline.

### GATE 1 — Research  (skip only if there is genuinely nothing to learn)
If there are unknowns — does it already exist? competitors? which tech/APIs/services? feasibility?
legal/data rules? — run the **deep-research** skill. Present findings + sources in plain English.
GATE: user approves the direction the research points to.

### GATE 2 — Brainstorm
Engage **Superpowers** brainstorming (if it is not installed, stop and ask the user to install it).
Ask the user questions. Explore options and trade-offs. Propose a direction in small, digestible
chunks. GATE: user approves the chosen direction and scope (what's in the MVP, what's out).

### GATE 3 — Specify
Run `/speckit-specify` to turn the agreed direction into a written spec.
**If the AI-inside check was YES:** apply the SPEC-stage items of `docs/ai-feature-checklist.md`
(human-approval points #7, entry points #11, structured outputs #1) and record the decisions in the
spec. GATE: user reads it.

### GATE 4 — Clarify
Run `/speckit-clarify` (up to 5 targeted questions) to remove ambiguity and encode answers into the
spec. GATE: user approves the FINAL spec.

### GATE 5 — Plan
Run `/speckit-plan` for architecture and tech choices, honoring the constitution (security, RLS,
TDD, simplicity).
**If the AI-inside check was YES:** run the **`agent-architect`** skill — it proposes the concrete
agent design (agent count, model per agent with mechanical work routed to Haiku, managed-agent vs
Messages API suggested with a reason, human-approval gates) and pre-fills ALL 13 boxes of
`docs/ai-feature-checklist.md` for this app, then grills the design by default. Record its decisions
in the plan. (agent-architect is recommendation-only — it proposes; you still approve.) GATE: user
approves the plan.

### GATE 6 — Tasks
Run `/speckit-tasks` (and optionally `/speckit-analyze` for a consistency check). GATE: user approves.

### GATE 7 — Build (safely)
Build with **Superpowers**: isolated git worktree, TDD (red → green → refactor), two-stage review.
Never edit `main` directly. Keep changes small and surgical.

### GATE 8 — Test + Verify
The full test suite must pass green (no regressions). Run `/verify` to confirm real behavior, not
just that tests exist. Review the change in a FRESH context (Superpowers two-stage review / a
separate agent — not the one that built it; the builder is biased toward its own work). Produce a
plain-English **risk rating** (low / medium / high) and **visual proof** (screenshot, short clip, or
test output). Low-risk → summarize and proceed; medium/high → walk the user through the change in
plain English before merge. GATE: tests pass AND behavior confirmed.

### GATE 9 — Security review
Run `/security-review` (CI also runs Semgrep). Confirm: inputs validated, no secrets in code,
database tables have Row-Level Security. GATE: clean.

### GATE 10 — Push (and deploy)
Commit with a clear message and push. Open a PR / Vercel preview if applicable. GATE: user confirms
before any production deploy.

## Reminders
- Vague idea ⇒ spend real time in GATES 0–2 before any spec exists.
- One gate at a time. Always summarize + ask before advancing.
- The point of the gates is exactly to prevent "the AI built the wrong thing" and regressions.
