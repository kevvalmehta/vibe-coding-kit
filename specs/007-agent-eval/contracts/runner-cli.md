# Contract: eval runner CLI

`python .claude/skills/agent-eval/assets/eval_runner.py <eval_set_dir> [options]`

## Arguments

| Arg / option | Meaning |
|---|---|
| `<eval_set_dir>` | Path to an eval set folder (e.g. `evals/support-reply`). Required. |
| `--sample` | Run a representative sample (`sample_size`) PLUS all critical cases. Default for the CI gate. |
| `--full` | Run every case. On demand + before merge. |
| `--only <id[,id...]>` | Run just the named case(s). For quick iteration. |
| `--ci` | Machine-friendly: terse output, strict exit code, no prompts. |
| `--estimate-only` | Print the cost estimate and exit without calling any model. |

If neither `--sample` nor `--full` is given in interactive use, the runner asks which (plain
English). In `--ci` mode it defaults to `--sample`.

## Behavior

1. Load + validate `config.yaml` and `cases.yaml` (refuse with a plain message on invalid; see
   data-model validation rules). Empty set ⇒ explain + non-zero exit (no false green).
2. Select cases (`--sample` / `--full` / `--only`); always include critical cases in `--sample`.
3. Print a **cost estimate**; if it exceeds `cost_cap_usd`, abort with a plain message.
4. For each case: call `run_feature(input)` via the adapter, then grade —
   - `grading: code` → deterministic match (`exact`/`contains`/`regex`); no model call.
   - `grading: model` → LLM-as-judge (see judge-io contract).
5. Apply scoring rule (data-model): % vs `pass_bar` AND no critical failures. If overall % is within
   `borderline_margin` of `pass_bar`, re-run borderline/failing cases once, then decide.
6. Print the plain-English report + actual cost.

## Exit codes

| Code | Meaning |
|---|---|
| `0` | Set passed (≥ bar AND no critical failure). |
| `1` | Set failed (below bar, or a critical case failed). |
| `2` | Could not run (invalid files, empty set, cost cap exceeded, judge/model/parse error). **Never reported as a pass.** |

Exit `2` is distinct from `1` so CI can tell "the AI got worse" (1) from "the eval itself broke" (2)
— both block, but the message differs. Fail loud (Principle VII, FR-006).
