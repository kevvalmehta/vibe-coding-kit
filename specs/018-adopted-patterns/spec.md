# Spec 018 — Adopted Patterns Batch (mattpocock/skills review, 2026-07-03)

## WHY
Review of mattpocock/skills (MIT) found four patterns worth rebuilding natively
(kit rule: never install, rebuild). Everything else in that repo is already covered
by stronger kit equivalents.

## WHAT
1. **/pathfinder** (new skill; adapted from wayfinder, in-progress draft): for ideas
   too big/foggy for one session, BEFORE /speckit-specify. Local-markdown map
   (`pathfinder/map.md` in the project): Notes, Decisions-so-far (index, one line +
   link each), Fog (questions felt but not yet sharp). Tickets = one sharp question
   each, one file per ticket (`pathfinder/tickets/`), four types routed to EXISTING
   kit skills: research→research-scout, prototype→/prototype, grilling→grill-me /
   grill-with-docs, task→manual checklist. Frontier = open tickets not blocked by
   others. HARD RULES: one ticket resolved per session; chart-the-map session never
   also resolves tickets; fog is written down, never pre-sliced into fake tickets;
   ticket vs fog test = "can you phrase the question sharply now?". Exit: fog empty +
   no open tickets → hand the Decisions-so-far index to /speckit-specify. Plain
   English throughout (non-technical owner).
2. **Merge-conflict rescue** (git-safety): new section — what a conflict IS (two
   saved versions of the same lines colliding; git refuses to guess), plain-English
   walkthrough (don't panic; nothing is lost; both versions shown in the file between
   <<<<<<< / ======= / >>>>>>> markers), the AI runs the mechanics and shows both
   versions in plain words, owner picks; `git merge --abort` as the always-safe
   escape hatch; never resolve blind on migration/schema files (017 gate territory).
3. **Two-axis review lens** (/ship review stage): review on TWO separate axes so one
   can't mask the other — (a) SPEC FIDELITY: does it do what the spec says (nice code
   building the wrong thing fails here); (b) STANDARDS: is it built well (correct
   behavior written badly fails here). Report each axis separately.
4. **domain-modeling named entry** (SKILL-MAP.md): register the discipline by name —
   challenge fuzzy terms, keep a shared project language (CONTEXT.md glossary), record
   hard decisions sparsely (ADRs) — pointing at grill-with-docs as its home, so other
   skills can invoke it by name.

## NOT in scope
Installing anything from the source repo; HTML architecture reports; setup skill;
codebase-design / teach (parked); scripts or hooks (docs/skills only).

## Done when
Guard test green; full suite green; registered in AGENTS.md + SKILL-MAP.md + README
index + HANDOFF.md (Principle VI); mirrored to vibe-coding-kit; CI green both PRs.
