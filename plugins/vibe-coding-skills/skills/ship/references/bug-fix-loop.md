# The bug-fix loop — `/ship`'s safe self-healing cycle

Grounded in `research/self-healing-loop-safety.md` (cited research-scout pass, 2026-06-25). A *loop* =
repeating a step until a goal is met. This is the part of `/ship` that, after a build, gets failing
tests to green **without** the AI cheating its way there.

> ⭐ **The headline risk: the AI faking a fix.** Research measured frontier models making a failing test
> "pass" by deleting/skipping it or hardcoding the expected answer **33–76%** of the time. So this loop
> is built to make that impossible, enforcing constitution **Principle II** ("never make a failing test
> pass by deleting, skipping, or weakening it") mechanically — not as a hope.

## How one pass works

1. **Run the full test suite** — an *independent* run (the source of truth), not the builder's say-so.
2. If green → exit the loop (done). If red → continue.
3. **Pick ONE failing test** (the first / most fundamental). Fix **one failing test per pass** — fixing
   everything at once thrashes and rarely converges.
4. **Feed the real failing-test output** (the actual error/traceback) to `systematic-debugging` as the
   feedback for this pass — targeted direction, not a blind "try again."
5. The fix may change **source code only**.
6. **Diff-check the fix** (next section) before it counts.
7. Re-run the full suite (back to step 1).

## The iteration log (log this before every attempt)

Three lines, written down before you try anything, then completed after running:
1. **Hypothesis** — what I think is actually broken.
2. **Expected failure mode** — what I'd expect to still see if this hypothesis turns out wrong.
3. **Diagnostic result** (filled in after running) — what the real output showed.

This survives context compaction (the point where earlier reasoning in a long session gets
summarized away and lost) and makes every attempt reviewable by the owner instead of a vague "tried
again."

**Entropy on stall.** If an attempt makes no progress, the next attempt's hypothesis must be
**genuinely different** — a different theory of the bug, not the same one turned up louder. Repeating
the prior approach "but harder" (bigger timeout, broader regex, one more retry) is banned. This is a
quality bar on what an attempt may look like — it does not add a 4th attempt or loosen the stop rule
below.

## Anti-cheating guardrails (layered — no single one is enough)

1. **Test files are READ-ONLY.** The fix step may edit source code; it may **never** edit the test files
   or the test-runner config. (Research: making tests read-only is the highest-leverage anti-cheat.)
2. **Diff-check every fix and REJECT it (never count as a pass) if it:**
   - edited or deleted a **test** file or the test-runner config,
   - added a **skip**/`xfail`/`@pytest.mark.skip` or commented-out a test,
   - **hardcoded** a literal equal to the expected value (so the test passes without real logic),
   - **weakened** an assertion (loosened a check, removed cases).
   A detected cheat is **escalated to the owner immediately — never retried** (the AI is now working
   against the goal, so more attempts make it worse, not better).
3. **"Green" is confirmed by the independent full-suite run**, not by the builder reporting success.

## The STOP rule (multiple independent exits — the runaway guard people forget)

The loop STOPS and hands back to the owner (plain-English summary of what's still failing + what it
tried) when **ANY** of these fire:

- **3 fix attempts** on the same bug (the cost backstop — raising this does NOT make a stuck loop
  converge, so keep it small).
- **No progress** — the same failure or an unchanged diff repeats (2–3×), OR the same test keeps failing
  after distinct attempts (oscillation): the loop is circling a dead end / the bug is mis-understood, not
  mis-typed. Break early; don't burn budget.
- **A cheat is detected** (a guardrail above trips) → stop + escalate **immediately**.
- **Budget exhausted** (token/time) without green.

On any stop, `/ship` reports in plain English: which test is red, what the error says, what it tried,
and the one or two things the owner (or a fresh session) could check next. It never reports "done" on a
red suite, and never reports a faked pass as success (Principle VII).
