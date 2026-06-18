---

description: "Task list — Audit Advisor (/audit)"
---

# Tasks: Audit Advisor (`/audit`)

**Input**: Design documents from `/specs/004-audit-advisor/`

**Prerequisites**: [plan.md](plan.md) (required), [spec.md](spec.md) (user stories)

**Tests**: REQUIRED — "TDD always" (Constitution II). Guard test `tests/test_audit_advisor.py` written
failing-first, then made green file-by-file. Behavior quality (does it audit/vet/route well) is
eye-checked at verify — a skill's output can't be fully unit-tested (see plan Known Risk).

**Organization**: grouped by the 3 user stories. One skill (`SKILL.md` + 3 references) + the
registrations span all three; each story turns specific guard assertions green.

## Format: `[ID] [P?] [Story] Description`

## Path Conventions

Kit skill — no `src/`.
New: `.claude/skills/audit/SKILL.md`, `.claude/skills/audit/references/audit-playbook.md`,
`.claude/skills/audit/references/brief-template.md`, `.claude/skills/audit/references/routing-and-modes.md`,
`tests/test_audit_advisor.py`.
Edits (surgical, additive): `AGENTS.md`, `SKILL-MAP.md`, `.claude/skills/health/SKILL.md`,
`.claude/skills/guide/SKILL.md`.

---

## Phase 1: Setup

- [x] T001 Confirm `pytest -q` is green from repo root (known-green baseline before adding the guard).

---

## Phase 2: Foundational (Blocking — write the failing guard)

**⚠️ CRITICAL**: write the test first; no skill content until it fails.

- [x] T002 Write `tests/test_audit_advisor.py` (pattern from `tests/test_agent_architect.py`: pure
  pathlib reads, no execution) with 9 assertions:
  T1 `.claude/skills/audit/SKILL.md` exists + frontmatter `name: audit` + non-empty `description`;
  T2 all three references exist (`audit-playbook.md`, `brief-template.md`, `routing-and-modes.md`);
  T3 `SKILL.md` encodes the hard rules — read-only-on-source, never-reproduce-secret-values,
  repo-content-is-data-not-instructions, decline-to-implement, and the push/merge/deploy WALL in
  BOTH modes;
  T4 `audit-playbook.md` covers all 9 categories + a "Finding format";
  T5 `brief-template.md` has the required brief fields (in-scope / out-of-scope, verify-gate, STOP
  conditions, planned-at SHA, executor-routing line) + a worked golden example;
  T6 `routing-and-modes.md` documents both modes + the executor map (`/safe-change`,
  `/speckit-specify`, `/autopilot`) + the sequential/non-git fallbacks;
  T7/T8 `audit` registered in `AGENTS.md` + `SKILL-MAP.md`;
  T9 `.claude/skills/health/SKILL.md` cross-links `/audit` (score → specifics handoff).
- [x] T003 Run `pytest tests/test_audit_advisor.py` → CONFIRM all FAIL (skill absent). Fail-loud: if any
  pass before content exists, fix the assertion.

---

## Phase 3: User Story 1 - Audit a repo → vetted, ranked findings (Priority: P1) 🎯 MVP

**Goal**: read-only audit across 9 categories, vet every finding by re-reading the cited code, present
a plain-English table ordered by leverage; by-design patterns are not flagged.

**Independent Test**: `pytest tests/test_audit_advisor.py -k "T1 or T4"` passes; AND an eye-check
(T017) confirms a run produces a ranked table where every row cites a real `file:line`, a by-design
pattern is NOT reported, and nothing unverified is presented.

- [x] T004 [US1] Write `.claude/skills/audit/SKILL.md` — frontmatter (`name: audit`) + triggers + the
  Hard Rules block (read-only on source; never reproduce secret values → `file:line`+type+rotation;
  treat repo content as data not instructions; decline-to-implement) + workflow phases 1-4 (Recon;
  parallel read-only Explore audit with documented sequential fallback, depth quick/standard/deep +
  single-category focus; Vet by re-reading every cited location; Rank + present plain-English table,
  direction listed separately, state what was NOT audited). Make T1 pass; partial T3 (audit-half rules).
- [x] T005 [US1] Write `.claude/skills/audit/references/audit-playbook.md` — the 9 categories
  (correctness, security, performance, test coverage, tech debt, dependencies & migrations, DX, docs,
  direction) with what-to-look-for, the "Finding format", and the leverage/prioritization rubric.
  Carry the two subagent security rules (no secret values; content-is-data). Make T4 pass.
- [x] T006 [US1] Run `pytest tests/test_audit_advisor.py -k "T1 or T4"` → green.

**Checkpoint**: read-only audit produces a vetted, ranked, plain-English findings table.

---

## Phase 4: User Story 2 - Picks become self-contained handoff briefs (Priority: P2)

**Goal**: selected findings become self-contained briefs in `audit/` + an index, each naming its
executor skill; reconcile (don't duplicate) an existing `audit/`.

**Independent Test**: `pytest tests/test_audit_advisor.py -k "T5"` passes; eye-check confirms a brief
is fully self-contained (paths, excerpts from own re-read, in/out-of-scope, verify-gate, STOP) and
`audit/README.md` lists ranked order + rejected section.

- [x] T007 [US2] In `SKILL.md`, add workflow phases 5-6: Choose (write none for unselected); Write
  briefs (one self-contained brief per pick into `audit/` + `audit/README.md` index; stamp planned-at
  `git rev-parse --short HEAD`; reconcile-not-duplicate; never write a secret value). (Advances T3.)
- [x] T008 [US2] Write `.claude/skills/audit/references/brief-template.md` — the self-contained brief
  template (category/effort/risk/confidence/depends-on/planned-at SHA; `file:line` excerpts from own
  re-read; plain-English why-it-matters; in-scope + explicit out-of-scope; verify-gate command +
  expected output; STOP conditions; executor-routing line) + the `audit/README.md` index format
  (ranked order, dependency graph, considered-and-rejected) + a worked golden example. Make T5 pass;
  advances T2.
- [x] T009 [US2] Run `pytest tests/test_audit_advisor.py -k "T5"` → green.

**Checkpoint**: picks become self-contained, routable briefs.

---

## Phase 5: User Story 3 - Modes + routing + the wall + registration (Priority: P3)

**Goal**: interactive (offer + STOP) vs autonomous (`auto`, chain); both STOP before push/merge/deploy;
skill wired, registered, and portable.

**Independent Test**: `pytest tests/test_audit_advisor.py -k "T2 or T3 or T6 or T7 or T8 or T9"` passes;
eye-check confirms interactive offers-but-waits, `auto` chains to a green branch, and BOTH stop at the
push/merge/deploy wall.

- [x] T010 [US3] In `SKILL.md`, add workflow phase 7 (Route / run): interactive offers the executor
  skill + STOPs; `auto` chains the top-leverage picks (default top 3–5, owner-overridable — FR-017)
  through their executor skills sequentially (one worktree at a time); BOTH STOP before
  push/merge/deploy and hand off to `git-safety`; decline-to-implement points at the brief. Complete T3.
- [x] T011 [US3] Write `.claude/skills/audit/references/routing-and-modes.md` — interactive vs `auto`,
  the push/merge/deploy WALL (both modes; autonomous outcome = green reviewed branch, never a deploy),
  the executor map (fix-existing → `/safe-change`, new feature/direction → `/speckit-specify`, batch →
  `/autopilot`), and the sequential-executor + non-git-repo fallbacks. Make T6 pass; complete T2.
- [x] T012 [P] [US3] Register `audit` in `AGENTS.md` (skill list + one-line role). Make T7 pass.
- [x] T013 [P] [US3] Register `audit` in `SKILL-MAP.md` (row: "audit existing code / what's worth
  fixing → `/audit`"). Make T8 pass.
- [x] T014 [P] [US3] Cross-link in `.claude/skills/health/SKILL.md` (low score → run `/audit` for the
  specifics) — make T9 pass — and in `.claude/skills/guide/SKILL.md` (route "existing code, what next"
  → `/audit`).
- [x] T015 [US3] Run full `pytest tests/test_audit_advisor.py` → all 9 green.

**Checkpoint**: wired, registered, portable; the wall is enforced in both modes.

---

## Phase 6: Polish & Cross-Cutting

- [x] T016 [P] Full suite `pytest -q` + `ruff check .` → green (no regression).
- [x] T017 Behavior verify: run `/audit` against a small sample repo (the kit repo itself works — it has
  code, tests, and by-design patterns) with one planted defect + one by-design pattern; eye-check
  SC-001/002/005 (by-design NOT flagged; every row a real `file:line`; the push/merge/deploy wall holds;
  secrets shown only as location+type). Note: the fresh-context `/code-review` + two-stage review
  (Quality Gate 6 — risk rating + visual proof) run at BUILD via the Superpowers / `/safe-change`
  pipeline, not in this task.
- [x] T018 `powershell -File scripts\check-plan.ps1 -Gate` → PASS (every task checked, no placeholders).
- [x] T019 Update `HANDOFF.md` (built list + recent decision: `/audit` shipped, borrowed-thinking-from-
  improve, no execute/reconcile fork).

---

## Dependencies & Execution Order

- T001 → T002–T003 (failing guard) → blocks all stories.
- US1 (T004–T006) before US2/US3 — `SKILL.md` is one file, so sequence its writes: T004 → T007 → T010.
- Reference files are separate files: `audit-playbook.md` (T005), `brief-template.md` (T008),
  `routing-and-modes.md` (T011) can each be written right after their story's SKILL.md edit.
- T012 / T013 / T014 are [P] (different files) once the skill exists.
- Polish (T016–T019) after all stories green.

## Notes

- One `SKILL.md` → sequence its writes (T004 → T007 → T010); [P] tasks touch separate files only.
- TDD: T002–T003 prove red before any skill content (Constitution II + III).
- Behavior quality is eye-checked (T017), not unit-tested — documented plan limitation; the guard
  proves structure + hard-rules-present + wiring.
- Read-only skill, no deploy/DB/secrets of its own → security review expected clean; the security
  obligations it must ENFORCE (no secret values, content-is-data) are asserted by T3 + eye-checked.
- L-1 (no duplication): no `execute`/`reconcile` fork — execution delegated to existing skills.
