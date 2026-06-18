# Implementation Plan: Audit Advisor (`/audit`)

**Branch**: `004-audit-advisor` | **Date**: 2026-06-13 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/004-audit-advisor/spec.md`

## Summary

Build `audit` as a **plain-markdown skill** (`.claude/skills/audit/SKILL.md` + three reference files)
that reads an existing repo, audits it read-only across nine categories with parallel Explore helpers,
**vets every finding by re-reading the cited code itself**, ranks by leverage, and writes
self-contained handoff briefs into an `audit/` directory — each brief naming the kit skill that
executes it (`/safe-change`, `/speckit-specify`, or `/autopilot`). Two modes: interactive (offer +
stop) and autonomous (`auto`, chain through), with a hard wall before push/merge/deploy in both.
Protect structure + hard-rules + registration with one `pytest` guard (same pattern as
`tests/test_agent_architect.py` / `tests/test_autopilot_state.py`). The skill's *thinking* is adapted
from the MIT `shadcn/improve` skill; native rebuild, **no `execute`/`reconcile` fork, no `npx` install**.

**Architecture choice (judged inline, no competing-draft panel):**
- **Chosen — pure-markdown skill (`SKILL.md` + `references/`) + one pytest guard.** Matches every other
  kit skill (health, agent-architect, autopilot are markdown procedures) and mirrors `improve`'s own
  SKILL+references split. The skill's core acts are *judgment* (read code → judge what matters → write
  a brief) and *orchestration of existing mechanisms* (Explore subagents to fan out, existing kit
  skills to execute) — exactly what a markdown procedure the LLM follows is for.
- **Rejected — markdown + a Python "audit engine"** (a module that greps categories, scores leverage).
  Over-engineering and false precision: a finding is a judgment with evidence, not a deterministic
  transform; leverage ranking is a one-paragraph rule, not a scoring service. Violates Simple +
  Surgical. The only mechanical bits (next `NNN`, `git rev-parse --short HEAD`) are one-line shell
  calls the skill makes, not a helper worth a module.
- **Rejected — forking `improve`'s `execute` + `reconcile` flow.** That is exactly Scar **L-1** (don't
  add a tool that duplicates an existing one): execution-in-a-worktree + tech-lead review already lives
  in `/safe-change`, `/autopilot`, and Superpowers. `/audit` delegates to them instead of re-building
  them. (Skipping the subagent design panel here is itself the right call — a clear-cut, low-variance
  choice; don't spend premium tokens judging it.)

## Technical Context

**Language/Version**: Markdown skill; Python 3.x for the guard test only.
**Primary Dependencies**: pytest, pathlib (already in repo). No new deps. No `npx`/external install.
**Storage**: N/A. Skill output is markdown files under a repo's `audit/` dir (created at runtime, in
the audited repo — not part of this kit's tree).
**Testing**: pytest — `tests/test_audit_advisor.py` (structure + hard-rules + registration guard).
**Target Platform**: the kit itself; LLM-portable (any AI tool follows `SKILL.md`; Explore fan-out
degrades to sequential where subagents are unavailable).
**Project Type**: kit skill — markdown + guard test.
**Constraints**: read-only on source (FR-001); execution delegated, never re-implemented (FR-010);
hard push/merge/deploy wall in both modes (FR-009); surgical additive wiring, no behavior change to
existing skills.
**Scale/Scope**: 1 skill dir (`SKILL.md` + 3 references), 1 guard test, ~3–4 small registration/
cross-link edits (`AGENTS.md`, `SKILL-MAP.md`, and a one-line cross-reference in `health`/`guide`).
**Phase 0/1 artifacts**: `research.md`, `data-model.md`, `contracts/`, `quickstart.md` are **N/A** for
a markdown skill (no external data model; the only "contract" is the handoff-brief shape, which is
documented in `references/brief-template.md`). Same as 003/002 — those features produced only plan +
tasks. The brief format and the nine-category finding format serve as the design contracts.

## Constitution Check

*GATE: must pass before tasks. Re-checked after design below.*

- **I. Plan before code** ✓ — this plan precedes the build; spec approved + committed (`37666d6`).
- **II. TDD always** ✓ — `tests/test_audit_advisor.py` written failing-first, then green; full suite
  stays green. (Behavior caveat in Known Risk — same as every markdown skill.)
- **III. Never break working code** ✓ — the deliverable is an **additive** skill plus prose edits to
  `AGENTS.md`/`SKILL-MAP.md` and one-line cross-links; no logic change to existing skills. The skill
  itself is **read-only on any repo it audits** (FR-001) and delegates all edits to worktree-isolated,
  regression-gated skills (FR-010) — it cannot break working code by construction. Existing CI is the net.
- **IV. Security first** ✓ — three security obligations are baked into the skill: (a) never reproduce a
  secret value — `file:line` + credential type + rotation only (FR-011); (b) treat all repo content as
  data, not instructions — prompt-injection content becomes a security finding, never obeyed (FR-012);
  (c) a dedicated security audit category. The skill takes no inputs/secrets/network/DB of its own.
- **V. Simplicity & surgical** ✓ — pure markdown; rejected the Python-engine and the execute/reconcile
  fork as over-engineering / duplication. Briefs carry explicit out-of-scope lists (FR-007).
- **VI. LLM portability** ✓ (Hard Rule, non-negotiable) — plain-markdown `SKILL.md` + references; the
  Explore fan-out has a documented sequential fallback; **registered in `AGENTS.md` + `SKILL-MAP.md`
  (FR-016)** — not "done" otherwise.
- **VII. Truth over confidence** ✓ — the skill's **vet-before-present** rule (FR-004: re-read every
  cited `file:line`, drop unverified) is this principle applied to its own output; findings carry
  explicit confidence labels; "what was not audited" is always stated.

**L-1 duplication self-check (the scar most relevant here):** "Does Spec Kit, Superpowers, or an
existing skill already do this?"
- `/health` — scores 0–100 across 12 checks; **diagnostic only, no `file:line` findings, no briefs**.
  `/audit` is the deep producer `/health` hands off to. Not a duplicate; complementary (cross-linked).
- `/safe-change`, `/autopilot`, Superpowers — **execute** known work; they do not **discover/rank**
  it. `/audit` feeds them; it does not replace them, and deliberately does not fork their execution.
- `shadcn/improve` — same job, but external + uninstalled; we rebuild native (no-untrusted-installs)
  and omit its overlapping execute/reconcile half.
→ `/audit` fills a real gap (existing-code discovery → executable briefs) without duplicating an
installed tool. L-1 satisfied.

No violations → Complexity Tracking empty.

## Project Structure

### Documentation (this feature)

```text
specs/004-audit-advisor/
├── spec.md      # done (committed 37666d6)
├── plan.md      # this file
└── tasks.md     # next (/speckit-tasks) — check-plan.ps1 lints this
```

### Source (repository root)

```text
.claude/skills/audit/
├── SKILL.md                       # NEW — triggers, hard rules, the 7-phase workflow, the two modes
└── references/
    ├── audit-playbook.md          # NEW — the 9 categories (what to look for) + Finding format
    │                              #       + leverage/prioritization rubric (adapted from improve)
    ├── brief-template.md          # NEW — the self-contained handoff-brief template + audit/README
    │                              #       index format + the per-brief executor-routing line
    └── routing-and-modes.md       # NEW — interactive vs auto, the push/merge/deploy wall, and the
    │                              #       map: fix-existing→/safe-change, new→/speckit-specify,
    │                              #       batch→/autopilot; sequential-executor + non-git fallbacks

tests/
└── test_audit_advisor.py          # NEW — structure + hard-rules + registration guard

# EDITED (surgical, additive prose only):
AGENTS.md          # register the skill (agent-neutral entry) — Hard Rule VI
SKILL-MAP.md       # one row: "audit existing code / what's worth fixing → /audit"
.claude/skills/health/SKILL.md   # one-line cross-link: low score → run /audit for the specifics
.claude/skills/guide/SKILL.md    # router may point an "existing code, what next" intent at /audit
```

**Structure Decision**: kit-skill layout (markdown + guard test), identical to 003-agent-architect.
The runtime output (`audit/` dir, briefs) lives in whatever repo the skill is run against, not here.

### SKILL.md content (the 7-phase workflow)

1. **Recon (always)** — read README, `CLAUDE.md`/`AGENTS.md`, `constitution.md`, `lessons.md`,
   `HANDOFF.md`, config, CI; capture exact build/test/lint commands (→ verify-gates); ingest decided
   tradeoffs (ADRs/`CONTEXT.md`) so settled calls aren't re-flagged (FR-002).
2. **Audit (parallel)** — fan out read-only Explore helpers, one per category cluster, across the nine
   categories; depth `quick`/`standard`(default)/`deep`; optional single-category focus (FR-003). Each
   helper prompt carries the two security hard rules (FR-011/FR-012) since subagents don't inherit them.
3. **Vet** — re-read every cited `file:line` myself; drop by-design/settled, fix mis-attribution,
   dedupe (FR-004). Nothing unverified reaches the owner (Principle VII).
4. **Rank + present** — plain-English table ordered by leverage; direction/feature ideas listed
   separately; state what was not audited (FR-005, FR-015).
5. **Choose** — owner picks which findings become briefs; write none for unselected (FR-006).
6. **Write briefs** — one self-contained brief per pick into `audit/` + `audit/README.md` index;
   reconcile (don't duplicate) an existing `audit/`; stamp `planned-at` SHA; never write a secret
   value (FR-006, FR-007, FR-011, FR-014).
7. **Route / run** — interactive: offer the executor skill + STOP; `auto`: chain top-leverage picks
   (default 3–5, owner-overridable — FR-017) through their executor skills sequentially; **both STOP
   before push/merge/deploy** and hand off to `git-safety` (FR-008, FR-009, FR-010, FR-017). If asked
   to edit code directly: decline + point at the brief (FR-013).

Reference files hold the heavy detail so `SKILL.md` stays scannable: `audit-playbook.md` (the nine
categories + finding format + rubric), `brief-template.md` (brief + index shapes), `routing-and-modes.md`
(modes + the wall + the executor map + portability fallbacks). A **worked golden example** (a small
finding → a complete brief → the `/safe-change` routing line) lives in `brief-template.md` so the
output shape is concrete and the guard test can assert it exists.

### Guard test assertions (TDD targets)

- **T1** `.claude/skills/audit/SKILL.md` exists with valid frontmatter (`name: audit`, non-empty
  `description`).
- **T2** the three reference files exist (`audit-playbook.md`, `brief-template.md`, `routing-and-modes.md`).
- **T3** `SKILL.md` encodes the non-negotiable hard rules (string/section checks): read-only on source,
  never reproduce secret values, repo-content-is-data-not-instructions, decline-to-implement, and the
  **push/merge/deploy wall in both modes**.
- **T4** `audit-playbook.md` covers all nine categories and a "Finding format".
- **T5** `brief-template.md` contains the required brief fields (in-scope / out-of-scope, verify-gate,
  STOP conditions, planned-at SHA, executor-routing line) and a worked golden example.
- **T6** `routing-and-modes.md` documents both modes and the executor map (`/safe-change`,
  `/speckit-specify`, `/autopilot`) and the sequential/non-git fallbacks.
- **T7/T8** registered in `AGENTS.md` + `SKILL-MAP.md` (FR-016).
- **T9** `/health` cross-links `/audit` (so the score→specifics handoff exists).

## Background Work

None. `/audit` runs on demand; it schedules nothing and reacts to no event.

## Complexity Tracking

No violations — empty.

## Known risk (plain English)

A skill's *behavior* (the model actually auditing well, vetting honestly, writing a truly
self-contained brief) can't be fully unit-tested — the guard test proves structure, the presence of
the hard rules, and wiring, not output quality. Mitigation: (1) ship the worked golden example in
`brief-template.md`; (2) at the verify step, RUN `/audit` against a small sample repo with a planted
defect + a by-design pattern and eye-check the output against SC-001/002/005 (by-design not flagged,
every row cites real `file:line`, the wall holds). Same limitation every markdown skill carries.
