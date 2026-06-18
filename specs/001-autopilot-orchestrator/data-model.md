# Data Model — Autopilot Workflow Orchestrator

No database. These are in-memory / derived concepts the skill and its helper reason about.
State is DERIVED from existing artifacts — there is no new persistent store.

## Entity: Step

One stage in the fixed planning sequence.

| Field | Meaning | Example |
|-------|---------|---------|
| `key` | stable identifier | `plan` |
| `order` | position in the fixed sequence (0-based) | `2` |
| `skill` | the kit skill this step invokes | `/speckit-plan` |
| `artifact` | the file whose existence marks this step done | `specs/<id>/plan.md` |
| `parallel` | whether the step uses parallel subagents | `true` (plan, pre-pr) / `false` (others) |

**Fixed order (STEP_ORDER)**: `specify → clarify → plan → tasks → pre-pr-checks`.
`clarify` is skippable when the spec has no open clarification markers (mirrors the kit).

## Entity: Run state (derived)

The current position in a feature's run. NOT stored; computed by `autopilot_state.py`.

| Field | Meaning | Source |
|-------|---------|--------|
| `feature_dir` | the active feature directory | `.specify/feature.json` |
| `completed` | steps whose artifact exists | filesystem scan of `feature_dir` |
| `current` | first step not yet completed | first gap in STEP_ORDER |
| `next` | the step after `current` | STEP_ORDER lookup |

**Validation / rules**:
- If a prerequisite artifact is missing (e.g. asked to plan with no `spec.md`), `current`
  resolves to the missing earlier step — Autopilot refuses to skip (FR edge case).
- If `feature.json` is absent, state = "no active feature; start at specify".
- Malformed HANDOFF section → warn, treat as no resume hint, fall back to filesystem scan.

## Entity: Combined check report

The merged result presented at the PRE-PR step (transient, shown to owner; not persisted).

| Field | Meaning |
|-------|---------|
| `verify_result` | pass / fail + plain-English summary from `/verify` |
| `security_result` | pass / fail + findings from `/security-review` |
| `overall` | `fail` if either failed, else `pass` |
| `blocking` | true when `overall == fail` → Autopilot stops, no PR suggested |

## State transitions

```
(no feature.json) --start--> specify --go--> clarify* --go--> plan --go--> tasks --go--> pre-pr-checks --(stop; manual build/PR)
       ^                          |              |             |            |                 |
       |                          +--change------+--change-----+--change----+-----change------+  (revise current step, stay put)
       |
   ambiguous reply at any step --> one yes/no confirmation --> (go | stay)

*clarify auto-skips when spec has no open clarification markers.
```

Terminal: Autopilot ends at the combined pre-PR report. Build (Superpowers TDD), push, and
merge are out of scope and owner-driven.
