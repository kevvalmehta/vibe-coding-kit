# Routing & Modes

How `/audit` hands work to the kit's build skills, and how the two modes differ. The founding rule
survives unchanged: **the advisor never edits source code.** The executor skills edit code in their
own isolated worktrees, with their own TDD and regression gates.

---

## The executor map

Each brief names exactly one executor skill, chosen by what the finding is:

| Finding is… | Route to | Why |
|---|---|---|
| A fix/change to **existing** code (bug, perf, tech-debt, security fix, refactor) | **`/safe-change`** | Its gates (impact map → characterization tests → isolated worktree → full regression run → fresh-context review) are exactly the regression-safe path the constitution requires. |
| A **new feature** or a **direction/spike** | **`/speckit-specify`** | New capability belongs in the greenfield flow (spec → plan → tasks → build), not a patch. |
| A **batch** of related briefs to run as one guided sequence | **`/autopilot`** | It drives the planning sequence step-by-step for the owner. |

`/audit` writes the brief and names the route. It does **not** re-implement any of these — that would
duplicate them (scar L-1).

---

## The two modes

### Interactive (default)

After presenting findings and writing the briefs, **offer** to run the executor skill on a chosen
brief and then **STOP** for the owner's go — exactly like `/health` and `/guide` hand off. Never
auto-run. One brief at a time, owner-driven.

> "Brief 001 (the N+1 fix) is ready. Want me to run `/safe-change` on it now, or are you taking it
> from here?" — then wait.

### Autonomous (`auto`, opt-in)

The owner approves once (`/audit auto`) and the skill chains straight through:

1. Pick the **top findings by leverage** — default the **top 3–5**, owner-overridable.
2. Route each into its executor skill, running them **sequentially** — one isolated worktree at a time
   (parallel edits to one repo risk conflicts).
3. Between briefs, report progress in one plain-English line; carry on without stopping at every step.

The autonomous **outcome** is a green, reviewed, regression-tested branch ready for the owner to
approve and merge — **never a live deploy.**

---

## The wall (holds in BOTH modes)

Whether interactive or `auto`, the chain **STOPS before push, merge, and deploy.** Those are the
owner's manual decisions — hand them to the **`git-safety`** skill, which runs the git mechanics for a
non-technical owner and keeps `main` always-working. This is identical to the refusals already in
`/autopilot` and `/safe-change`. Even fully autonomous, `/audit` never pushes, merges, or deploys.

If `auto` hits an **ambiguity** or a **failing gate** mid-chain, **stop and surface it** (fail loud).
Never guess forward.

---

## Portability fallbacks

- **No parallel subagents** (a tool that can't spawn Explore agents): audit the categories
  **sequentially** in priority order and say so in the report. The findings are the same; only the
  wall-clock changes.
- **`auto` on a tool without worktree-capable execution**: write the briefs and hand them over for
  manual execution; say that autonomous chaining isn't available here.
- **Not a git repository**: worktree isolation (which `/safe-change` needs) can't run — deliver the
  briefs for manual execution and say so.

These keep `/audit` LLM-portable: any tool can follow this file by hand. The fixed routing and the
wall still apply.
