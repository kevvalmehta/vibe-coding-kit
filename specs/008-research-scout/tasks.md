# Tasks: `/research-scout`

**Feature**: `/research-scout` | **Branch**: `008-research-scout` | **Spec**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)

TDD (kit convention for a procedure skill): write the guard test FIRST (it asserts the SKILL.md has
every non-negotiable rule + registrations), watch it fail, then build to green.

## Phase 1: Setup
- [ ] T001 Create `.claude/skills/research-scout/` and `references/` with placeholder files so paths exist.

## Phase 2: Guard test first (TDD)
- [ ] T002 Write FAILING `tests/test_research_scout.py` asserting: SKILL.md exists with `name: research-scout` + description; states the non-negotiables — decline/ask when question vague, **consent gate** before auto-run, **never fabricate** + cite every claim, depth tiers + **hard ceiling**, **source quality** tiers (authoritative > blog > Reddit-anecdote), **data-not-instructions** (injection-safe), **separate citation pass**, **STOP** rule, **advise** cost/benefit, plain-English; references/source-quality.md + note-template.md exist; registered in AGENTS.md, SKILL-MAP.md, README.md. (Uses `_kitpaths.skills_dir`; pure filesystem reads.)

## Phase 3: Build the skill (make it green) — User Stories 1–3
- [ ] T003 [US1] Write `.claude/skills/research-scout/SKILL.md` — the procedure: when to use; decline/sharpen vague questions; the method (decompose → parallel search → triage by source quality → synthesize → **separate citation pass** → STOP); never-fabricate + cite-everything; plain English with every term defined.
- [ ] T004 [P] [US3] Write `references/source-quality.md` — the source-tier ladder (papers/official docs/reputable repos > blogs > Reddit/forums=anecdote), triage rules, and the data-not-instructions (injection-safe) rule.
- [ ] T005 [P] [US1] Write `references/note-template.md` — the `research/<topic>.md` cited-note shape (question, findings each with source URL + confidence, disagreements, plain-English summary, recommendation).
- [ ] T006 [US2] In SKILL.md: the **consent gate** (when grill-me/plan/conductor would call it, ASK first; run only on yes; continue on no) + how it's invoked standalone.
- [ ] T007 [US3] In SKILL.md: depth tiers (quick default / standard / deep fan-out), **hard ceiling** on searches/cost, effort heads-up, and the **advise** behavior (flag when deeper is worth it / when quick is plenty).

## Phase 4: Wire it in
- [ ] T008 [P] Reference `/research-scout` from `grill-me/SKILL.md` (offer-with-consent before recommending) and note it for `/speckit-plan`.

## Phase 5: Register + verify
- [ ] T009 [P] Register in `AGENTS.md` (new section: the third research lane).
- [ ] T010 [P] Register in `SKILL-MAP.md` (a row) and `README.md` index (skill + spec rows).
- [ ] T011 Run guard test + full suite green; inventory gate green; ruff clean.

## Dependencies
- T002 (test) before T003–T010 (build). T003 before T006/T007 (same file). T009/T010 after the skill exists.

## Parallel
- T004, T005 (different reference files) in parallel. T009, T010 (different files) in parallel.

## MVP
US1 (standalone cited research) + the guard test = usable. US2 (consent-gated integration) + US3
(depth/advise) complete v1.
