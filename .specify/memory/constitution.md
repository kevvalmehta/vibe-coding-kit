# Perfecting Coding Spec Kit — Constitution

The rules every spec, plan, and line of code in this project must obey.
The AI coding agent treats these as non-negotiable. When in doubt, this file wins.

## Core Principles

### I. Plan Before Code (NON-NEGOTIABLE)
No code before a spec and plan exist and are approved.
Flow: `/speckit-specify` → `/speckit-plan` → `/speckit-tasks` → approve → build.
If requirements are unclear, run `/speckit-clarify` and ask — never guess.

### II. Test-First / TDD (NON-NEGOTIABLE)
Every feature ships with tests. Red → Green → Refactor: write a failing test,
make it pass, then clean up. A change is not "done" until its tests pass AND the
full existing suite still passes.

### III. Never Break Working Code (Regression Safety)
The agent works in an isolated copy (git worktree/branch), never directly on `main`.
Before anything merges: the full test suite runs green and the change is reviewed
in a fresh context (a separate agent/session that did NOT write the code — the builder is
biased toward its own work) against the plan. If an edit breaks an existing test, STOP and fix it — never
disable, skip, or delete a test to make the bar go green.

### IV. Security First
- Validate and sanitize all inputs. Never trust user data.
- Secrets live in environment variables only. Never hardcode keys; never commit `.env`.
- Database: enable Row-Level Security (RLS) on every table; deny by default.
- Run a security review (`/security-review` or Semgrep) before shipping.

### V. Simplicity & Surgical Changes
Minimum code that solves the problem. No speculative features (YAGNI).
Touch only what the task requires. Don't refactor or "improve" unrelated code.
Match existing conventions.

### VI. LLM Portability (NON-NEGOTIABLE)
Nothing in this kit -- or in any project built with it -- may depend on a single AI tool to work.
`AGENTS.md` is the agent-neutral entry point and must always say what `CLAUDE.md` says; a guardrail,
skill, or process change is NOT done until it is registered in `AGENTS.md` (+ `SKILL-MAP.md`).
Custom skills live in `.claude/skills/` as plain markdown: non-Claude agents (Codex, Gemini,
Cursor, ...) MUST read and follow the relevant `SKILL.md` on demand -- `SKILL-MAP.md` maps the
situation to the skill. Claude-only mechanisms (hooks, plugins) need a documented manual fallback
in `AGENTS.md`. Every project built here keeps the AI-portable file standard (CLAUDE.md / AGENTS.md
/ HANDOFF.md / README.md / plan.md + `docs/memory-snapshot/`).

### VII. Truth Over Confidence (NON-NEGOTIABLE)
A confidently-wrong claim is worse than an admitted gap — and the AI being sure of a thing it
never checked is the failure this kit most guards against. The agent must:
- **Verify before claiming.** Never say something is built / current / pushed / done / passing
  from memory. Show the verifying output in the SAME message: git state for "pushed/current/clean",
  file timestamp + source commit for "built", the test-run output for "tests pass". No proof in the
  same message → no claim.
- **No ungrounded assumptions.** Do not invent file names, functions, APIs, flags, paths, numbers,
  or behavior. If it wasn't read or run this session, don't assert it — read the file / run the
  command first, or label it unverified.
- **Label confidence.** Distinguish "verified (output shown)" from "believe, unchecked" from
  "guessing." When unsure, say so or check — never mask a gap with confident phrasing.
- **State assumptions, then verify or ask.** On ambiguity, list assumptions, mark each
  verified/unverified, confirm the unverified before building. Surface conflicts; don't silently pick one.
- **Re-ground after summarization / at session start** before any state claim: re-run git status,
  git log -1, and the relevant tests. A summary is memory, not proof.

## Quality Gates (must all pass before "done")
1. Spec + plan approved, and the plan passes the seam check — `scripts\check-plan.ps1` when the plan
   is written (every Independent Test measurable, no scaffolding left), and `scripts\check-plan.ps1 -Gate`
   before merge (no unchecked tasks, no vague tests). The script decides plan↔build match, not the agent's word.
2. Tests written and passing (unit + integration for new contracts).
3. Full existing test suite still green — no regressions.
4. Security review clean — inputs validated, no secrets in code, RLS on.
5. Plain-English errors for end users — no raw stack traces shown.
6. Change reviewed in a fresh context; the PR carries a plain-English risk rating
   (low / medium / high) and visual proof (screenshot, short clip, or test output) that it
   works — so review is by risk + proof, not by reading code line-by-line.
7. Every "done / pushed / current" claim carries its proof in the same message (git state + test
   output); no ungrounded assumptions, invented names, or unchecked facts stated as truth;
   uncertainty is labelled, not hidden (Principle VII).

## Tech Stack (defaults — override per project in the spec)
- Build agent: Claude Code + Superpowers (TDD, isolated worktrees, two-stage review)
- Spec / plan: GitHub Spec Kit (`/speckit-*` skills)
- App: Python / Streamlit for internal tools unless specified otherwise
- Database: SQLite early → Supabase (Postgres + RLS) for deployment
- Hosting: Vercel; CI: GitHub Actions (tests + Semgrep on every change)

## Version Control & Recovery
- Work on a branch or worktree, never directly on `main`; merge via Pull Request. `main` stays working.
- Commit small with clear messages; push often (cloud backup). Tag known-good versions.
- Undo safely: prefer `git revert`; confirm before any destructive op; never force-push `main`.
- Before risky work (refactor, deletes, dependency bumps), make a save point (commit + push) first.
- Secrets stay in `.env` (gitignored) — never committed.

## Governance
This constitution supersedes other practices. The agent must verify compliance on
every spec, plan, and change, and must surface — not hide — any rule it cannot meet.
Before any spec, plan, or change is "done", the agent must read `lessons.md` (the scar log)
and run each entry's self-check; mistakes worth never repeating get logged there, and a scar
is promoted into a Principle here when it earns it.
Amendments: edit this file (or run `/speckit-constitution`), bump the version, note the date.

**Version**: 1.5.0 | **Ratified**: 2026-06-06 | **Last Amended**: 2026-06-11
