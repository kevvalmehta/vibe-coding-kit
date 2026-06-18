# Handoff Brief Template

Every brief is written for an executor with **zero context** — a kit skill (`/safe-change`,
`/speckit-specify`, `/autopilot`) or another AI tool that has not seen the audit session, the survey,
or the other briefs. Assume it follows explicit instructions well and fills gaps badly.

Three properties make a brief executable by a weaker executor:

1. **Self-contained** — everything needed is in the file: paths, code excerpts, conventions, commands.
2. **Verify-gates** — every step ends with a command and its expected result. The executor never has
   to *judge* whether it succeeded.
3. **Hard boundaries + escape hatches** — explicit out-of-scope list, and "STOP and report" conditions
   instead of letting a weaker model improvise when reality doesn't match the brief.

File naming: `audit/NNN-short-slug.md`, numbered in recommended execution order. Excerpts come from
**your own re-read** of the code, never from a subagent's report. Never write a secret value into a
brief — `file:line` + credential type + a rotation note only.

---

## Template

```markdown
# Brief NNN: <Imperative title — what will be true after this brief is done>

> **Executor**: Follow this brief step by step. Run every verify command and confirm the expected
> result before moving on. Touch only the files listed In scope. If a STOP condition occurs, stop and
> report — do not improvise. **Drift check (run first)**: `git diff --stat <planned-at SHA>..HEAD --
> <in-scope paths>`. If any in-scope file changed since this brief was written, compare the Current
> state excerpts against the live code before proceeding; on a mismatch, treat it as a STOP condition.

## Status
- **Category**: bug | security | perf | tests | tech-debt | migration | dx | docs | direction
- **Effort**: S | M | L     **Risk**: LOW | MED | HIGH     **Confidence**: HIGH | MED | LOW
- **Depends on**: audit/NNN-*.md (or "none")
- **Planned at**: commit `<short SHA>`, <YYYY-MM-DD>
- **Execute with**: /safe-change  (or /speckit-specify, or /autopilot)

## Why this matters
2–5 plain-English sentences: the problem, its concrete cost, and what improves when this lands.
Intent is what lets a correct judgment happen when a detail is slightly off.

## Current state
The facts the executor needs, inlined — never "as discussed":
- Relevant files, each with one line on its role.
- Short excerpts of the code as it exists today, with `file:line` markers, so the executor can confirm
  it's looking at the right thing.
- The repo conventions that apply here, with a pointer to one exemplar file to match.

## In scope (the only files you may modify)
- `path/to/file.ts`
- `path/to/file.test.ts` (create)

## Out of scope (do NOT touch, even though they look related)
- `path/to/legacy.ts` — deprecated; changing it wastes effort and risks pinned clients.
- The public response shape — clients depend on it.

## Verify-gates (exact commands from recon — not guessed)
| Purpose   | Command                 | Expected on success |
|-----------|-------------------------|---------------------|
| Tests     | `<repo test command>`   | all pass            |
| Typecheck | `<repo typecheck cmd>`  | exit 0, no errors   |
| Lint      | `<repo lint command>`   | exit 0              |

## Steps
### Step 1: <imperative title>
What to do, precisely — exact files/symbols.
**Verify**: `<command>` → <expected output>
### Step 2: ...
(Each step small enough to verify independently; order so the codebase is never broken between steps.)

## Test plan
- New tests to write, in which file, covering which cases (happy path, the specific bug, named edges).
- Which existing test to model the structure on.

## Done criteria (machine-checkable — ALL must hold)
- [ ] `<test command>` passes; new tests for <X> exist and pass
- [ ] `<typecheck command>` exits 0
- [ ] No files outside In scope are modified (`git status`)

## STOP conditions (stop and report — do not improvise)
- The code at the Current-state locations doesn't match the excerpts (the codebase drifted).
- A step's verify fails twice after a reasonable fix attempt.
- The fix appears to require touching an out-of-scope file.
- A key assumption ("<assumption>") turns out false.

## Maintenance notes
- What future changes will interact with this; what a reviewer should scrutinize.
```

---

## Index file: `audit/README.md`

Written once after all briefs, updated by executors:

```markdown
# Audit Briefs — <repo>, generated <date>

Execute in the order below unless dependencies say otherwise. Each executor: read the brief fully,
honor its STOP conditions, update your row when done.

## Execution order & status
| Brief | Title | Category | Effort | Depends on | Execute with | Status |
|-------|-------|----------|--------|------------|--------------|--------|
| 001   | ...   | perf     | S      | —          | /safe-change | TODO   |
| 002   | ...   | tests    | M      | 001        | /safe-change | TODO   |

Status: TODO | IN PROGRESS | DONE | BLOCKED (one-line reason) | REJECTED (one-line rationale)

## Dependency notes
- 002 requires 001 because <reason>.

## Considered and rejected (so nobody re-audits these)
- <finding>: not worth doing because <one line>.
```

---

## Worked golden example

A vetted finding → a complete brief. (Illustrative; the verify commands would come from the audited
repo's own recon.)

```markdown
# Brief 001: Batch the order-list query to remove the N+1

## Status
- **Category**: perf · **Effort**: S · **Risk**: LOW · **Confidence**: HIGH
- **Depends on**: none
- **Planned at**: commit `a1b2c3d`, 2026-06-13
- **Execute with**: /safe-change

## Why this matters
The order-list endpoint issues one query per line item, so a 50-item order fires 51 queries. The list
page is the most-hit route; this is the single biggest latency source there.

## Current state
- `src/orders/api.ts:142` — `for (const item of order.items) { await db.product(item.id) }` inside the
  list handler. Error handling follows the Result pattern — see `src/lib/result.ts`, used in
  `src/users/api.ts:40-60`. Match it.

## In scope
- `src/orders/api.ts`
- `src/orders/api.test.ts` (create)

## Out of scope
- `src/orders/legacy-api.ts` — deprecated v1 path.
- The JSON response shape — clients depend on it.

## Verify-gates
| Purpose | Command           | Expected      |
|---------|-------------------|---------------|
| Tests   | `pnpm test orders`| all pass      |
| Types   | `pnpm typecheck`  | exit 0        |

## Steps
### Step 1: Add a batched lookup
Replace the per-item loop with a single `db.productsByIds(order.items.map(i => i.id))`.
**Verify**: `pnpm test orders` → all pass.

## Test plan
- New test in `src/orders/api.test.ts`: a 3-item order issues exactly 2 queries (model after
  `src/users/api.test.ts`).

## Done criteria
- [ ] `pnpm test orders` passes; the 2-query test exists and passes
- [ ] `pnpm typecheck` exits 0
- [ ] No files outside In scope modified (`git status`)

## STOP conditions
- `src/orders/api.ts:142` no longer matches the excerpt (drifted).
- The response shape would have to change to batch — stop and report.
```
