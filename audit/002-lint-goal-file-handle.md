# Brief 002: Close the file handle in lint-goal.py

> **Executor**: Follow this brief step by step. Run every verify command and confirm the expected
> result before moving on. Touch only the files listed In scope. If a STOP condition occurs, stop and
> report — do not improvise.
> **Drift check (run first)**: `git diff --stat 4487c42..HEAD -- scripts/lint-goal.py`
> If `lint-goal.py` changed since this brief was written, compare the Current-state excerpt against the
> live file before proceeding; on a mismatch, treat it as a STOP condition.

## Status
- **Category**: bug (resource leak) · **Effort**: S · **Risk**: LOW · **Confidence**: HIGH
- **Depends on**: none
- **Planned at**: commit `4487c42`, 2026-06-13
- **Execute with**: /safe-change

## Why this matters
`lint-goal.py` opens the goal file without a context manager, so the handle isn't deterministically
closed. At this scale it's cosmetic — but it's exactly the class of thing the kit's own linter should
catch, and the fix is one line. Honest framing: low impact; worth doing only as a quick hygiene pass
(consider bundling with turning on the ruff `SIM` rule so the linter prevents the next one).

## Current state
- `scripts/lint-goal.py:91-96` — the file-reading branch of `main()`:
  ```python
  if args.file:
      try:
          text = open(args.file, encoding="utf-8").read()
      except OSError as e:
          print(f"could not read {args.file}: {e}", file=sys.stderr)
          return 2
  ```
- `open(...).read()` leaks the handle (no `with`). The `except OSError` should stay — it handles the
  missing/unreadable file path and returns exit code 2.

## In scope (the only file you may modify)
- `scripts/lint-goal.py`

## Out of scope (do NOT touch)
- The stdin branch (`else: text = sys.stdin.read()`) — correct as is; do not wrap stdin in a `with`.
- The `lint()` logic, the regex tables, exit codes — unrelated.

## Verify-gates
| Purpose | Command | Expected on success |
|---------|---------|---------------------|
| Lint | `ruff check scripts/lint-goal.py` | `All checks passed!` |
| Behaves (clean goal) | `python scripts/lint-goal.py CLAUDE.md` | exits non-zero with findings, no traceback |
| Full suite | `python -m pytest -q` | all pass (no regression) |

## Steps
### Step 1: Use a context manager
Replace `text = open(args.file, encoding="utf-8").read()` with:
```python
with open(args.file, encoding="utf-8") as fh:
    text = fh.read()
```
Keep the surrounding `try/except OSError` exactly as is (still returns exit code 2 on a bad path).
**Verify**: `ruff check scripts/lint-goal.py` → clean; `python -m pytest -q` → all pass.

## Test plan
- No existing test targets `lint-goal.py` directly. A characterization test is optional for a one-line
  hygiene fix; if `/safe-change` GATE 2 wants coverage, add a tiny test: a missing path returns exit
  code 2, and a file with a weak phrase returns exit code 1 (model structure on `tests/test_tdd_guard.py`).

## Done criteria (ALL must hold)
- [ ] `open()` for the file path uses a `with` block; handle is closed
- [ ] `ruff check scripts/lint-goal.py` clean; `python -m pytest -q` all pass
- [ ] No file outside `scripts/lint-goal.py` modified (`git status`)

## STOP conditions (stop and report — do not improvise)
- `scripts/lint-goal.py:91-96` no longer matches the excerpt (drifted since `4487c42`).
- The fix would change the script's exit codes or output format — it must not; stop if it does.

## Maintenance notes
- Consider enabling ruff's `SIM115` (open-without-context-manager) in `ruff.toml` so the linter
  catches the next occurrence repo-wide — a natural follow-up, out of scope here.
