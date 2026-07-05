# Spec 030 — /wargame: war-game the plan before the build (2026-07-05)

## WHY
The kit plans forward (`/speckit-plan`) but never simulates the plan FAILING before the build
starts, so the first mid-build surprise is met by an AI improvising — the moment working code
gets broken. Item 7 of the 2026-07-05 gap survey; concept adapted from Mark Kashef's AI
war-gaming approach (youtube.com/watch?v=nuwlyQXrADg), rebuilt on the kit's contract-before-work
house pattern (a named file the owner approves → checkable steps → honest scope → plain English).

## WHAT
1. **/wargame** (new skill): after `/speckit-plan` (or pointed at any existing plan file), reads
   the plan READ-ONLY and writes a binding `WARGAME.md` next to it containing:
   - per plan step, four lines: **expected observation** (checkable success condition),
     **failure scenario** (what you'd observe), **most likely cause**, **countermove**
     (pre-decided first response, routed to existing kit skills: systematic-debugging /
     safe-change / git-safety / research-scout — never new machinery);
   - numbered **decision forks** — "if you observe X → route A; if Y → route B" — decided by the
     owner now, not by a model mid-build;
   - **abort conditions** — where the executor STOPS and returns to the owner (failed twice,
     out-of-plan change, destructive action, secret outside `.env`); improvising past an abort
     is banned;
   - an **assumptions ledger** split into *assumed inputs* (taken as true, one line each) vs
     *recon needed* — every unknown a greppable `{PlaceholderName}` variable the owner fills or
     consciously defers before the build;
   - a named **executor model** line ("Executor: {ExecutorModel} — follows this file step by
     step; takes forks as written; stops at aborts; does not re-plan") so a cheaper model can
     execute the battle plan faithfully.
   Refuses with no plan file (routes to `/speckit-plan`). Skeleton in
   `references/wargame-template.md`. Never edits code; NEVER pushes/merges/deploys.
2. **Absorption — tasks template**: the "Done when" convention
   (`.specify/templates/tasks-template.md`, Completion Criteria section) gains a companion line:
   a risky task may carry "Fails when → then what", copied verbatim from `WARGAME.md` when one
   exists.
3. **Absorption — /pathfinder Fog**: a fog entry holding a nameable-but-unanswered VALUE is
   marked as a `{Variable}` placeholder — the same unknowns-ledger notation as `/wargame`'s
   recon list.

## NOT in scope
Running the build (that's `/ship` / the executor); editing the plan (back through
`/speckit-plan`); scripts or hooks (docs/skills only); any push/merge/deploy.

## Done when
Guard test (`tests/test_wargame.py`) green; full suite green; registered in SKILL-MAP.md +
AGENTS.md + README index + QUICKSTART + `/guide` map + `/start` stage-resource-map + HANDOFF.md
(Principle VI); PR opened (owner reviews → merge).
