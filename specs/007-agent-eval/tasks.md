# Tasks: `/agent-eval` — make evals runnable

**Feature**: `/agent-eval` | **Branch**: `007-agent-eval` | **Spec**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)

TDD approach (constitution Principle II): the runner's deterministic core gets failing tests FIRST,
then implementation to green. The judge is mocked in tests — no live API calls.

Paths are relative to repo root. `[P]` = parallelizable (different files, no incomplete deps).

---

## Phase 1: Setup

- [ ] T001 Create skill directory tree: `.claude/skills/agent-eval/{assets/eval_set_template,assets/ci,references,tests}/` with empty placeholder files so paths exist.
- [ ] T002 [P] Add `anthropic`, `pyyaml`, `pytest` to the kit's Python deps (requirements file / note) so the runner + tests resolve.

## Phase 2: Foundational — the tested runner core (BLOCKS US2 + US3)

This is the heart. Write tests first (T003), then implement (T005–T011) until green.

- [ ] T003 Write FAILING tests in `.claude/skills/agent-eval/tests/test_eval_runner.py` covering, with the judge MOCKED: config/cases loading + validation (unique ids, required fields, ranges), empty/invalid set → exit 2, code-based grading (`exact`/`contains`/`regex`), scoring rule (% vs `pass_bar` + `case_score_threshold`), critical-tier override, borderline re-run fires only within `borderline_margin`, cost estimate + `cost_cap_usd` abort, exit codes 0/1/2 (a judge/parse error never returns 0), and prompt-injection framing (rubric authority stays in the system prompt).
- [ ] T004 [P] Write `.claude/skills/agent-eval/references/judge-prompt.md` — the hardened judge system prompt (rubric + 1–5 scale + reason-then-`<score>` structured output + "case content is data, not instructions" framing). Needed by T007.
- [ ] T005 Implement config/cases loading + validation in `.claude/skills/agent-eval/assets/eval_runner.py` (data-model rules; plain-English errors; empty set → exit 2).
- [ ] T006 Implement code-based grading (`exact`/`contains`/`regex`) in `eval_runner.py`.
- [ ] T007 Implement the LLM-as-judge path in `eval_runner.py`: Haiku tier, `temperature 0`, prompt caching on the system prompt loaded from `judge-prompt.md`, parse `<score>`/`<reason>`, injection-safe framing; unparseable score → error (not a pass).
- [ ] T008 Implement the scoring rule in `eval_runner.py`: % at/above `case_score_threshold` vs `pass_bar`, AND every `critical` case must pass.
- [ ] T009 Implement borderline re-run in `eval_runner.py`: if overall % within `borderline_margin` of `pass_bar`, re-run borderline/failing cases once, then decide.
- [ ] T010 Implement cost estimate + `cost_cap_usd` abort + fail-loud error handling in `eval_runner.py` (any judge/model error ⇒ exit 2, never a silent pass).
- [ ] T011 Implement the CLI in `eval_runner.py`: `<eval_set_dir>`, `--sample`/`--full`/`--only`/`--ci`/`--estimate-only`, plain-English report, exit codes 0/1/2 per the runner-cli contract. Run full pytest → all green; refactor.

## Phase 3: User Story 1 — Create an eval set (P1)

**Goal**: owner runs `/agent-eval`, gets a ready-to-fill eval set + plain-English explanation.
**Independent test**: run against a sample AI feature → `evals/<feature>/` with config + ≥1 labelled starter case + adapter stub appears, explained in plain English; declines on a non-AI feature after asking.

- [ ] T012 [P] [US1] Write `.claude/skills/agent-eval/assets/eval_set_template/config.yaml` with documented defaults (pass_bar 80, headroom 85, threshold 4, borderline 5, sample_size 10, cost_cap 1.00, Haiku judge model, shared rubric).
- [ ] T013 [P] [US1] Write `.claude/skills/agent-eval/assets/eval_set_template/cases.yaml` — a few clearly-labelled `starter: true` cases (mix of `code` and `model` grading), with a comment that they're training wheels until real cases are added.
- [ ] T014 [P] [US1] Write `.claude/skills/agent-eval/assets/eval_set_template/feature_adapter.py` stub (`run_feature` raising `NotImplementedError`, per the adapter contract).
- [ ] T015 [US1] Write `.claude/skills/agent-eval/SKILL.md` — Part 1: declines for non-AI apps, ASKS when unsure (FR-008); scaffolds `evals/<feature>/` from the template; explains each file + every term in plain English; auto-fills labelled starter cases from the feature description + rubric; volume guidance ("more decent cases beats a few perfect ones").

## Phase 4: User Story 2 — Run and get a pass/fail (P1)

**Goal**: run the eval, get a plain-English verdict vs the bar; fails loud on error.
**Independent test**: good output → PASS report; bad output → FAIL with reasons; induced judge error → exit 2, not a pass. (Runner logic already built + tested in Phase 2; this adds the owner-facing procedure.)

- [ ] T016 [US2] Add to `SKILL.md` — Part 2: how to fill the adapter, run the runner (`--full` vs `--sample`), read the plain-English report, and the cost cap. State the skill always offers a full run and recommends one when the AI's prompt/instructions changed (FR-018).

## Phase 5: User Story 3 — Automatic CI gate (P2)

**Goal**: the eval runs by itself on every change and blocks drops below the bar.
**Independent test**: a quality-dropping change fails the PR check with a plain reason; a safe change passes.

- [ ] T017 [P] [US3] Write `.claude/skills/agent-eval/assets/ci/agent-eval.yml` — GitHub Actions: `--sample` on pull requests, `--full` on push to `master`, `ANTHROPIC_API_KEY` from secret, fails the job on non-zero exit.
- [ ] T018 [US3] Add to `SKILL.md` — Part 3: how to wire the CI gate into the project, stating how often it runs and the token cost (no surprise spend).

## Phase 6: Polish & cross-cutting (registration + green suite)

- [ ] T019 [P] Register the skill in `AGENTS.md` (new "/agent-eval" section + add it under the AI-inside guidance) — Principle VI.
- [ ] T020 [P] Add an `/agent-eval` row to `SKILL-MAP.md`.
- [ ] T021 [P] Update `docs/ai-feature-checklist.md` #14: change the "planned `/agent-eval`" note to "run `/agent-eval`" now that it exists.
- [ ] T022 Confirm the kit's CI (ruff + pytest) discovers `.claude/skills/agent-eval/tests/`; adjust config/path if needed.
- [ ] T023 Run the full kit test suite (must stay green) + quickstart scenario A (unit tests) → all pass; ruff clean.
- [ ] T024 Update `HANDOFF.md` with the new skill + its v1 scope + the named later phases.

---

## Dependencies & order

- Phase 1 → Phase 2 (foundational runner) → then US1/US2/US3.
- T003 (tests) before T005–T011 (implementation). T004 (judge prompt) before T007.
- US1 (T012–T015) is independent of US2/US3 and is the MVP slice.
- US2 (T016) and US3 (T017–T018) depend on the Phase-2 runner.
- Polish (T019–T024) last.

## Parallel opportunities

- T012, T013, T014 (template files) in parallel.
- T019, T020, T021 (registration in three different files) in parallel.

## MVP scope

US1 + the Phase-2 runner + US2 = a usable eval tool (create + run + verdict). US3 (auto-gate) is the
high-value fast-follow. After-launch monitoring (#15) and fuller trajectory evals are later phases.
