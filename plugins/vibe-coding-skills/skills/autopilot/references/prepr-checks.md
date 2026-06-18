# PRE-PR step — combined verify + security report

Goal: one report covering BOTH checks, run at once, so the owner stops babysitting two separate steps.
This is the LAST Autopilot step; building/pushing/merging stay manual.

## Step 0 — Is there actually a build to check yet? (no-build-yet guard)

Autopilot stops before the build (Superpowers TDD is the owner's manual step), so this step can be
reached when ONLY planning artifacts exist — there is no code to verify. Before running anything,
check what actually changed:

```
git diff --name-only master...HEAD
```

- **If only planning files changed** (everything under `specs/`, plus `.specify/feature.json` / the
  HANDOFF marker) and there is no real code/app change → there is **no build yet**. Do NOT fake-run
  `/verify` on documentation. Say so plainly:
  > "No build to check yet — only planning artifacts changed. Pre-PR checks (`/verify` +
  > `/security-review`) run **after the build**. Hand off to the build (Superpowers TDD); re-run this
  > step against the built code."
  Then STOP — this completes Autopilot's planning role.
- **If real code/app files changed** → run the full recipe below.

This fixes the v1 ordering quirk (pre-PR checks were positioned before the build). The fix is the
guard above, NOT reordering the fixed step sequence (`STEP_ORDER` stays unchanged).

## Recipe

1. **Run both checks in parallel (default tier).** Spawn two subagents IN ONE message:
   - one runs the **`/verify`** skill (does the change actually work — behavior + visual proof),
   - one runs the **`/security-review`** skill (inputs validated, no secrets, no risky ops, RLS).
2. **Merge (cheap).** With the Haiku tier, combine the two into ONE plain-English report:
   - `verify`: pass/fail + one-line summary,
   - `security`: pass/fail + each finding (severity + where + fix),
   - `overall`: **fail if EITHER failed**, else pass.
3. **Present + decide:**
   - **overall = pass** → tell the owner both checks passed; hand back for the MANUAL build/PR decision
     (Autopilot does not open the PR — see Refusals in SKILL.md).
   - **overall = fail** → state the failure(s) plainly and **STOP**. Do NOT open or suggest
     auto-opening a PR. Offer to route the fix through the **safe-change** skill.

## Fail loud

If either subagent errors or a check is skipped, say so — never report "passed" for a check that did
not actually run (FR-010). A missing check is a fail, not a pass.

## Non-Claude fallback

If parallel subagents are unavailable, run `/verify` then `/security-review` sequentially and present
the same combined report. Say it ran sequentially.
