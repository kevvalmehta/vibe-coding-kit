# Phase 1 Data Model: `/agent-eval`

The "data" here is plain files in a project's `evals/<feature>/` folder, plus the in-memory result
the runner produces. All owner-facing files are YAML so a non-technical owner can read/edit them
(FR-020).

## Entity: Eval set

One folder per AI feature: `evals/<feature-name>/`. Contains `config.yaml`, `cases.yaml`,
`feature_adapter.py`.

## Entity: `config.yaml`

| Field | Type | Meaning | Default |
|---|---|---|---|
| `feature_name` | string | Human label for the feature being evaluated | — |
| `pass_bar` | number (0–100) | % of cases that must pass for the set to pass | `80` |
| `headroom_target` | number (0–100) | Quality to aim for so wobble stays above `pass_bar` | `85` |
| `case_score_threshold` | number | Per-case score (1–5) counted as "passing" | `4` |
| `borderline_margin` | number | If overall % is within this of `pass_bar`, re-run once | `5` |
| `sample_size` | integer | How many non-critical cases the `--sample` gate runs | `10` |
| `cost_cap_usd` | number | Abort the run if the estimate exceeds this | `1.00` |
| `judge_model` | string | Model id for the judge | Haiku tier id |
| `rubric` | string (multiline) | Shared grading guide for model-based cases | — |

## Entity: `cases.yaml`

A list of cases. Each:

| Field | Type | Meaning | Required |
|---|---|---|---|
| `id` | string | Unique id (used in reports + `--only`) | yes |
| `input` | string (multiline) | What gets sent to the feature adapter | yes |
| `grading` | enum: `code` \| `model` | Code-based check, or LLM-as-judge | yes |
| `expected` | string | For `code` grading: the exact/contains/regex target | if `grading: code` |
| `match` | enum: `exact` \| `contains` \| `regex` | How `expected` is compared | if `grading: code` (default `contains`) |
| `rubric` | string | Optional per-case override of the shared rubric | no |
| `critical` | bool | If true, MUST pass or the whole set fails | no (default `false`) |
| `starter` | bool | True = auto-generated training-wheels case | no (default `false`) |
| `notes` | string | Free notes for the owner | no |

**Validation rules** (runner refuses to run, with a plain message, if violated):
- every `id` unique and non-empty
- `grading: code` requires `expected`
- `pass_bar`, `headroom_target` in 0–100; `case_score_threshold` in 1–5
- at least one case present (else: explain the set is empty and stop — no false green)
- `starter: true` cases trigger a warning that the set isn't trustworthy until real cases are added

## Entity: `feature_adapter.py`

A project-provided file with one function:

```python
def run_feature(input_text: str) -> str:
    """Call the project's real AI feature with input_text, return its text output."""
    ...
```

Scaffolded as a stub with a clear `TODO`; the owner or an AI fills it to call their actual feature.

## Entity: Eval report (runner output, in memory → printed)

| Field | Meaning |
|---|---|
| `per_case` | list of {id, grading, score (model) or pass/fail (code), passed, reason} |
| `pct_passed` | % of run cases that passed |
| `critical_failures` | list of critical case ids that failed (empty = good) |
| `overall_passed` | bool — `pct_passed ≥ pass_bar` AND no critical failures |
| `reran` | bool — whether a borderline re-run happened |
| `cost_estimate_usd` / `cost_actual_usd` | shown before and after |
| `errors` | any judge/model/parse errors (non-empty ⇒ fail loud, never a silent pass) |

The printed report is plain English: each case (pass/fail + why), the overall verdict vs the bar,
any critical failures called out, and the cost. Exit code: `0` pass, non-zero fail or error (so CI
can gate on it).

## Deferred fields (placeholders, Phase 2/3)

- `trajectory:` block per case (steps/tools expected) — commented placeholder, Phase 3.
- live-monitoring config (sample rate, alert threshold, storage) — Phase 2, not in v1 files.
