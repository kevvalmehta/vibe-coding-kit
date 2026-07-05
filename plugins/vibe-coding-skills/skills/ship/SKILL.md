---
name: ship
description: Build auto-chaining (Conductor v4) — drives the whole BUILD phase end-to-end for a non-technical owner: build (tests first) → confirm it works → fix failing tests in a safe loop → harden security → hand off a green, reviewed branch. The post-plan counterpart of autopilot. Use WHENEVER the owner has an approved plan + tasks and says "build it", "make it", "ship it", "/ship", "run the build", "now build this", or reaches the build stage via /start. It DRIVES existing skills (Superpowers TDD, /verify, systematic-debugging, /security-review, git-safety) — it does not reimplement them. The bug-fix loop carries hard anti-cheat guardrails (test files read-only, every fix diff-checked) and a multi-exit STOP (3 attempts / no-progress / cheat-detected) so it can't loop forever or fake a pass. Checkpoints by default + opt-in "just run it" bypass. NEVER pushes, merges, or deploys — it stops at a green, reviewed branch and hands those to the owner. The user is a NON-TECHNICAL business owner — plain English, define every term, "make sense?" checks.
---

# /ship — build auto-chaining (your "now build it" driver)

The owner is a **non-technical business owner**. Your job: once a plan exists, **drive the whole build
to a finished, working, secure state** so they never have to know which skill comes next. Explain each
stage in plain English, define every term the first time, give a one-line "make sense?", and checkpoint.

You are an **orchestrator** — you DRIVE existing skills, you do not reinvent them (the build-phase
counterpart of `autopilot`, which chains the *planning* phase). The skills you route to: **Superpowers**
(tests-first build), **`/verify`** (confirm it really works), **`systematic-debugging`** (find a bug's
true cause), **`/security-review`** (lock it down), **git-safety** (save points).

## 0. Gate: is there a plan?

`/ship` **refuses to build without an approved plan + tasks** (constitution Principle I — plan before
code). If there's no plan, say so plainly and route the owner back to the planning flow (`autopilot` or
the `/speckit-*` steps). Don't build on a guess.

## 1. Build (tests first)

Route to **Superpowers** to build the tasks **test-first** (write the failing test, then the code to
pass it) in an isolated copy. Explain in plain English what's being built this step. Checkpoint.

## 2. Confirm it works → `/verify`

Route to **`/verify`** — run the real thing + a risk rating + visual/real proof. A passing unit test
isn't the same as "it actually works"; `/verify` checks the real behavior. Checkpoint.

**Review on two separate axes, and report them separately** (adapted from Matt Pocock's skills,
MIT — never blend the two into one verdict):
- **Axis 1 — SPEC FIDELITY:** does the build do what the spec actually says? Beautiful, clean code
  that quietly builds the WRONG THING fails HERE, not on axis 2.
- **Axis 2 — STANDARDS:** is it built well — naming, simplicity, following this project's
  conventions? Correct behavior written badly fails HERE, not on axis 1.

Reporting them separately matters because a pass on one axis can hide a failure on the other — code
that reads beautifully but ignores the spec is not "mostly done," and code that nails the spec but
is a mess is not "fine as-is." Call out each axis's verdict on its own line.

## 3. Fix failing tests → the bug-fix loop (only if red)

If tests are red, run the **bug-fix loop** (full detail in `references/bug-fix-loop.md`). In plain
English, the loop:
- runs the **full test suite** (an **independent** check — the source of truth, not a self-report),
- fixes **one** failing test per pass, feeding the **real failing-test output** to
  `systematic-debugging` as targeted direction,
- treats **test files as read-only** — fixes change source code only,
- **diff-checks every fix** and rejects+escalates any cheat (a fix that edits/skips a test, hardcodes
  the expected answer, or weakens an assertion — never counted as a pass),
- and **STOPS and hands back** to the owner (plain-English: what's failing + what it tried) on **ANY**
  of: **3 attempts** on a bug, **no progress** (same failure unchanged), a **detected cheat**, or
  budget exhausted.

**Before every attempt, log three lines** (this is a quality bar on the attempts, not an extra exit —
see below): the **hypothesis** (what I think is actually broken), the **expected failure mode** (what
I expect to still be wrong if this hypothesis is mistaken), and — after running — the **diagnostic
result** (what the real output showed). This log survives context compaction (the point where an
agent's earlier reasoning gets summarized away) and turns each attempt into something the owner can
actually review, instead of a string of vague "tried again" retries.

**Entropy on stall — no repeating the same idea "but harder."** If an attempt makes no progress, the
NEXT attempt must state a **genuinely different hypothesis** — a different theory of what's broken,
not the same knob turned up. Banned: retrying the same fix with a bigger timeout, a broader regex, an
extra retry loop, or any other "same idea, harder" move. If no new hypothesis is available, that
**is** the no-progress stop below firing — don't manufacture a fake new angle just to keep going.

**All existing exits are unchanged by this.** The 3-attempt cap, the no-progress stop, the
cheat-detection hard-stop, and the budget exit all still fire exactly as before — the hypothesis log
and the entropy rule raise the quality of what happens *inside* each attempt; they do not add, remove,
or loosen any exit.

The loop never reports "done" on a red suite and never passes a faked fix (Principle VII, constitution II).

## 4. Harden security → `/security-review`

Once green + verified, route to **`/security-review`** (inputs validated, no secrets in code, data
locked down). Surface findings in plain English; loop back to fix real ones. CI Semgrep also runs later.

## 5. Hand off — stop at a green, reviewed branch

If the project has a quality charter (`reference/charter.md`), "reviewed" includes it: run the
charter's validator scripts and its Present Gate as one more exit condition before declaring the
branch done (see `/quality-charter`). Projects without a charter: this step is unchanged.

End at a **green, reviewed branch**. Summarize in plain English what was built and verified. Then
**STOP**: push, merge, and deploy are the **owner's** manual action — route them to `git-safety` to do
it themselves. (See the wall below.)

## Keep the owner in control (checkpoints + bypass)

Checkpoint at each stage by default (explain → do/route → stop for OK). If the owner says **"just run
it"** (bypass), move through stages without stopping — **except** the STOP conditions, the anti-cheat
guardrails, and the safety wall, which **always** hold.

## Hard rules

- **Plain English, every term defined**; "make sense?" checks; status at each stage + at any stop.
- **Drive, don't duplicate** — route to Superpowers / verify / systematic-debugging / security-review /
  git-safety; never reimplement them.
- **Refuse to build without a plan** (Principle I).
- **The bug-fix loop never cheats** — test files read-only, every fix diff-checked, cheats escalated;
  never weaken/skip/delete a test to go green (constitution II). Grounding:
  `research/self-healing-loop-safety.md`.
- **Multi-exit STOP** — 3 attempts / no-progress / cheat-detected / budget. Never loop forever.
- **"Green" = an independent full-suite run**, never a self-report (Principle VII).
- **NEVER** push / merge / deploy — in either mode. End at a green, reviewed branch; hand those to the owner.

## Later versions (see memory `conductor-roadmap`)
v4 (this) = build auto-chaining. v6 = availability-prober; v7 = stack scaffolding. Possible v5+: an
optional LLM-judge layer on fix diffs (heavier anti-cheat) + live post-launch monitoring.

## For non-Claude agents
Plain procedure — read this file + `references/bug-fix-loop.md` and follow it. Route to Superpowers /
`/verify` / `systematic-debugging` / `/security-review` / `git-safety` by reading their `SKILL.md`.
Nothing here is Claude-only.
