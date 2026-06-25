# Tasks: `/start` (the Conductor)

**Feature**: `/start` | **Branch**: `009-conductor` | **Spec**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)

TDD: guard tests first (assert SKILL.md behaviors + hook fire-once), red → build → green.

## Phase 1: Setup
- [ ] T001 Create `.claude/skills/start/` + `references/` placeholders.

## Phase 2: Guard tests first (TDD)
- [ ] T002 Write FAILING `tests/test_conductor.py`: SKILL.md exists with `name: start` + description; states — proactive greeting + /start; greet with capabilities/limits + dynamic questions; DRIVES idea-to-app + guide (no duplicate pipeline); names the stage→resource map incl. discover, grill-me, research-scout, loop-design, stack suggestion, verify, security-review, git-safety; checkpoints + "just run it" bypass; NEVER push/merge/deploy; plain-English; references/stage-resource-map.md exists; registered in AGENTS.md, SKILL-MAP.md, README.md. PLUS hook test: `scripts/conductor_greeting.py` exists, is deterministic stdlib, fires once (writes marker), stays quiet after (mirror test_recommender_nudge.py).

## Phase 3: Build the skill (green) — US1/US2/US3
- [ ] T003 [US1] Write `.claude/skills/start/SKILL.md` — greet, capabilities/limits, dynamic intent elicitation, plain-English mentoring, "make sense?" checks; route to existing-code path (safe-change/health) vs new-build path.
- [ ] T004 [P] [US2] Write `references/stage-resource-map.md` — the stage → skill/resource table (discover → grill-me + research-scout(consent) → loop-design + light stack suggestion → build (speckit+Superpowers) → verify → security-review → git-safety; name extras: recommender, GitMCP, cookbook, agent-architect, agent-eval).
- [ ] T005 [US2] In SKILL.md: weave-in rules — at each stage name the resource + plain-English why; offer research-scout with consent; light stack suggestion (kit defaults + project type + one-line why; full decider = v3); say-so-and-continue if a resource is unavailable.
- [ ] T006 [US3] In SKILL.md: checkpoint at every stage + "just run it" bypass; the never push/merge/deploy wall in BOTH modes; drive idea-to-app's gates, don't reimplement.

## Phase 4: Proactive greeting (the hook)
- [ ] T007 Write `scripts/conductor_greeting.py` — SessionStart hook: inject a one-line offer ("New here? say start…"), once per project via a git-ignored marker (`.claude/.conductor-greeted`); deterministic stdlib; never blocks. Mirror `recommender_nudge.py`.
- [ ] T008 Wire the hook into `.claude/settings.json` SessionStart; add the marker to `.gitignore`; document a manual fallback in AGENTS.md (Principle VI, Claude-only mechanism).

## Phase 5: Register + verify
- [ ] T009 [P] Register in `AGENTS.md` (new "front door — `/start`" section + hook fallback note).
- [ ] T010 [P] Register in `SKILL-MAP.md` (top row — the front door) + `README.md` index (skill, script, spec, test rows).
- [ ] T011 Run guard tests + full suite green; inventory gate green; ruff clean.

## Dependencies
- T002 before T003–T010. T003 before T005/T006 (same file). T007 before T008. T009/T010 after skill+hook exist.

## Parallel
- T004 with T003 drafting; T009 + T010 (different files).

## MVP
US1 (greeting + guided elicitation) + the stage-resource map = the core "chef". US2/US3 complete v1.
