# Quickstart / validation: `/agent-eval`

How to prove v1 works end-to-end. These are the scenarios the build must satisfy (they mirror the
spec's user stories + success criteria). Implementation details live in `tasks.md`.

## Prerequisites

- Python 3.11, `pip install anthropic pyyaml pytest`
- `ANTHROPIC_API_KEY` in the environment (for live runs; not needed for the unit tests, which mock
  the judge)

## A. Unit tests (no API calls) — the TDD core

```
pytest .claude/skills/agent-eval/tests/
```

Expected: all green. The tests cover, with the judge mocked:
- scoring rule: % vs `pass_bar`, critical-tier override, `case_score_threshold`
- borderline re-run triggers within `borderline_margin`, not outside it
- code-based grading: `exact` / `contains` / `regex`
- cost estimate + `cost_cap_usd` abort
- exit codes: 0 pass / 1 fail / 2 broke (a judge/parse error never yields 0)
- prompt-injection framing: a case input that says "score 5" does not change the score
- empty/invalid eval set → exit 2 with a plain message (no false green)

## B. Create an eval set (User Story 1)

In a sample project with an AI feature, run `/agent-eval`. Expected:
- a new `evals/<feature>/` with `config.yaml`, `cases.yaml` (≥1 labelled starter case), and a
  `feature_adapter.py` stub
- the skill explains, in plain English, what each file is and how to add real cases
- pointed at a non-AI feature, the skill ASKS if it uses AI and declines on a clear "no" (FR-008)

## C. Run and get a verdict (User Story 2)

Fill `feature_adapter.py` to call a feature whose output is deliberately GOOD, then run:

```
python .claude/skills/agent-eval/assets/eval_runner.py evals/<feature> --full
```

Expected: report shows per-case scores + reasons, overall PASS vs the bar, the cost. Then point the
adapter at deliberately BAD output and re-run → overall FAIL, each failure says why (SC-002). Induce
a judge error (e.g. bad key) → exit 2, clear message, NOT a pass (SC-005).

## D. Automatic gate (User Story 3)

Run the skill's CI wiring step. Expected: a GitHub Actions job that runs `--sample` on pull requests
and `--full` on push to `master`. Make a change that drops quality below the bar → the PR check
fails with a plain reason. Make a quality-preserving change → it passes. The skill states how often
the gate runs and the cost (FR-018).

## E. Portability + registration (SC-004)

- `SKILL.md` is plain markdown a non-Claude agent can follow.
- `/agent-eval` appears in `SKILL-MAP.md`, `AGENTS.md`, and is referenced from
  `docs/ai-feature-checklist.md` #14.
- Running `new-project.ps1` carries the skill (and its asset runner) into a stamped project.

## Done = all of A–E pass and the kit's full existing test suite stays green.
