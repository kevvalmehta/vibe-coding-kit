# Contract — Autopilot Skill

The interface Autopilot exposes. This is a Claude Code skill (no HTTP/API surface).

## Invocation

| | |
|---|---|
| **Trigger** | Owner runs `/autopilot` or says "run autopilot", "drive the planning", "press go on this idea". Also reachable via `/guide`. |
| **Input** | Optional: a feature idea (plain English). If omitted, Autopilot resumes the active feature from `.specify/feature.json` + HANDOFF. |
| **Preconditions** | A git branch exists (kit rule: never on main). If on `main`/`master`, Autopilot tells the owner to branch first (via git-safety) and stops. |

## Behavior contract (what callers can rely on)

1. **Fixed sequence**: runs steps only in order specify → clarify → plan → tasks →
   pre-PR checks, each via the existing kit skill (FR-001).
2. **Stop for approval (gate mode)**: after a step it prints a plain-English summary and WAITS for an
   explicit affirmative; ambiguous → one yes/no confirm (FR-002). The **default gate mode is
   `stop-at-every-step`**; `big-3` and `auto` are opt-in (v2) and change only WHEN it stops, never the
   hard rules (never advance on ambiguity, never skip, never push/merge/deploy, fail loud).
3. **Change, don't advance**: a change request revises the current step's artifact and
   stops again at the same step (FR-003).
4. **Resumable**: invoked with no idea, it reports the current step from artifacts and
   continues (FR-004). Determined by `scripts/autopilot_state.py`.
5. **Parallel PLAN**: produces 2-3 candidate architectures in parallel + a judge pick,
   showing winner + rejected options + reason (FR-005).
6. **Combined PRE-PR**: runs `/verify` + `/security-review` in parallel → one report;
   any failure stops the run (FR-006).
7. **Model routing**: mechanical sub-work → Haiku; judgment → default tier (FR-007).
8. **HANDOFF upkeep**: updates its owned HANDOFF.md section after each completed step (FR-008).
9. **Refusals (hard)**: never pushes, merges, or deploys; declines + redirects to manual
   git-safety flow (FR-009).
10. **Fail loud**: never claims a step complete if a sub-step was skipped or a subagent
    failed; surfaces what was dropped (FR-010).

## Helper contract — `scripts/autopilot_state.py`

Pure, deterministic, no side effects. The TDD target.

```
get_current_step(feature_dir: str | None, handoff_text: str | None = None) -> dict
  returns: {
    "feature_dir": str | None,
    "completed": list[str],     # step keys whose artifact exists
    "current": str,             # first incomplete step key, or "specify" if none/started
    "next": str | None,         # step after current, or None at the end
    "warnings": list[str],      # e.g. malformed handoff, missing prerequisite
  }

STEP_ORDER: list[str] = ["specify", "clarify", "plan", "tasks", "pre-pr-checks"]
```

- Given an empty/missing `feature_dir` → `current == "specify"`, `completed == []`.
- Given spec.md + plan.md present, tasks.md absent → `current == "tasks"`.
- `clarify` is treated complete when spec.md exists and has no open clarification markers.
- Missing prerequisite (artifact gap before an existing later one) → earliest gap is
  `current`, plus a warning. Never returns a step whose prerequisite is missing.

## Portability fallback (non-Claude tools)

The `SKILL.md` is plain markdown: any AI tool can follow the same step order and gates
manually. Where parallel subagents are unavailable, the tool runs the PLAN candidates and
the PRE-PR checks sequentially and says so. Registered in AGENTS.md + SKILL-MAP.md (FR-011).
