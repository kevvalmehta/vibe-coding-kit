# Tasks 016 — Opus Hardening Layer

## Phase 1 — hooks (this branch)
- [x] T1 Write failing tests for lessons_injector (confirmed-only extraction, candidate exclusion, no-op paths)
- [x] T2 Implement scripts/lessons_injector.py
- [x] T3 Write failing tests for done_claim_verifier (claim+no-evidence blocks, claim+evidence passes, stop_hook_active no-op, opt-out marker, no-claim no-op)
- [x] T4 Implement scripts/done_claim_verifier.py
- [x] T5 Write failing tests for regrounding (snapshot content, non-git no-op)
- [x] T6 Implement scripts/regrounding.py
- [x] T7 Write failing tests for import_reality_check (stdlib ok, installed ok, local ok, invented flagged, relative js ok, dep js ok, unknown js flagged)
- [x] T8 Implement scripts/import_reality_check.py
- [x] T9 Wire all four into .claude/settings.json
- [x] T10 Full suite green (208 passed; also fixed the README inventory gate) + live smoke of each hook via piped JSON
- [x] T11 Register in AGENTS.md + SKILL-MAP.md + HANDOFF.md
- [x] T12 Mirror to vibe-coding-kit (scripts + hooks.json + docs) — VCK branch 016-opus-hardening, commit 4c4cc3e, suite 239 green

**Independent Test**: pipe a fabricated Stop-event JSON with a "tests pass" claim and no
pytest run into done_claim_verifier.py; it must emit a block decision. Pipe the same with
a pytest tool_use present; it must stay silent.

## Phase 2 — activate existing gates (this branch)
- [x] T13 TDD-Guard default-on with `.no-tdd-guard` opt-out (tests updated; fail-open in default mode)
- [x] T14 Semgrep `continue-on-error: false` in ci.yml (security findings now block)
- [x] T15 Wire check-plan.ps1 -Gate as a PR-only CI job (no half-done feature merges)
- [x] T16 lint-goal.py made REQUIRED in /goal skill (exit 0 before handoff)
- [x] T17 Fix red inventory test (README index completed — done in Phase 1 commit)

## Phase 3 — production gaps (this branch)
- [x] T18 Dependency vuln scanning (pip-audit/npm audit CI job, BLOCKING + Dependabot config)
- [x] T19 DB migration safety guidance (docs/production-readiness.md §2 — additive-first + backup-before)
- [x] T20 Error monitoring recipe (docs/production-readiness.md §3 — Sentry, beyond AI-drift /monitor)
- [x] T21 Data backup/restore recipe (docs/production-readiness.md §4 — incl. test-the-restore rule)
- [x] T22 Load smoke + accessibility (docs/production-readiness.md §5-6; git-safety walks all six at deploy; guard test tests/test_production_readiness.py)
