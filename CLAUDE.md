# Perfecting Coding Spec Kit

Personal spec-driven development workspace. Describe an app in plain English →
get a proper spec, plan, and a tested build that does not break when edited later.

Owner is a non-technical business owner. Explain decisions in plain language; avoid jargon unless asked.

## The Stack (one source of truth, one builder)
| Layer | Tool |
|---|---|
| Plan / spec | GitHub Spec Kit — `/speckit-*` skills |
| Build safely | Superpowers (Claude Code plugin) — TDD, isolated worktrees, two-stage review |
| Version control | git + GitHub |
| CI gate | GitHub Actions + Semgrep + ruff + Biome/tsc (tests + security scan + Python & JS/TS lint on every change) |
| App + database | Streamlit/Python or web app; Supabase (Postgres + Row-Level Security) |
| Hosting | Vercel (preview URL before live) |

## The Workflow
```
Idea (plain English)
 → /speckit-constitution   rules (done once; see .specify/memory/constitution.md)
 → /speckit-specify        what + why
 → /speckit-clarify        optional: de-risk unclear parts
 → /speckit-plan           how (architecture)
 → /speckit-tasks          small testable steps
 → /speckit-analyze        optional: consistency check
 → build with Superpowers  isolated copy, TDD, two-stage review
 → GitHub Actions gate → Vercel preview → approve → live
```

**Lost? Run `/guide`** — the mentor. It reads where your project is and tells you the one next step +
the exact skill to run, and stops you if you skip ahead (e.g. coding with no plan). Plain-English map
of every skill: **`SKILL-MAP.md`**.

## Optional planning skills (adopted from Matt Pocock, MIT)
Sharpen the PLAN stage — they never start the build. Full details in `AGENTS.md`.
- **grill-me** — interrogates your plan, one question at a time, until every decision is resolved.
- **grill-with-docs** — same, but checked against your existing code + a glossary/decision records.
- **zoom-out** (`/zoom-out`) — plain-English map of how a piece of code fits the bigger picture.
- **prototype** — a throwaway demo to feel out a design before the real build, then deleted.

## Building apps that CONTAIN AI (agents, chatbots, LLM features, plugins/skills)
Walk **`docs/ai-feature-checklist.md`** (12-Factor Agents, plain English) during
`/speckit-specify` + `/speckit-plan`. It also covers when to use Claude Managed Agents
vs the plain Messages API. Skip it for ordinary apps with no LLM inside.

## Stop the AI guessing a library's API — GitMCP (optional)
Before writing code against a library (Streamlit, Supabase, the Anthropic SDK, anything),
point the AI at the library's REAL current docs instead of its memory: add
`https://gitmcp.io/{owner}/{repo}` (or `gitmcp.io/docs` for any repo) to your MCP config.
Optional connector, not a skill; backs Principle VII (no invented APIs). Full details +
caveats in `AGENTS.md` → "Grounding against real library docs".

## Hard Rules (full text: .specify/memory/constitution.md)
1. **Plan before code** — nothing built before spec + plan approved.
2. **TDD always** — tests pass + full suite green = done.
3. **Never break working code** — isolated worktree; regression tests gate every merge.
4. **Security first** — validate inputs, secrets in env only, RLS on every table.
5. **Simple + surgical** — minimum code, touch only what's needed.
6. **LLM portability** — nothing (kit or project) may depend on a single AI tool. A skill,
   guardrail, or process change is NOT done until registered in `AGENTS.md` + `SKILL-MAP.md`.
7. **Pin dependencies exactly** — no `^`/`~` version ranges; use `npm ci` (installs exactly what
   the lockfile says) instead of `npm install` in test/CI loops, so builds are reproducible and a
   newly-published malicious package version can't slip in unnoticed.

## Current State
Read **HANDOFF.md** first — it holds what's built, what's next, and recent decisions.

## AI Portability
Follows the AI-portable standard: CLAUDE.md / AGENTS.md / HANDOFF.md / README.md / plan.md
+ `docs/memory-snapshot/`. For other AI tools, see README → "Switching AI Tools."

## Recall (don't start like a goldfish)
Every session is already saved in full on disk (Claude Code transcripts) next to your memory files —
storage was never the gap, **search** was. Before saying you don't remember something, run
`python scripts/recall.py <keywords>` (add `--all` for every project): it prints dated matches from
your memory + past transcripts. Local-only (no network / AI / telemetry). This is the recall half of
the "stop forgetting like a goldfish" fix.

<!-- SPECKIT START -->
For additional context about technologies to be used, project structure,
shell commands, and other important information, read the current plan:
`specs/004-audit-advisor/plan.md` (Audit Advisor — the /audit existing-code advisor skill).
<!-- SPECKIT END -->
