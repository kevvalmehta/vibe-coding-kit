# WARGAME.md skeleton

Copy this structure when writing `WARGAME.md` next to the plan it war-games. Replace every
`<angle-bracket>` note with real content; leave `{CurlyBrace}` placeholders IN the file until the
owner fills them — they are the greppable unknowns ledger.

```markdown
# WARGAME — <feature name>

- **Plan war-gamed:** <path, e.g. specs/031-my-feature/plan.md> (as of commit <short-sha>)
- **Executor: {ExecutorModel}** — follows this file step by step; takes forks as written; stops
  at any abort condition; does not re-plan, re-order, or skip steps.
- **Status:** DRAFT → BINDING once the owner says "yes, fight it this way" (date it here).

## 1. Step-by-step battle table

### Step 1 — <plan step name>
- **Expected observation:** <what you SEE when it succeeds — checkable, never "it works">
- **Failure scenario:** <the most realistic way it goes wrong, as something you'd observe>
- **Most likely cause:** <the single most probable reason, plain English>
- **Countermove:** <the pre-decided first response, in order; route to systematic-debugging /
  safe-change / git-safety where they apply>

### Step 2 — <…repeat for every plan step; a trivial step may honestly say
"low risk — if it fails, stop and re-read the plan">

## 2. Decision forks

- **FORK F1 (at step <n>):** if you observe <X> → take **route A**: <what to do>.
  If you observe <Y> → take **route B**: <what to do>.
- **FORK F2 (at step <n>):** <…numbered so the build log can say "took F2 route A">

## 3. Abort conditions — stop the build, bring this file back to the owner

- The same step failed twice, with different countermoves tried.
- A step would change something the plan says not to touch.
- Anything destructive (drop/reset/bulk delete) — destructive_action_gate territory.
- A secret would have to live anywhere other than `.env`.
- <feature-specific aborts>

## 4. Assumptions ledger

### Assumed inputs (taken as TRUE — if one breaks, this row is where to look)
- <assumption, one line each — the stack, an existing file, an API that exists…>

### Recon needed (unknowns the OWNER fills — or consciously defers, in writing — before build)
- `{PlaceholderName}` — <why it matters; where the owner finds the answer>
- `{AnotherUnknown}` — <…every recon item is a {CurlyBrace} placeholder, greppable with `{`>

## Owner approval

- [ ] Forks reviewed — the owner picked/blessed the routes
- [ ] Abort conditions reviewed
- [ ] Every `{Placeholder}` filled or consciously deferred (deferrals listed here)
- [ ] "Yes, fight it this way" — <owner, date> → status flips to BINDING
```
