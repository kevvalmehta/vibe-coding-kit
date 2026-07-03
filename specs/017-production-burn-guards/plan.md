# Plan 017 — Production Burn Guards

## HOW

All guards are stdlib-only Python (same style as the four existing hooks: swallow errors,
exit 0, never break a session — EXCEPT preflight_gate, which is a gate and must fail loud
with non-zero exit).

### G1 preflight_gate.py
- `find_secrets(root)`: regex families (AWS `AKIA…`, Google `AIza…`, `sk-…`/`sk-ant-…`,
  GitHub `ghp_…`, private-key PEM headers, generic `(api[_-]?key|secret|token)\s*[:=]\s*['"][^'"]{16,}`).
  Scan git-tracked text files only; skip `.env.example`, lockfiles, tests fixtures dir.
- `check_rls(root)`: parse `CREATE TABLE <name>` vs `ALTER TABLE <name> ENABLE ROW LEVEL
  SECURITY` across migration SQL; report tables missing RLS. No SQL migrations → SKIP.
- `check_rate_limit(root)`: detect API routes; look for known limiter signals
  (`@limiter`, `slowapi`, `express-rate-limit`, `rate_limit`, `Ratelimit`, `upstash`).
  No routes → SKIP.
- Output: table of PASS/FAIL/SKIP + plain-English fix per FAIL. `--json` for CI.
- CI: new blocking job `preflight` running the script against the repo (kit repo itself
  should PASS: no secrets, no migrations → SKIP, no API routes → SKIP).

### G2 destructive_action_gate.py
- PreToolUse. Input JSON: `tool_name`, `tool_input`.
- Bash: strip quoted strings? No — v1 keeps it simple, pattern-match raw command.
  Patterns (case-insensitive): `\brm\s+(-[a-z]*r[a-z]*f|-[a-z]*f[a-z]*r)\b`,
  `\bdrop\s+(table|database|schema)\b`, `\btruncate\s+table?\b`,
  `\bdb\s+reset\b`, `\bdelete\s+from\s+\w+\s*(;|$)` (no WHERE),
  `--dangerously-skip-permissions`, `\bmigrate\s+(reset|down)\b`.
- Edit/Write/MultiEdit: path matches `[\\/]migrations?[\\/]` or `schema\.(prisma|sql)$`.
- Output `{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"ask",
  "permissionDecisionReason":"<plain-English what+risk>"}}`. Reads never gated.
- Registered in settings.json PreToolUse for both `Bash` and `Edit|Write|MultiEdit`
  (one script handles both by tool_name).

### G3 spec_drift_warn.py
- PreToolUse on Bash; act only when command matches `\bgit\s+commit\b`.
- `git diff --cached --name-only` (staged files): if any path starts with app/src/lib/
  scripts/plugins and none start with specs/ or .specify/ → print advisory context
  (systemMessage), NEVER block. Marker `.no-spec-drift-warn` disables.

### G4 settings.json
- Add `"permissions": {"deny": ["Read(./.env*)", "Read(**/*.pem)", "Read(~/.ssh/**)",
  "Read(~/.aws/**)"]}` + register G2, G3 hooks.

### Delegation (frugal-fable routing)
- Fable: spec/plan/tasks, G2 (security-critical hook), settings.json (shared file),
  integration review, PRs.
- Opus agent: G1 + G3 scripts + their tests + CI job (bounded, pattern to copy exists).
- Sonnet agent: all T tweaks + AGENTS.md/SKILL-MAP.md/HANDOFF.md registration (docs only).
- Sonnet agent: VCK mirror after PCK merges (copy + wire plugin hooks.json + README).

### Test strategy
Mirror existing test style (`tests/test_<name>.py`, importlib load from scripts_dir,
tmp_path fixtures). Each guard: happy path, non-applicable SKIP/silence, opt-out marker,
malicious/edge sample. Full suite must stay green.
