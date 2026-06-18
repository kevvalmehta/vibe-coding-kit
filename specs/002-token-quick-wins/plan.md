# Implementation Plan: Token Quick-Wins

**Branch**: `002-token-quick-wins` | **Date**: 2026-06-10 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/002-token-quick-wins/spec.md`

## Summary

Adopt six token-saving wins as one plain-English habits doc (`docs/token-quick-wins.md`), register
it in the kit's portability files, and protect the whole thing with one small guard test so it can
never silently rot. Chosen approach = the "robust/testable" candidate (docs + a `pytest` guard),
because the kit's **TDD-always** Hard Rule means "done" must be machine-verifiable, and the kit
already has the small-script/doc + guard-test pattern (`scripts/autopilot_state.py` +
`tests/test_autopilot_state.py`). Grafted from the rejected simpler candidate: explicit
**already-in-place vs new** labels on each win so the owner knows when they must act.

## Technical Context

**Language/Version**: Python 3.x (test only — matches existing `tests/`)
**Primary Dependencies**: pytest, pathlib (already in repo). No new deps.
**Storage**: N/A (markdown docs + one test file)
**Testing**: pytest — one new guard module `tests/test_token_quick_wins.py`
**Target Platform**: the kit repo itself (developer tooling), not a deployed app
**Project Type**: kit/tooling change — docs + guard test
**Performance Goals**: N/A
**Constraints**: Surgical — touch only the doc + 4 small registration edits + 1 test file; change NO
skill behavior, NO planning-workflow files' logic.
**Scale/Scope**: 1 new doc, 1 new test, ~4 one-line edits to existing files.

## Constitution Check

*GATE: Must pass before Phase 0. Re-check after design.*

- **Plan before code** ✓ — this plan precedes any edit.
- **TDD always** ✓ — guard test is written failing-first, then made green file-by-file; full suite
  must stay green (SC-004). This is the whole reason candidate B won.
- **Never break working code** ✓ — no edits to skill logic or workflow scripts; only prose additions
  to MD files + a new isolated test. Existing CI (ruff + Biome + pytest) is the regression net.
- **Security first** ✓ — no inputs, secrets, network, or DB. N/A but no violations.
- **Simple + surgical** ✓ — minimum files; declined to add settings.json hooks for already-installed
  features (would be over-engineering — FR-007).
- **LLM portability** ✓ — doc registered in `AGENTS.md` + `SKILL-MAP.md` + `HANDOFF.md`; each
  Claude-only win carries a non-Claude fallback (FR-002, asserted by test T2).

No violations → Complexity Tracking left empty.

## Project Structure

### Documentation (this feature)

```text
specs/002-token-quick-wins/
├── spec.md              # done
├── plan.md              # this file
├── checklists/
│   └── requirements.md  # done (all ✓)
└── tasks.md             # next step (/speckit-tasks)
```

### Source Code (repository root)

```text
docs/
└── token-quick-wins.md          # NEW — the six wins (what/when/you-do/fallback + already|new label)

tests/
└── test_token_quick_wins.py     # NEW — 7 filesystem-string guard assertions

# EDITED (one line/sentence each — surgical):
AGENTS.md                        # register the doc (portability)
SKILL-MAP.md                     # register the doc (one habits-table row)
HANDOFF.md                       # "what's built" pointer
docs/ai-feature-checklist.md     # cross-ref Win 6 (prompt caching) at the caching factor
```

**Structure Decision**: Doc lives under `docs/` (matches `docs/ai-feature-checklist.md`,
`docs/superpowers/`); guard test lives under `tests/` next to `test_autopilot_state.py` (same
pattern, same runner). No `src/` — this feature ships no application code.

### The six wins (doc content outline)

Each entry = **What / When / You do / Status (already-in-place | new) / Non-Claude fallback**:

1. **Model routing → Haiku** — mechanical sub-work (classify/summarize/format) to cheap tier;
   judgment stays default. *Status: already-in-place (Autopilot does this).* Fallback: pick the
   cheap model manually for grunt sub-tasks.
2. **/compact** — compact context at natural breakpoints. *Status: Claude command (existing).*
   Fallback: paste a 3-sentence summary into a fresh thread.
3. **/recap** — orient on resume. *Status: Claude command (existing).* Fallback: paste HANDOFF
   opening into the new thread.
4. **Scope-bound prompts** — name only the files/scope needed; copy-paste template block. *Status:
   new habit.* Fallback: none needed (plain text, tool-agnostic).
5. **Caveman mode** — compress output. *Status: already-installed* (`/caveman` toggle). Fallback:
   "answer in bullets only."
6. **Prompt caching on system prompts** — default for AI features built with the kit. *Status: new
   default; cross-ref `docs/ai-feature-checklist.md`.* Fallback: documented as API guidance, not
   tool-specific.

### Guard test assertions (TDD targets)

- **T1** all six wins present (+ at least one carries an "already-in-place" label — the graft)
- **T2** each Claude-only win (compact, recap, caveman) has a fallback marker
- **T3/T4/T5** doc referenced in `AGENTS.md` / `SKILL-MAP.md` / `HANDOFF.md`
- **T6** `docs/ai-feature-checklist.md` cross-refs the prompt-caching win
- **T7** negative-space: habits doc embeds no planning-workflow *change* instructions
  (worded as links, not imperatives — see risk below)

## Background Work

None. (No scheduled/event-driven work — pure docs + a test.)

## Complexity Tracking

No constitution violations — table intentionally empty.

## Known risk (carried from the judge, plain English)

T7 is brittle: if the doc later says something like "before `/speckit-plan`, compact first," the test
could read that as a workflow-change instruction and fail. Mitigation: word the doc to **link** to
the workflow rather than embed instructions inside it. Flagged here so whoever writes the doc knows
the constraint up front.
