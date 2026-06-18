# Perfecting Coding Spec Kit

**Describe an app in plain English → get a proper spec, a plan, and a _tested_ build that doesn't
break when you edit it later.**

This is a personal, spec-driven coding workspace built on **GitHub Spec Kit + Superpowers** inside
Claude Code. It's designed for a **non-technical owner**: you describe what you want in normal words,
and the kit walks you through planning, building safely, testing, and shipping — refusing to skip the
steps that prevent expensive mistakes.

> **New here? The only thing you have to remember is one command: `/guide`.**
> Type it any time and it tells you exactly where you are and what to do next.

---

## Table of contents
1. [The big idea](#the-big-idea)
2. [Quick start — build your first app](#quick-start--build-your-first-app)
3. [The full workflow, explained](#the-full-workflow-explained)
4. [The safety nets (what protects you)](#the-safety-nets-what-protects-you)
5. [Changing something you already built](#changing-something-you-already-built)
6. [Saving, undoing, and never losing work](#saving-undoing-and-never-losing-work)
7. ["I want to… → do this" quick reference](#i-want-to--do-this-quick-reference)
8. [Planning helpers (sharpen the idea before building)](#planning-helpers-sharpen-the-idea-before-building)
9. [What "done" means (the rules)](#what-done-means-the-rules)
10. [The stack](#the-stack)
11. [File index](#file-index)
12. [Starting a brand-new project from this template](#starting-a-brand-new-project-from-this-template)
13. [Switching AI Tools](#switching-ai-tools)
14. [FAQ / troubleshooting](#faq--troubleshooting)

---

## The big idea

Three promises, enforced automatically so you can't accidentally skip them:

1. **Plan before code.** Nothing gets built until there's a written spec and plan you've approved.
   This kills the #1 cause of wasted work: building the wrong thing.
2. **Build safely.** Code is written on an isolated copy, with tests written *first*, and reviewed by
   a *fresh* set of AI eyes before it merges.
3. **Never break working code.** Every change is reversible, and the full test suite must stay green
   before anything ships. Your live app stays working.

You stay in control with plain-English approval at every gate. You never have to read code — you
review the **plan** and a **preview** of the result.

---

## Quick start — build your first app

Open this folder in **Claude Code** and type, in plain English, what you want. For example:

> "I want to build a simple tool where my team logs daily sales and I see a weekly chart."

That's it — the kit takes over and walks you through the gates below, one at a time, asking your
approval before each step. If you're ever unsure, type **`/guide`**.

**What happens, step by step:**

| Step | You do | The kit does |
|---|---|---|
| 1. Idea | Describe it in plain words | Restates it back; flags if it's clear or vague |
| 2. Research | Approve | Checks if it exists, what tools fit, any risks |
| 3. Brainstorm | Answer a few questions | Explores options, recommends a direction |
| 4. Spec | Read & approve | Writes *what + why* (`/speckit-specify`) |
| 5. Clarify | Answer up to 5 questions | Removes fuzziness (`/speckit-clarify`) |
| 6. Plan | Read & approve | Decides *how* — architecture (`/speckit-plan`) |
| 7. Tasks | Approve | Breaks it into small steps, each with a "Done when" (`/speckit-tasks`) |
| 8. Build | Wait (or do other things) | Writes tests first, then code, on a safe copy |
| 9. Verify | Look at the screenshot | Confirms it really works + gives a risk rating |
| 10. Security | Approve | Checks inputs, secrets, database locks |
| 11. Ship | Approve the preview | Opens a Vercel preview link → you OK → goes live |

You can stop at any gate. Nothing is permanent until you approve the final step.

---

## The full workflow, explained

```
idea (plain English)
 → /guide                  "where am I, what next?"  (ask anytime)
 → idea-to-app             walks every gate below, refuses to skip
 → research                does it exist? competitors? which tools?
 → brainstorm + grill-me   pressure-test the idea until decisions are resolved
 → /speckit-specify        write WHAT + WHY (the spec)
 → /speckit-clarify        answer up to 5 questions to remove fuzziness
 → /speckit-plan           decide HOW (architecture)
 → /speckit-tasks          break into small steps, each with a "Done when"
 → build                   Superpowers: isolated copy, tests first, fresh-eyes review
 → /verify                 confirm it really works (+ risk rating + screenshot)
 → /security-review        inputs, secrets, database security
 → git-safety              save + Pull Request → preview → live
```

**The Spec Kit commands** (you can type these directly, or just let `idea-to-app` run them for you):

| Command | What it does |
|---|---|
| `/speckit-constitution` | Set or update your rules (done once; see `.specify/memory/constitution.md`) |
| `/speckit-specify` | Turn your idea into a written spec (what + why) |
| `/speckit-clarify` | Ask up to 5 targeted questions to remove ambiguity |
| `/speckit-plan` | Decide the architecture (how it gets built) |
| `/speckit-tasks` | Break the plan into small, testable steps |
| `/speckit-analyze` | Optional consistency check across spec, plan, and tasks |
| `/speckit-implement` | Build the tasks |

---

## The safety nets (what protects you)

These are **guardrail skills** — they switch on automatically based on what you say, so you don't have
to remember them. They're the heart of the kit.

| Skill | Switches on when you… | What it guarantees |
|---|---|---|
| **`/guide`** | are unsure, or say "what next", "where am I", "I'm lost" | Tells you the one next step + exact skill; corrects you if you skip ahead |
| **`idea-to-app`** | give any new build idea ("let's build…", "make me a…") | Walks every gate; **refuses to skip** to coding |
| **`safe-change`** | want to change/fix/edit existing code | Maps impact → tests → isolated edit → fresh-eyes review, so one change can't silently break another |
| **`git-safety`** | do anything git ("save", "undo", "it broke", "publish") | Keeps `main` working; every change reversible; runs the git for you |

**The key behavior you asked for:** if you jump straight to "just code it" with no plan, the kit
**stops you, explains why in one line, and points you to planning first**. You're the boss — if you
insist after the warning, it proceeds but tells you which safety step was skipped.

---

## Changing something you already built

Editing existing code is a *different, more careful path* than building new — because a careless edit
can break something elsewhere. Just say what you want in plain English:

> "Make the sales chart show months instead of weeks."

The **`safe-change`** skill takes over and:
1. Reads the code **and everything that depends on it** (so nothing breaks by surprise).
2. Shows you an **impact map** — what this change could touch.
3. Makes sure there are tests covering today's behavior *before* editing.
4. Works on an isolated copy, makes the smallest change that does the job.
5. Runs the **full** test suite — if anything breaks, it stops and fixes it (never hides a failure).
6. Reviews the change with **fresh AI eyes** and gives you a **risk rating + screenshot**.

---

## Saving, undoing, and never losing work

You don't need to know git. The **`git-safety`** skill runs it for you and explains in plain English.
Plain-language guide: **`GITHUB-GUIDE.md`**.

- **Save your work / back it up:** say "save my work" — or run `scripts/save.ps1 -Message "what changed"`
  (does save + backup to GitHub in one go).
- **Undo a change:** say "undo that" or "go back" — it reverses it safely, keeping full history.
- **It broke:** say "it broke" — it helps you get back to the last working version.
- **Golden rule the kit follows for you:** never work directly on the live version (`main`); every
  change happens on a branch and merges via a Pull Request, so `main` always works.

---

## "I want to… → do this" quick reference

Full plain-English map lives in **`SKILL-MAP.md`**. The short version:

| When you're… | Say / run | 
|---|---|
| Lost — "what do I do now?" | **`/guide`** |
| Starting any new idea (even vague) | Just describe it → `idea-to-app` takes over |
| Pinning down a fuzzy plan | "grill me" → `grill-me` |
| Unsure how a piece of code fits | `/zoom-out` |
| Want to try a design before committing | "prototype this" → `prototype` |
| Changing / fixing existing code | Just say what to change → `safe-change` takes over |
| Stuck on a bug | Describe it → `systematic-debugging` |
| Anything git (save, undo, branch, publish) | Say it → `git-safety` |
| Confirming a change works | `/verify` |
| Checking security before shipping | `/security-review` |

---

## Planning helpers (sharpen the idea before building)

Optional skills that make the **planning** stage sharper. They never start the build. (Adopted from
Matt Pocock's skills, MIT — full notes in `AGENTS.md`.)

- **`grill-me`** — interrogates your plan, one question at a time, until every decision is resolved.
- **`grill-with-docs`** — same, but checked against your existing code + recorded decisions.
- **`/zoom-out`** — a plain-English map of how a piece of code fits the bigger picture.
- **`prototype`** — a throwaway demo to feel out a design before the real build, then deleted.

---

## What "done" means (the rules)

A change is only "done" when all of these pass (full text: `.specify/memory/constitution.md`):

1. Spec + plan approved.
2. Tests written and passing.
3. The **full** existing test suite still green — no regressions.
4. Security clean — inputs validated, no secrets in code, database Row-Level Security on.
5. Plain-English errors for users — no scary stack traces.
6. Reviewed with **fresh eyes** (a different AI than the one that wrote it), with a **risk rating +
   visual proof** (screenshot) — so you review by risk and proof, not by reading code.

---

## The stack

| Layer | Tool |
|---|---|
| Plan / spec | GitHub Spec Kit — `/speckit-*` commands |
| Build safely | Superpowers (Claude Code plugin) — tests-first, isolated copies, fresh-eyes review |
| Version control | git + GitHub |
| Safety gate | GitHub Actions + Semgrep (tests + security scan on every change) |
| App + database | Streamlit/Python or web app; Supabase (Postgres + Row-Level Security) |
| Hosting | Vercel (preview link before live) |

---

## File index

> **Completeness rule (enforced).** This is the *complete* index — every file/folder group in the kit
> is listed below. When you (or any AI tool) summarize "what's in the kit", enumerate from this table or
> the live file tree — **never from memory**. If you add a new file/skill/script, add it here in the
> same change. This is not just a request: `scripts/check_inventory.py` runs in CI (via pytest) and
> **fails the build** if any skill, script, or top-level doc is missing from this index.

### Root docs
| File | What it's for |
|---|---|
| `CLAUDE.md` | Full project brief — Claude Code auto-reads it every session |
| `AGENTS.md` | Same brief for other AI tools (Codex, Cursor, Copilot) |
| `HANDOFF.md` | Current state — what's built, what's next, recent decisions (read first) |
| `README.md` | This file — human overview + AI switching prompt + full index |
| `SKILL-MAP.md` | Plain-English "which skill for which moment" cheat sheet |
| `GITHUB-GUIDE.md` | Plain-English guide to saving / undoing / publishing |
| `SETUP.md` | How to spin up a new project from this kit |
| `plan.md` | Historical phased build plan |

### Skills — `.claude/skills/` (run inside Claude Code; mirrored in `.agents/skills/` for other AI tools)
| Skill | What it's for |
|---|---|
| `guide` | The mentor/router — `/guide`: "where am I, what's next, which skill?" |
| `idea-to-app` | Guardrail — walks every gate for a new build, refuses to skip |
| `safe-change` | Guardrail — regression-safe edits to existing code |
| `git-safety` | Guardrail — keeps `main` working, every change reversible |
| `health` | `/health` — one 0–100 score across 12 checks + fix-this-first ledger |
| `audit` | `/audit` — deep "what's worth fixing" pass (+`references/`: playbook, brief-template, routing-and-modes) |
| `autopilot` | Runs specify→clarify→plan→tasks→checks as one guided flow (+`references/`: gates, parallel-plan, prepr-checks) |
| `agent-architect` | Proposes the agent design for apps that contain AI (+`references/decision-routine.md`) |
| `goal` | Turns a vague ask into a task contract (outcome + verification + stop rules) |
| `grill-me` | Interrogates a fuzzy plan one question at a time |
| `grill-with-docs` | Same, against your real code + decisions (+`ADR-FORMAT.md`, `CONTEXT-FORMAT.md`) |
| `zoom-out` | `/zoom-out` — plain-English map of how a piece of code fits |
| `prototype` | Throwaway demo to feel out a design (+`LOGIC.md`, `UI.md`), then deleted |
| `speckit-specify` / `-clarify` / `-plan` / `-tasks` / `-analyze` / `-implement` / `-constitution` | The GitHub Spec Kit planning + build commands |
| `speckit-checklist` | Generates a quality checklist for the current feature |
| `speckit-taskstoissues` | Turns the task list into GitHub issues |
| `speckit-agent-context-update` | Keeps the AI brief files (CLAUDE.md/AGENTS.md) current |
| `speckit-git-*` | `commit` / `feature` / `initialize` / `remote` / `validate` git helpers |

### Scripts — `scripts/`
| File | What it's for |
|---|---|
| `save.ps1` | One-command save + backup to GitHub |
| `new-project.ps1` | Spin up a new project from this scaffold (`-Update` re-syncs skills/scripts) |
| `autopilot_state.py` | Deterministic resume helper for `autopilot` (TDD-covered) |
| `tdd_guard.py` | The TDD-Guard enforcement hook (blocks code before a failing test exists) |
| `lint-goal.py` | Lints `/goal` task-contract files |
| `check-plan.ps1` | Plan↔build seam check — is the plan measurable / did the build match it |
| `capture-lessons.ps1` | Stop-hook that logs candidate lessons from your corrections |
| `check_inventory.py` | Inventory coverage gate — fails CI if a skill/script/top-level doc is missing from this index (enforces the Completeness rule above) |

### Spec Kit engine + memory — `.specify/`
| Path | What it's for |
|---|---|
| `memory/constitution.md` | The non-negotiable rules (security, TDD, regression safety) |
| `memory/lessons.md` | Scar log — rules earned from real past mistakes |
| `templates/` | spec / plan / tasks / checklist / constitution templates |
| `scripts/powershell/` | Spec Kit helper scripts (prerequisites, new-feature, setup-plan/tasks) |
| `extensions/git/` | Git extension — `speckit.git.*` commands + bash & powershell scripts |
| `extensions/agent-context/` | Agent-context-update extension + scripts |
| `integrations/` | `claude` / `codex` / `speckit` manifests (multi-LLM) |
| `workflows/` | Spec Kit workflow registry |

### Built features (Spec Kit artifacts) — `specs/`
| Path | What it's for |
|---|---|
| `001-autopilot-orchestrator/` | Full spec/plan/tasks/research/data-model/quickstart/contracts |
| `002-token-quick-wins/` | Spec/plan/tasks for the token-wins doc |
| `003-agent-architect/` | Spec/plan/tasks for the agent-architect skill |
| `004-audit-advisor/` | Spec/plan/tasks for the audit skill |

### Tests — `tests/`
| File | Covers |
|---|---|
| `test_autopilot_state.py`, `test_autopilot_v2.py` | Autopilot resume + v2 gate modes |
| `test_agent_architect.py` | Agent-architect skill guard |
| `test_audit_advisor.py` | Audit skill guard |
| `test_health_skill.py` | Health-score skill guard |
| `test_tdd_guard.py` | TDD-Guard hook |
| `test_token_quick_wins.py` | Token-quick-wins doc guard |

### Docs — `docs/`
| Path | What it's for |
|---|---|
| `ai-feature-checklist.md` | 13 decisions to make when your app contains AI (12-Factor Agents) |
| `awesome-claude-code-shortlist.md` | Vetted shortlist of external tools to consider (not all installed) |
| `token-quick-wins.md` | Six habits to cut token cost per session |
| `memory-snapshot/MEMORY.md` | Portable memory mirror for other AI tools |
| `superpowers/plans/`, `superpowers/specs/` | Design notes (TDD-Guard, workflow-evolution map) |

### Audit findings — `audit/`
| Path | What it's for |
|---|---|
| `001`–`003` + `README.md` | Verified, ready-to-run fix briefs produced by `/audit` on the kit itself |

### Config / CI / connectors
| File | What it's for |
|---|---|
| `.mcp.json` | MCP servers: `gitmcp` (library grounding) + `cookbook` (live Claude Cookbook recipes) |
| `.github/workflows/ci.yml` | CI — Semgrep security scan + ruff + Biome/tsc lint + tests on every push |
| `ruff.toml` | Python linter config (CI `lint` job) |
| `biome.json` | JS/TS linter config (CI `lint-js` job) |
| `.claude/settings.json` | Claude Code project settings (incl. the lessons Stop hook) |
| `.env.example` | Template for secrets (never commit the real `.env`) |
| `.gitignore` | Keeps secrets + state files out of git |

---

## Starting a brand-new project from this template

This kit is reusable. To start a fresh project with all the same guardrails, see **`SETUP.md`** or run:

```
.\scripts\new-project.ps1 -Name "My CRM"
```

That creates `C:\Projects\My CRM` as its **own** folder and its **own** git repo — nothing is built
inside the kit, and nothing merges back into it. The new project carries the **full toolbox**: every
custom skill (`.claude/skills/` + `.agents/skills/`, including `/goal`, `/guide`, `grill-me`, …), every
script (the linters, save/check helpers), the docs, the constitution, and the CI checks. Each new
project then gets its own spec → plan → build cycle and its own always-working `main`.

Because the script copies whole folders, **any skill or script you add to the kit later is included
automatically** — you never edit the script when you build a new skill. To pull your newest skills into
a project you already started, run from the kit folder:

```
.\scripts\new-project.ps1 -Name "My CRM" -Update
```

This re-syncs only the skills and scripts; your project's specs, code, and docs are left untouched.

---

## Switching AI Tools

Starting a session in Codex / Cursor / another AI? Paste this verbatim:

```
You are taking over an existing project. Read these files in this exact order
before writing any code:

1. AGENTS.md         — project brief and architecture
2. HANDOFF.md        — current state (what's built, what's next, hard rules)
3. docs/memory-snapshot/  — Claude Code's mirrored memory (read all files)
4. .specify/memory/constitution.md  — the non-negotiable rules
5. plan.md           — historical context
6. README.md         — human-readable overview

Then check spec status: read the latest files under specs/ (if present) and
.specify/ to see the current spec, plan, and tasks.

After reading, confirm in plain English that you understand the project's
current state, hard rules, and what's open. DO NOT write any code until
confirmation.
```

---

## FAQ / troubleshooting

**I don't know where to start.** → Type `/guide`. It reads the project and tells you the next step.

**I just want to build something fast — do I have to do all the steps?** → The kit will warn you in one
line why a skipped step matters, then let you proceed if you insist. The steps exist to stop you
building the wrong thing or breaking what works — skipping them is how rework happens.

**I'm not a coder. How do I "review" anything?** → You never read code. You review the **plan** (in
plain English) and a **preview/screenshot** of the result, plus a **risk rating** (low/medium/high)
that tells you how much attention a change needs.

**Something broke after a change.** → Say "it broke" or "undo that". `git-safety` walks you back to the
last working version. Because every change is on a branch and reversible, nothing is ever truly lost.

**I want to use Codex/Cursor instead of Claude Code.** → See [Switching AI Tools](#switching-ai-tools)
above. The kit is built so any AI tool picks up exactly where the last one left off.

**Where are the rules the AI follows?** → `.specify/memory/constitution.md`. Change them with
`/speckit-constitution`.
