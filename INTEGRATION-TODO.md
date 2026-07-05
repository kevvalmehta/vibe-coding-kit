# INTEGRATION-TODO — weaving `/quality-charter` into the existing kit

Status: **new skill landed standalone; weave-in deliberately deferred** (token
budget). Everything below is a small, bounded edit — do them in one later PR,
or piecemeal. Delete this file when all boxes are checked.

## What landed in this PR

- `plugins/vibe-coding-skills/skills/quality-charter/SKILL.md` — the skill
- `references/quality-architecture.md` — the 8 patterns + 3 cross-cutting laws, with provenance
- `references/charter-template.md` — copy-paste charter skeleton
- `references/gates-and-validators.md` — enforcement-layer design rules (3 tiers, status vocabulary, never-fabricate branch)
- `references/self-evolution-loop.md` — READ/CAPTURE/RECONCILE/PROMOTE wiring
- `references/project-seed.md` — starter AGENTS.md for any new project
- Rows in `SKILL-MAP.md` + `README.md` (inventory gate passes)

## Weave-in checklist (each is a ≤10-line edit)

- [ ] **`/start` (Conductor)** — after the stack/scaffold stage, offer:
      "want the quality system installed before we build? → `/quality-charter`".
      New projects get the seed (`references/project-seed.md`) at scaffold time.
- [ ] **`/scaffold`** — drop `reference/charter.md` (from the template, mostly
      empty) + `reference/learnings.md` (layer headers only) + `reference/exemplars/README.md`
      into every scaffolded project, the way `.env.example` is dropped today.
- [ ] **`/ship`** — before "green, reviewed branch" is declared: if the project
      has a charter, run its validators + Present Gate as one more exit
      condition. (Ship's anti-cheat loop already has the right shape.)
- [ ] **`/goal`** — task contracts gain one line: "which charter rules bind
      this task" (cite by number).
- [ ] **`/audit`** — add a 10th category: quality-architecture presence
      (charter? gates? learnings loop? exemplars?) scored via the
      `/quality-charter` step-1 diagnosis.
- [ ] **`/health`** — one of the 12 checks becomes "quality system installed
      and being read" (learnings file has entries newer than the last N
      corrections).
- [ ] **`speckit-implement`** — read the project charter (if present) at step
      1 alongside the spec; cite rule numbers in the completion report.
- [ ] **`agent-eval`** — cross-link: gate questions from a charter make good
      eval rubric rows; note it in both directions.
- [ ] **`lessons_injector.py` / capture-lessons hook** — teach the lessons
      format the two-layer (Rules / dated log) + `[promoted:]` convention from
      `self-evolution-loop.md`, so kit-level lessons follow the same
      reconcile/promote lifecycle.
- [ ] **`HANDOFF.md`** — add `/quality-charter` as a routing target
      (from `/start`, `/audit`, `/health`).

## Testing after weave-in

1. Fresh session → `/guide` → confirm `quality-charter` is discoverable.
2. `/scaffold` a toy project → confirm seed files land.
3. `/ship` on a project WITH a charter → confirm the gate runs; on a project
   WITHOUT one → confirm ship behaves exactly as before (no new friction).
4. `python3 plugins/vibe-coding-skills/scripts/check_inventory.py` still OK.

## Known limitations / v2

- The skill installs the *files*; it does not yet generate project-specific
  validator scripts beyond routing to `/ship` — a `validator-cookbook.md`
  (common checks: banned-phrases, placeholder-scan, link-check, spec-parse)
  would make that step mostly copy-paste.
- Fresh-eyes review is prescribed but not automated; a small
  `content_loss_diff.py` (old vs new instruction file → dropped-meaning
  candidates) would mechanize the refactor half of it.
