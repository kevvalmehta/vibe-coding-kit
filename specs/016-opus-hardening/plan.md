# Plan 016 — Opus Hardening Layer

## Architecture
Four standalone Python hook scripts in `scripts/`, following the kit's existing hook
contract (see `tdd_guard.py`, `recommender_nudge.py`):
- stdin: hook JSON (`cwd`, `transcript_path`, `session_id`, `tool_name`, `tool_input`,
  `stop_hook_active` where applicable)
- stdout: `hookSpecificOutput` JSON (`additionalContext` for SessionStart) or top-level
  `{"decision": "block", "reason": ...}` (Stop / PostToolUse feedback)
- exit 0 in every path; all exceptions swallowed (a hook must never break a session)

## Wiring (PCK `.claude/settings.json`)
| Script | Event | Matcher |
|---|---|---|
| lessons_injector.py | SessionStart | (all) |
| regrounding.py | SessionStart | resume\|compact |
| done_claim_verifier.py | Stop | * |
| import_reality_check.py | PostToolUse | Edit\|Write\|MultiEdit |

Mirror: same entries in `vibe-coding-kit/plugins/vibe-coding-skills/hooks/hooks.json`
with `${CLAUDE_PLUGIN_ROOT}/scripts/...` paths; scripts copied to plugin `scripts/`.

## Key decisions
1. **Injector loads only confirmed L-#/P-# entries.** Auto-captured candidates are
   unreviewed suspects (and the capture hook demonstrably mis-captures skill text);
   injecting them would feed garbage rules to every session.
2. **Digest, not full file.** Rule + Self-check lines only — keeps per-session token
   cost small and rules sharp. Parse failure on a confirmed entry → include entry as-is.
3. **Verifier scans one turn only** (from last real user message). Claims regex kept
   narrow (tests pass / pushed / committed / build green / deployed) to avoid nagging;
   widen later if misses appear.
4. **Verifier trusts command presence, not output parsing** (v1). Checking "pytest ran"
   catches the dominant lie (claim with zero verification). Output-parsing is a later
   tightening.
5. **Import check is feedback, not rollback.** PostToolUse can't undo an edit; the goal
   is the model hears "that package doesn't exist here" immediately, while it can still
   fix course cheaply.

## Test plan (TDD)
`tests/test_lessons_injector.py`, `tests/test_done_claim_verifier.py`,
`tests/test_regrounding.py`, `tests/test_import_reality_check.py` — pure-function unit
tests on tmp_path fixtures (same style as `test_tdd_guard.py`). Full suite must stay
green (pre-existing `test_inventory_coverage` failure is Phase 2 scope).
