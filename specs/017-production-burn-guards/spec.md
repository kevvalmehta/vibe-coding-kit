# Spec 017 — Production Burn Guards

## WHY
Gemini deep-research (2026-07-02, two reports) identified the "90-day solo-founder burn
vectors": leaked secrets, missing Row-Level Security, unthrottled endpoints, destructive
database commands run by agents, and spec/code drift after v1. The kit's existing gates
catch none of these deterministically. These guards close the gap with mechanical checks
that bypass the LLM entirely.

## WHAT

### G1 — Pre-flight security gate (deterministic, no LLM)
A script (`scripts/preflight_gate.py`) that scans a project for the three burn vectors:
1. **Secrets**: regex sweep for hardcoded API keys/tokens/private keys in tracked files.
2. **RLS**: every `CREATE TABLE` in `**/migrations/**/*.sql` (and `supabase/migrations`)
   has a matching `ENABLE ROW LEVEL SECURITY` for that table somewhere in the migrations.
3. **Rate limiting**: if the project has API routes (`app/api/**/route.*`, `pages/api/**`,
   Express/FastAPI routers), at least one recognized rate-limit mechanism is present.
Checks that don't apply (no migrations, no API routes) SKIP, not fail. Exit non-zero on
any failure with plain-English reasons. CI runs it as a blocking job; git-safety's deploy
escalation runs it before any deploy.

### G2 — Destructive-action gate (PreToolUse hook)
`scripts/destructive_action_gate.py` intercepts, BEFORE execution:
- Bash commands matching destructive patterns (`drop table`, `db reset`, `rm -rf`,
  `truncate`, bulk `delete from` without `where`, `--dangerously-skip-permissions`).
- Edit/Write to migration/schema files (`**/migrations/**`, `schema.prisma`, `schema.sql`).
Returns permissionDecision "ask" with a plain-English explanation of what the action
changes, so the owner explicitly approves. Never blocks reads. Opt-out marker:
`.no-destructive-gate`.

### G3 — Spec-drift warner (warn-only)
`scripts/spec_drift_warn.py`: given a git diff, if source dirs changed but no file under
`specs/` or `.specify/` changed, print a WARNING (never block): "Code changed without a
spec update — update the spec first to prevent AI drift." Wired as a PreToolUse hook on
`git commit` commands (advisory output). Opt-out marker: `.no-spec-drift-warn`.

### G4 — Least-privilege deny rules
`permissions.deny` in `.claude/settings.json`: block agent reads of `.env*`, `**/*.pem`,
`~/.ssh/**`, `~/.aws/**`. Documented in AGENTS.md for other AI tools.

### T — Tweaks (docs/templates)
1. Plan template: "Running cost implications" section (call out per-usage costs).
2. Spec template: note — keep specs lean (~300 lines max); over-specifying paralyzes,
   under-specifying hallucinates.
3. agent-eval SKILL.md: judges must use categorical labels (pass/fail/unsafe), never 1–10.
4. git-safety SKILL.md: run preflight gate before deploy; never use
   `--dangerously-skip-permissions`.
5. CLAUDE.md/AGENTS.md: dependency pinning — exact versions (no `^`/`~`), `npm ci` in
   test loops.

## NOT in scope
Prompt-injection elimination (impossible; G2+G4 shrink blast radius — documented honestly),
Architect/Worker separation (already exists), micro-eval sandbox (agent-eval covers it),
Conductor v2/v4.

## Done when
All guards have passing tests; full suite green; registered in AGENTS.md + SKILL-MAP.md
(Principle VI); mirrored to vibe-coding-kit; CI green on both PRs.
