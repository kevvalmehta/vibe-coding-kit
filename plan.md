# Build Plan — Perfecting Coding Spec Kit

Phased setup of the spec-driven workflow. Historical; live state lives in HANDOFF.md.

## Phase 0 — Toolchain setup
- [x] Remove overlapping tools (TaskMaster engine + prd-taskmaster skill)
- [x] Install uv (Python tool manager)
- [x] Install GitHub Spec Kit + `specify init` (Claude integration, PowerShell scripts)
- [x] Set global git identity + init repo
- [x] Write constitution (security + TDD + regression rules)
- [x] Create portable MD files + .gitignore + .env.example + memory-snapshot
- [x] Install Superpowers plugin (`/plugin install superpowers@claude-plugins-official`)
- [x] Add multi-LLM support (Codex integration + AGENTS.md bootstrap self-prompt)
- [ ] Restart Claude Code; confirm `/speckit-*` skills + Superpowers active

## Phase 1 — First spec (no code)
- [ ] Pick first app idea
- [ ] `/speckit-constitution` — formalize/version the rules
- [ ] `/speckit-specify` — write the spec
- [ ] `/speckit-clarify` — resolve ambiguity
- [ ] `/speckit-plan` — architecture
- [ ] `/speckit-tasks` — task list
- [ ] Review + approve

## Phase 2 — Build (safely)
- [ ] Build with Superpowers (isolated worktree, TDD, two-stage review)
- [ ] All tests green + full suite passes (no regressions)
- [ ] `/security-review` clean

## Phase 3 — Safety net + deploy
- [ ] GitHub remote + push
- [ ] GitHub Actions: run tests + Semgrep on every push (block on failure)
- [ ] Supabase project: enable Row-Level Security on every table
- [ ] Vercel: preview deployment → review → production
