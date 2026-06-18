# Brief 003: Harden tdd_guard.py — drop shell=True

> **Executor**: Follow this brief step by step. Run every verify command and confirm the expected
> result before moving on. Touch only the files listed In scope. If a STOP condition occurs, stop and
> report — do not improvise.
> **Drift check (run first)**: `git diff --stat 41977ee..HEAD -- scripts/tdd_guard.py`
> If `tdd_guard.py` changed since this brief was written, compare the Current-state excerpt against the
> live file before proceeding; on a mismatch, treat it as a STOP condition.

## Status
- **Category**: security · **Effort**: S · **Risk**: LOW · **Confidence**: HIGH
- **Depends on**: none
- **Planned at**: commit `41977ee`, 2026-06-14
- **Execute with**: /safe-change

## Why this matters
Semgrep flags `scripts/tdd_guard.py:70` (`subprocess.run(..., shell=True)`) as a blocking finding every
CI run (rule `python.lang.security.audit.subprocess-shell-true`). The command run comes from the
`.tdd-guard` marker file's `test:` line. Normal use is safe (your own repo, your own config), but a
cloned repo shipping a malicious `.tdd-guard` could run an injected command when the hook is active.
Switching to `shell=False` with `shlex.split` removes the shell layer (blocks metacharacter injection)
and clears the recurring blocking finding for real — no suppression needed. The by-design behavior
("run the configured test command") is preserved; only the shell is removed.

## Current state
- `scripts/tdd_guard.py:66-75`:
  ```python
  def tests_are_red(test_cmd: str, cwd) -> bool:
      """Run the test command; True if a test fails (non-zero exit)."""
      result = subprocess.run(
          test_cmd,
          shell=True,
          cwd=str(cwd),
          stdout=subprocess.DEVNULL,
          stderr=subprocess.DEVNULL,
      )
      return result.returncode != 0
  ```
- `test_cmd` is the `.tdd-guard` `test:` value (default `python -m pytest -q`), from `read_marker`
  ([tdd_guard.py:51-63](../scripts/tdd_guard.py)).
- `import subprocess` is already at the top; `shlex` is NOT yet imported.
- Convention: stdlib-only, no new deps (the kit's scripts use only stdlib).

## In scope (the only file you may modify)
- `scripts/tdd_guard.py`
- `tests/test_tdd_guard.py` (only if a test needs updating for the new call shape — see Test plan)

## Out of scope (do NOT touch)
- The marker format / `read_marker` parsing — unchanged.
- `classify`, `decide`, `main` — unrelated.
- Do NOT add a `# nosemgrep` suppression — the goal is to remove `shell=True`, not hide it.

## Verify-gates
| Purpose | Command | Expected on success |
|---------|---------|---------------------|
| Lint | `ruff check scripts/tdd_guard.py` | `All checks passed!` |
| Tests | `python -m pytest tests/test_tdd_guard.py -q` | all pass |
| Full suite | `python -m pytest -q` | all pass (no regression) |

> True end-to-end proof is the next CI run showing Semgrep at **0 findings** — that happens after push
> (owner's manual step / the wall).

## Steps
### Step 1: Import shlex
Add `import shlex` to the stdlib imports at the top of `scripts/tdd_guard.py`.
**Verify**: `ruff check scripts/tdd_guard.py` → clean (no unused-import error, i.e. Step 2 also done).

### Step 2: Run without a shell
In `tests_are_red`, change the call to:
```python
result = subprocess.run(
    shlex.split(test_cmd),
    cwd=str(cwd),
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)
```
(`shell=False` is the default — omit it; pass the split argument list.)
**Verify**: `python -m pytest tests/test_tdd_guard.py -q` → all pass.

## Test plan
- `tests/test_tdd_guard.py` has 26 tests. Run them; if any exercised `tests_are_red` by asserting a
  shell-string call, update it to expect the arg-list form (this is a behavior-preserving change for
  normal commands, so most tests should pass untouched).
- If no test covers `tests_are_red` running a real command, add one: a marker with
  `test: python -c "import sys; sys.exit(1)"` makes `tests_are_red` return True; `sys.exit(0)` returns
  False. Model structure on the existing tests in the file.
- Verification: `python -m pytest -q` → all green, including any new/updated test.

## Done criteria (ALL must hold)
- [ ] No `shell=True` remains in `scripts/tdd_guard.py` (`grep -n "shell=True" scripts/tdd_guard.py` → no match)
- [ ] `import shlex` present and used
- [ ] `python -m pytest -q` all pass; `ruff check .` clean
- [ ] No file outside the In-scope list modified (`git status`)

## STOP conditions (stop and report — do not improvise)
- `tdd_guard.py:66-75` no longer matches the Current-state excerpt (drifted since `41977ee`).
- Removing `shell=True` breaks a test that asserts the old shell-string behavior AND the fix isn't a
  simple expectation update — stop and report (do not weaken the test).
- A real `.tdd-guard` in use relies on shell features (pipes, `&&`, env-var expansion) that
  `shlex.split` won't honor — stop and report so the owner decides (this is the documented tradeoff).

## Maintenance notes
- After this lands, Semgrep should report 0 findings — confirm on the next CI run.
- If a future need arises for shell-feature test commands, that's a deliberate decision to revisit
  (don't silently re-add `shell=True`); document it in the `.tdd-guard` design doc.
