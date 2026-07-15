# Loop pattern catalog (local, portable)

A small curated set of **proven loop patterns**, copied with attribution from the MIT-licensed
**loop-library** by Forward-Future.

- **Source:** https://github.com/Forward-Future/loop-library — live catalog at
  https://signals.forwardfuture.ai/loop-library/catalog.json
- **License:** MIT (attribution kept; see source repo for full licence text).
- **Pulled:** 2026-06-22. The live library had 51 loops; the dozen below are the ones most relevant to
  the kind of app a solo owner builds. To refresh or add more, the `/upstream-check` skill watches this
  repo (it's row #2 in `upstream-sources.md`).

Each entry below keeps loop-library's own wording for the prompt, the verification, and the steps, then
maps them onto this kit's four-part frame (**Goal · Success measure · Next-step rule · Stop condition**).
**These are starting points — adapt thresholds and tools to the project, but never strip the verification
or the give-up ceiling.**

---

## Test coverage until done — *from loop-library #005, "The 100% Test Coverage Loop"*
- **Use when:** 100% coverage is an explicit project requirement with a trustworthy coverage command.
- **Prompt (theirs):** "Add tests until we have 100% test coverage."
- **Verification (theirs):** the full test suite passes at 100% coverage, using the project's coverage report.
- **Steps (theirs):** run full suite, save baseline → prioritise uncovered branches by risk → add
  meaningful tests → repeat until 100%.
- **Frame:** Goal = full coverage · Success = coverage report at 100%, suite green · Next-step = add a
  test for the riskiest uncovered branch · Stop = 100% reached **OR** no new coverage gained for N rounds.

## Docs match the code — *from loop-library #001, "The Docs Sweep"*
- **Use when:** code changes may have left READMEs, setup guides, API references, or examples behind.
- **Prompt (theirs):** "review the codebase in full and make sure all documentation reflects the current implementation."
- **Verification (theirs):** documentation matches the current implementation, delivered as a reviewable pull request.
- **Steps (theirs):** review changes → compare docs with code → update stale material → run checks, open PR.
- **Frame:** Goal = docs match reality · Success = no drift found on a re-scan · Next-step = fix the next
  stale doc · Stop = a clean re-scan **OR** the PR is opened for review (then a human decides).

## Make pages fast — *from loop-library #003, "The Sub-50 ms Page-Load Loop"*
- **Use when:** there's a defined set of pages, a stable speed-test, and a concrete target.
- **Prompt (theirs):** "Continue optimizing… after each significant change, measure page-load… until every page loads in under 50 ms."
- **Verification (theirs):** every page meets the threshold on the same benchmark, with no regressions.
- **Frame:** Goal = every page under the target · Success = the speed test passes for all pages · Next-step
  = speed up the slowest failing page · Stop = all pass **OR** no improvement after N rounds.

## Ticket → review-ready fix — *from loop-library #016, "The Ticket-to-PR-Ready Loop"*
- **Use when:** a loosely written ticket or complaint needs to become a bounded, proven change.
- **Prompt (theirs):** "Turn ticket into review-ready patch… reproduce failure, prove root cause, make smallest fix, rerun tests."
- **Verification (theirs):** the failure is fixed, verified, and ready for review, with before-and-after proof.
- **Frame:** this is really a **multi-step workflow** (reproduce → root cause → smallest fix → tests → PR),
  with a stop-for-review gate at the end. Good example of when NOT to pick a loop.

## Fix what's broken in production — *from loop-library #004, "The Production Error Sweep"*
- **Use when:** a scheduled reliability pass where the agent can read production telemetry.
- **Prompt (theirs):** "Review our production logs… trace it to root cause, fix it, verify, and open PR… stop without changes if no actionable errors."
- **Verification (theirs):** actionable production errors are fixed and verified; otherwise a clean stop.
- **Frame:** Goal = no actionable errors left · Success = each fix verified · Next-step = take the next
  actionable error · Stop = none left **OR** clean stop if there were none to begin with. Note the honest
  "do nothing if nothing's wrong" stop.

## Argue against your own design first — *from loop-library #024, "The Devil's-Advocate Loop"*
- **Use when:** before committing to an architecture, interface, or rollout plan.
- **Prompt (theirs):** "Have critic argue design is wrong… record objections… builder fixes or documents acceptance."
- **Verification (theirs):** no high-impact objection remains open (resolved or explicitly accepted with evidence).
- **Frame:** Goal = no unanswered serious objection · Success = objection log all closed · Next-step =
  answer the next open objection · Stop = log clear **OR** remaining items explicitly accepted with reasons.

## Two independent checkers must agree — *from loop-library #034, "The Multi-LLM Convergence Loop"*
- **Use when:** an important plan or code change benefits from two independent AI perspectives.
- **Prompt (theirs):** "Review [work] against [bar] for [pass limit] rounds… alternate model families… succeed only when both approve."
- **Verification (theirs):** two different AI model families approve the exact same version.
- **Frame:** Goal = both reviewers approve · Success = same version passes both · Next-step = fix findings,
  hand to the other reviewer · Stop = both approve **OR** the pass-limit (give-up ceiling) is hit.

## Build, then a second agent verifies — *from loop-library #020, "The Loop Harness Verification Loop"*
- **Use when:** a recurring task should run unattended, but one agent must not both produce and approve its own work.
- **Prompt (theirs):** "first Claude stages patch, second Claude verifies… ship only on pass."
- **Verification (theirs):** only independently verified output ships; a second-agent pass is required.
- **Frame:** Goal = only verified work ships · Success = the second agent passes it · Next-step = on a
  fail, the first agent fixes and re-stages · Stop = verified pass **OR** the retry limit is reached.

## Keep a streak of passing real-world cases — *from loop-library #009, "The Quality Streak Loop"*
- **Use when:** quality needs a strict consecutive-success bar and failures should improve test coverage.
- **Prompt (theirs):** "Test realistic scenarios… document failure, add coverage, fix it, restart streak… stop after [N] successful cases."
- **Verification (theirs):** the latest N realistic cases pass in a row, every failure documented and protected.
- **Frame:** Goal = N in a row pass · Success = the streak hits N · Next-step = on a fail, document it,
  add a test, fix, reset the streak · Stop = streak of N reached.

## Update a value everywhere it lives — *from loop-library #033, "The Propagation Compliance Loop"*
- **Use when:** you changed something that appears in several files (a version number, a feature name).
- **Prompt (theirs):** "List where new value belongs and update it… search for old value… review each match… fix stale only."
- **Verification (theirs):** no unintended copy of the old value remains; only intentional matches left.
- **Frame:** Goal = no stale copies · Success = a search for the old value returns only intentional hits ·
  Next-step = fix the next stale copy · Stop = search is clean.

## Score a real user flow and improve it — *from loop-library #036, "The UI/UX Score Loop"*
- **Use when:** a real task (signup, login, checkout) can be exercised end-to-end in a browser.
- **Prompt (theirs):** "Improve [user flow] at [URL] until [criterion]… fresh browser state… score screens with checklist… improve weakest."
- **Verification (theirs):** the complete task scores better without making any important screen worse.
- **Frame:** Goal = the flow clears the bar · Success = every screen scores at/above the checklist bar ·
  Next-step = improve the weakest screen · Stop = all clear **OR** no improvement after N rounds.

## Builder + adversarial reviewer pass a baton — *from loop-library #027, "The Autonomy-Loop Builder-Reviewer Loop"*
- **Use when:** the repo has deterministic test/build/lint gates and a task suited to repeated handoffs.
- **Prompt (theirs):** "builder makes change and adds red-before, green-after test… reviewer proves test."
- **Verification (theirs):** every accepted wave passes a proof-of-test gate (the reviewer confirms the
  test actually fails without the fix).
- **Frame:** Goal = every change is independently proven · Success = reviewer's proof-of-test passes ·
  Next-step = next change, next review · Stop = task complete **OR** retry ceiling hit.
