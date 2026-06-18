# Brief 001: Make CI actually run the Python test suite

> **Executor**: Follow this brief step by step. Run every verify command and confirm the expected
> result before moving on. Touch only the files listed In scope. If a STOP condition occurs, stop and
> report — do not improvise.
> **Drift check (run first)**: `git diff --stat 4487c42..HEAD -- .github/workflows/ci.yml`
> If `ci.yml` changed since this brief was written, compare the Current-state excerpt against the live
> file before proceeding; on a mismatch, treat it as a STOP condition.

## Status
- **Category**: tests (CI gate) · **Effort**: S · **Risk**: LOW · **Confidence**: HIGH
- **Depends on**: none
- **Planned at**: commit `4487c42`, 2026-06-13
- **Execute with**: /safe-change

## Why this matters
This repo has 7 pytest files / 70 tests — the guard tests that protect every kit skill (audit,
agent-architect, health, autopilot, tdd-guard, token-quick-wins). But the CI `test` job only runs the
Python step when a `requirements.txt` or `pyproject.toml` exists, and **neither exists in this repo**.
So the safety net never runs on push or PR: a change that breaks a guard test passes CI green. This
defeats Constitution II (TDD) and Quality Gate 3 (full suite stays green) at the CI level — the place
it matters most. Fixing it is a few lines.

## Current state
- `.github/workflows/ci.yml:96-109` — the Python half of the `test` job:
  ```yaml
  - name: Setup Python
    if: ${{ hashFiles('**/requirements.txt', '**/pyproject.toml') != '' }}
    uses: actions/setup-python@v5
    with:
      python-version: '3.12'
  - name: Python install & test
    if: ${{ hashFiles('**/requirements.txt', '**/pyproject.toml') != '' }}
    run: |
      python -m pip install --upgrade pip
      if (Test-Path requirements.txt) { pip install -r requirements.txt }
      pip install pytest
      pytest || echo "No tests yet — add them as you build (TDD)."
    shell: bash
  ```
- Two defects here:
  1. **Dead gate**: `hashFiles('**/requirements.txt','**/pyproject.toml')` is empty in this repo →
     both steps are skipped → tests never run.
  2. **Shell mismatch (latent)**: line 106 uses PowerShell `if (Test-Path requirements.txt) { … }`
     inside a `shell: bash` block. Under bash this is wrong syntax and would misbehave the moment a
     project actually adds `requirements.txt`.
- Convention to match: the sibling `lint` job (`ci.yml:34-51`) already gates on
  `hashFiles('**/*.py') != ''` — copy that pattern so the test job fires whenever Python files exist.

## In scope (the only file you may modify)
- `.github/workflows/ci.yml`

## Out of scope (do NOT touch)
- The `security`, `lint`, `lint-js` jobs — they work; don't refactor them.
- The Node half of the `test` job — unrelated.
- Do NOT add a `pyproject.toml`/`requirements.txt` just to satisfy the old gate — fix the gate instead
  (this kit has no runtime deps; pytest is the only need).

## Verify-gates
| Purpose | Command | Expected on success |
|---------|---------|---------------------|
| Tests (the suite CI must run) | `python -m pytest -q` | all pass (currently 70) |
| Lint | `ruff check .` | `All checks passed!` |
| YAML parses | `python -c "import yaml,sys; yaml.safe_load(open('.github/workflows/ci.yml'))"` | exit 0, no error |

> Note: the TRUE proof is the next CI run actually executing pytest. That happens after push — which is
> the owner's manual step (the push/merge/deploy wall). This brief's local gates prove the workflow is
> well-formed and the suite is green; the owner confirms the live CI run after pushing.

## Steps
### Step 1: Gate the Python test steps on Python files existing
Change BOTH `if:` conditions on the "Setup Python" and "Python install & test" steps from
`hashFiles('**/requirements.txt', '**/pyproject.toml') != ''` to `hashFiles('**/*.py') != ''` (matches
the `lint` job's proven pattern, so the test job fires on any Python project including this one).
**Verify**: `python -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml'))"` → exit 0.

### Step 2: Fix the bash/PowerShell mismatch
Replace `if (Test-Path requirements.txt) { pip install -r requirements.txt }` with bash:
`[ -f requirements.txt ] && pip install -r requirements.txt`. Keep `pip install pytest` and the
`pytest || echo "…"` fallback so a deps-free repo (like this one) still runs the suite.
**Verify**: re-run the YAML parse → exit 0.

### Step 3: Prove the suite the gate now protects is green
**Verify**: `python -m pytest -q` → all pass; `ruff check .` → clean.

## Test plan
- This is a CI-config change; the "tests" are the existing suite that the workflow must run. No new
  unit test is needed. Confirming the suite passes locally (Step 3) is the regression check.
- Optional belt-and-suspenders: if a YAML-lint or `act` tool is available, dry-run the `test` job;
  skip if not installed (don't add tooling for this).

## Done criteria (ALL must hold)
- [ ] Both Python steps in the `test` job gate on `hashFiles('**/*.py') != ''`
- [ ] No PowerShell syntax remains in any `shell: bash` block (`Test-Path` gone)
- [ ] `python -m pytest -q` passes; `ruff check .` clean; the YAML parses
- [ ] No file outside `.github/workflows/ci.yml` modified (`git status`)

## STOP conditions (stop and report — do not improvise)
- `ci.yml` no longer matches the Current-state excerpt (drifted since `4487c42`).
- Changing the gate would make the `security`/`lint`/`lint-js` jobs behave differently — it shouldn't;
  if it does, stop.
- The full suite is NOT green locally before the change — then this is a different problem (a real test
  failure); stop and report rather than wiring CI to a red suite.

## Maintenance notes
- Whoever adds the kit's first real Python app with dependencies should add `requirements.txt`; the
  `[ -f requirements.txt ]` guard then installs them. The gate keying on `**/*.py` keeps working.
- A reviewer should confirm the next CI run on push shows the `Tests` job executing pytest (not skipped).
