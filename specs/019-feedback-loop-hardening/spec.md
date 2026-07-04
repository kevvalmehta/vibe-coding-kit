# Spec 019 — Feedback-Loop Hardening

## WHY
Two sources reviewed 2026-07-04: OpenAI's "harness engineering" post and the
loss-function-development (LFD) thread. Kit verdict: harness fundamentals already
built (registered docs, mechanical gates, worktrees, checked-in plans); the real
gaps are in the FEEDBACK LOOPS — "a constraint without an instrument is a vibe,"
eval sets small enough to memorize, and stall handling that only stops rather than
forcing a new idea first.

## WHAT (all docs/skills; no scripts)

1. **agent-eval — answer-key blinding.** When any agent iterates on an AI feature
   against an eval set, it must NEVER read the expected answers; it sees the score
   and failed-case CATEGORIES only. Answers exist for post-hoc scoring. A small eval
   with visible answers gets memorized in one round (LFD: a 28-item eval was
   memorized immediately); blinding forces a general fix instead.

2. **/goal — instruments rule + target mode.** New rule: every constraint in a goal
   contract must name the command/check that MEASURES it (wall-clock elapsed, spend,
   test count) — an unmeasurable constraint is a vibe the agent will cheerfully
   violate. Agents have no time sense; elapsed wall-clock is a first-class
   instrument. Plus a short optional "target mode" paragraph: for optimization
   problems, define a bar to descend toward (e.g. 95% of N held-out cases) instead
   of a finite done-when — with blinding per item 1.

3. **/ship — iteration log + entropy on stall.** The bug-fix loop logs, per attempt:
   hypothesis → expected failure mode → diagnostic result (survives context
   compaction; makes attempts reviewable). On a no-progress attempt, the NEXT
   attempt must state a genuinely different hypothesis — repeating the prior
   approach "but harder" is banned. All existing exits unchanged: cheat-detection
   still hard-stops, 3-attempt cap and budget exits stay.

4. **Scar Log graduation path** (.specify/memory/lessons.md): a note in the
   workflow — any confirmed L-# scar that is mechanically checkable (a regex or a
   file check could catch it) should GRADUATE into a hook/lint/CI check instead of
   remaining prose. Prose lessons rely on the model remembering; checks fire 100%.

5. **/scaffold — legibility line.** Starter READMEs advise structured logs (one
   event per line, plain words) so the AI can read the app's own behavior when
   debugging, instead of guessing.

## NOT in scope
Installing elvisun/loss-function-development (method already extracted); relaxing
any blocking gate; cron cleanup agents; architecture linters; new scripts/hooks.

## Done when
Guard test green; full suite green; registered in AGENTS.md/SKILL-MAP/HANDOFF; CI
green. (This is the mirror into vibe-coding-kit — origin is Perfecting Coding Spec
Kit spec 019, ported verbatim with skill/lessons paths adapted to this repo's
plugin layout.)
