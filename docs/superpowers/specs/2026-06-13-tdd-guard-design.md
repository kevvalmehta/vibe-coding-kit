# TDD-Guard — Design

**Date:** 2026-06-13
**Status:** Approved (design); implementation pending
**Owner:** Aastha Mehta
**Branch:** `feat/tdd-guard`

## Why

Hard Rule #2 of the kit is "TDD always", but Superpowers only *encourages* test-first
work — nothing *blocks* an edit that adds implementation code with no failing test behind
it. TDD-Guard closes that gap with a deterministic guard. No LLM, no third-party code; it
is our own native rebuild of the idea behind the community "TDD Guard" tool (we did not
install or copy that tool — supply-chain rule).

## Scope decision

Active **only inside a build** (a real app/feature with a test suite), never for routine
editing of docs, skills, config, or markdown. The kit is mostly `.md` skills and docs; a
guard that fired on every edit would block normal work. Test-first only has meaning during
a build, so that is the only place it enforces.

## Components

### 1. Marker file — `.tdd-guard` (repo root, gitignored)

The single on/off + mode switch. Gitignored so the repo never commits in the "on" state.

- **Absent** → guard off (default). Normal editing untouched.
- **Present**, format:
  ```
  mode: strict        # strict | refactor
  test: python -m pytest -q    # optional; this is the default
  ```
- `strict` → enforce test-first (red-green).
- `refactor` → allow implementation edits while all tests are green (refactor step).

### 2. The hook

`PreToolUse` on `Edit | Write | MultiEdit`, configured in `.claude/settings.json`.
Command: `python scripts/tdd_guard.py`. Claude Code passes the tool call as JSON on stdin;
the script reads the target `file_path` from it.

### 3. File classification (pure, testable)

- **Test file** — `test_*.py`, `*_test.py`, `*.test.ts`, `*.spec.ts`, anything under a
  `tests/` directory → **always allow** (writing the failing test is TDD step 1).
- **Non-code** — `.md`, `.json`, `.txt`, config files → **always allow**.
- **Implementation code** — `.py`, `.ts`, `.js`, `.tsx`, `.jsx`, etc. → run the check.

### 4. The check (only when: marker present + `strict` + editing impl code)

1. Run the marker's `test` command (default `python -m pytest -q`).
2. Exit **non-zero** (a test is red) → **allow** — you are making the red test pass.
3. Exit **zero** (all green) → **block**:
   > "All tests green — write a failing test before adding/changing implementation.
   > (Refactoring? set `mode: refactor` in `.tdd-guard`.)"
4. `refactor` mode → **allow** impl edits regardless of red/green.

No recursion risk: the guard runs pytest, and pytest does not trigger Edit/Write hooks.

### 5. Block mechanism

The hook returns Claude Code's deny decision (so the edit is stopped and the reason is
surfaced to the agent). **Exact PreToolUse output protocol + stdin JSON shape are verified
against current Claude Code docs at build time — not assumed from memory.**

## Data flow

```
Edit/Write/MultiEdit attempted
  → PreToolUse hook fires → python scripts/tdd_guard.py (stdin: tool JSON)
  → read .tdd-guard            (absent? → allow, exit)
  → classify file_path         (test/non-code? → allow, exit)
  → impl code + strict mode    → run test cmd
        red   → allow
        green → block (reason surfaced)
  → impl code + refactor mode  → allow
```

## How we build it (TDD — eat our own dog food)

Core is one pure function:

```
decide(mode: str | None, file_path: str, tests_red: bool) -> "allow" | "block"
```

`tests_red` is injected (the test run happens in the wrapper), so the decision function is
pure and fast to test. pytest cases:

| marker / mode | file | tests | expected |
|---|---|---|---|
| absent | impl `.py` | — | allow |
| strict | test file | — | allow |
| strict | non-code `.md` | — | allow |
| strict | impl `.py` | green | **block** |
| strict | impl `.py` | red | allow |
| refactor | impl `.py` | green | allow |

The thin wrapper (stdin parse → classify → maybe run tests → emit decision) is added after
the pure function is green.

## Out of scope (YAGNI)

- JS/TS test runners beyond what the `test:` override allows (v1 assumes pytest default;
  any command can be set via the marker).
- Per-edit skip tokens.
- Running a test subset automatically.

## Portability (Hard Rule #6)

Not done until registered in `AGENTS.md` + `SKILL-MAP.md`.

## Open items to verify live at build time (do not guess)

1. Exact `PreToolUse` hook output protocol for blocking an edit (current Claude Code docs).
2. Exact stdin JSON shape for the tool call (where `file_path` lives).
