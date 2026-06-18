# Audit Briefs — Perfecting Coding Spec Kit, generated 2026-06-13

From `/audit quick` (hotspots, HIGH-confidence only). Each executor: read the brief fully, honor its
STOP conditions, update your row when done. All briefs planned at commit `4487c42`.

## Execution order & status
| Brief | Title | Category | Effort | Depends on | Execute with | Status |
|-------|-------|----------|--------|------------|--------------|--------|
| 001 | Make CI actually run the Python test suite | tests | S | — | /safe-change | DONE (committed `714ac39` on branch `fix/ci-runs-python-tests`; pending merge+push) |
| 002 | Close the file handle in lint-goal.py | bug | S | — | /safe-change | DONE (committed `a78dacc` on branch `fix/lint-goal-file-handle`; pending merge+push) |
| 003 | Harden tdd_guard.py — drop shell=True | security | S | — | /safe-change | DONE (committed `3958366` on branch `fix/tdd-guard-shell-false`; pending merge+push) |

Status: TODO | IN PROGRESS | DONE | BLOCKED (one-line reason) | REJECTED (one-line rationale)

## Dependency notes
- None — 001 and 002 are independent and touch different files (`ci.yml` vs `scripts/lint-goal.py`).
- Recommended order: **001 first** (high leverage — your CI safety net is currently off), then 002
  (minor hygiene; consider folding it into a ruff-`SIM`-rule pass).

## Considered and rejected (so nobody re-audits these)
- ~~`scripts/tdd_guard.py:70` `subprocess.run(shell=True)` — by-design (trusted repo-local marker).~~
  **PROMOTED to brief 003** on 2026-06-14: Semgrep flagged it independently, and a closer look found a
  real (narrow) hostile-repo edge — worth hardening to `shell=False`, not rejecting.
- `scripts/autopilot_state.py` and `scripts/tdd_guard.py` core logic — read both; well-structured and
  test-covered (`test_autopilot_state.py`, `test_autopilot_v2.py`, `test_tdd_guard.py`). Clean.

## Not audited (quick depth)
Performance, dependencies & migrations, docs, direction/features, the 14 PowerShell scripts beyond
`ci.yml`, and the markdown skill prose. Run `/audit` (standard) or `/audit deep` to cover those.
