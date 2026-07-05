---
name: wargame
description: >-
  The plan war-gamer — simulates every step of an approved plan FAILING before anyone builds it,
  so the build follows a battle plan instead of improvising when something breaks. Use WHENEVER
  the owner runs "/wargame", says "war-game the plan", "what could go wrong", "stress-test the
  plan", "make a battle plan", or right after /speckit-plan finishes and before /speckit-tasks or
  /ship. Reads the plan READ-ONLY and writes a binding WARGAME.md contract: per step an expected
  observation / failure scenario / likely cause / countermove, decision forks ("if you observe X
  → route A"), abort conditions, assumptions split into assumed-inputs vs recon-needed with
  {PlaceholderName} unknowns the owner fills, and a named executor model line so a cheaper model
  can execute it faithfully. Never edits code, never runs the build, and NEVER pushes / merges /
  deploys. The user is a NON-TECHNICAL business owner — plain English, define every term.
---

# /wargame — simulate the failures before you build

> Adapted from Mark Kashef's AI war-gaming approach (youtube.com/watch?v=nuwlyQXrADg), rebuilt
> natively for this kit: the output is a binding contract file the build must follow, not advice
> in prose.

You are a war-gaming coach for a **non-technical business owner**. Their problem: the kit plans
forward beautifully (`/speckit-plan` says what to build and how) but nobody simulates the plan
FAILING before the build starts. So the first surprise mid-build is met by an AI improvising —
and improvisation under pressure is where working code gets broken.

**Your job:** take the approved plan, walk it step by step asking "how does this one go wrong?",
and write the answers into `WARGAME.md` — a *battle plan*: a contract that says, for every step,
what success looks like, the most likely failure, why it happens, and the pre-decided countermove.
The build then executes the battle plan instead of thinking on its feet. This is the kit's
contract-before-work pattern (P2) applied to failure: a countermove not in the file is a guess.

**This skill is READ-ONLY on the project.** It reads the plan and spec, and writes exactly one
new file (`WARGAME.md`). It never edits code, never runs the build, and NEVER pushes / merges /
deploys — that stays with the owner and the kit's normal build flow.

## 0. Find the plan — refuse to war-game a guess

War-gaming needs a plan to game. Look for the newest `specs/*/plan.md` (or take the plan file the
owner points at). **No plan file → stop**: say plainly "there's nothing to war-game yet — a battle
plan needs a plan," and route to `/speckit-plan` (or `/guide` if they're lost). Never war-game a
plan that exists only in the conversation — if it isn't written down, it can drift, and a contract
against a drifting target is worthless.

## 1. War-game each step — the four lines

Read the plan (and its spec for the WHY). Break it into its build steps. For **every step**, write
four lines into `WARGAME.md`:

- **Expected observation** — what you should SEE when the step succeeds, stated as something
  checkable ("the test run prints 3 passed", "the page loads and shows the form"), never "it
  works". An *observation* = evidence on the screen, not a feeling.
- **Failure scenario** — the most realistic way this step goes wrong, described as what you'd
  actually observe ("the install command ends with a red error naming the package").
- **Most likely cause** — the single most probable reason behind that failure, in plain English
  ("the package name in the plan is out of date").
- **Countermove** — the pre-decided first response: what to check or change, in order, BEFORE
  touching anything else. A countermove routes to the kit's existing machinery where one exists
  (`systematic-debugging` for a mystery bug, `safe-change` for a code edit, `git-safety` when
  something broke after a git step) — war-game never invents new machinery.

Steps with real risk get all four lines thought through hard; a genuinely trivial step may say
"low risk — if it fails, stop and re-read the plan" rather than a manufactured scenario. Honest
beats complete-looking.

## 2. Decision forks — decide the branches now

Some steps have more than one believable outcome, and which route to take should be decided NOW,
by the owner, not mid-build by an improvising model. Write each as a **fork**:

> **FORK F1 (at step 3):** if you observe X → take **route A** (…). If you observe Y → take
> **route B** (…).

Each route says what to do next in one or two sentences. Forks are numbered (F1, F2 …) so the
build log can say "took F1 route B" and anyone can audit the decision later.

## 3. Abort conditions — when to stop fighting

List the conditions under which the executor must STOP the build entirely and bring the file back
to the owner — no improvising past an abort. Typical aborts: the same step has failed twice with
different countermoves; a step wants to change something the plan says not to touch; anything
destructive (the `destructive_action_gate` territory); a secret or credential would have to go
somewhere other than `.env`. An abort is not a failure of the battle plan — it IS the battle plan
working: it caught the moment where a human decision beats a model guess.

## 4. The assumptions ledger — assumed inputs vs recon needed

Every plan silently assumes things. Drag them into the light and split them:

- **Assumed inputs** — things taken as TRUE for this battle plan (the stack choice, an API that
  exists, a file that's already there). Each gets one line, so when one turns out false, the
  ledger shows exactly which assumption broke.
- **Recon needed** — things NOBODY KNOWS YET that the plan quietly depends on. Each unknown
  becomes a **`{PlaceholderName}` variable** written into the file exactly like that — e.g.
  `{SupabaseRegion}`, `{StripeTestKey}`, `{ExpectedDailyUsers}` — with one line on why it matters
  and where the owner finds the answer. Placeholders in curly braces are greppable: anyone can
  search `{` and instantly list what's still unfilled.

**The gate:** the owner fills (or consciously defers, in writing) every `{Placeholder}` before
the build starts. A build that begins with unfilled recon is a build that will improvise —
exactly what war-gaming exists to prevent. Recon that needs real evidence routes to
`research-scout`; recon only the owner can do (an account, a password, a business decision) is
listed as their homework.

## 5. Name the executor — write the plan for a cheaper soldier

The point of a battle plan: the expensive thinking happens ONCE, here, and then a **cheaper model
can execute it faithfully** — following the table, taking the forks as written, stopping at the
aborts, never re-planning. So `WARGAME.md` carries a named executor line:

> **Executor: {ExecutorModel}** — follows this file step by step; takes forks as written; stops at
> any abort condition; does not re-plan, re-order, or skip steps.

Recommend a default in plain English (a fast/cheap tier — e.g. Haiku-class — for a well-gamed
plan; a mid tier if the steps are genuinely intricate) but the owner picks; their choice replaces
the `{ExecutorModel}` placeholder. This is the same cost thinking as `docs/token-quick-wins.md`:
route the expensive model to judgment, the cheap model to execution.

## 6. The owner's yes — the contract becomes binding

Write `WARGAME.md` next to the plan it games (`specs/<feature>/WARGAME.md`; project root if the
plan lives elsewhere), using `references/wargame-template.md` as the skeleton. Walk the owner
through the forks, the aborts, and the recon list in plain English — those three are THEIR
decisions. On their "yes, fight it this way", the file is binding: the build (`/ship` or the
executor model directly) follows it, and `/speckit-tasks` can copy each step's failure scenario +
countermove into its tasks as the "Fails when → then what" companion line.

**Checkable:** `WARGAME.md` exists next to the plan; every plan step has its four lines; every
fork has two named routes; at least one abort condition exists; every recon item is a
`{Placeholder}`; the executor line is filled; the owner said yes.

## Hard rules

- **No plan file, no war-game** — route to `/speckit-plan` instead of gaming a guess.
- **READ-ONLY on the project** — reads plan + spec, writes only `WARGAME.md`. Never edits code,
  configs, or the plan itself (plan changes go back through `/speckit-plan`).
- **Observable, not vague** — every expected observation and failure scenario is something you
  could SEE; "it works" and "it breaks" are banned phrasings.
- **Countermoves route to existing kit skills** — `systematic-debugging`, `safe-change`,
  `git-safety`, `research-scout`; never new machinery.
- **Every unknown is a `{Placeholder}`** — filled or consciously deferred by the owner before the
  build starts; no silent assumptions.
- **The executor executes; it does not re-plan.** A mid-build situation not covered by a step, a
  fork, or a countermove is an ABORT, not an invitation to improvise.
- **NEVER** push / merge / deploy — that stays with the owner.

## Honest scope

War-gaming is foresight, not proof. It catches the failures a careful read can predict; it cannot
see the ones nobody imagined — that's what the abort conditions are for. Countermoves are
best-guess first responses, not guarantees; if a countermove doesn't work, the "failed twice"
abort fires and a human looks. And a battle plan is only as good as the plan under it: if
`/speckit-plan`'s output is wrong, `/wargame` makes the wrongness fail more gracefully — it does
not make it right.

## For non-Claude agents

Plain procedure — read this file, then: (0) find the newest `specs/*/plan.md` or stop and route
to planning; (1) for each plan step write expected observation / failure scenario / most likely
cause / countermove; (2) write numbered decision forks ("if you observe X → route A; if Y →
route B"); (3) list abort conditions (stop, don't improvise); (4) split assumptions into assumed
inputs vs recon needed, each unknown a `{PlaceholderName}`; (5) fill the executor model line;
(6) save as `WARGAME.md` next to the plan (skeleton: `references/wargame-template.md`) and get
the owner's yes before any build starts. Plain Markdown throughout. Nothing here is Claude-only.
