# Stage → resource map (the Conductor's core knowledge)

This is what the Conductor knows that the owner doesn't: **which tool fits which moment.** At each
stage, name the resource, explain in plain English what it is + why now, route to it, then checkpoint.

| Stage | Resource (route to) | Plain-English why |
|---|---|---|
| Fresh project opened | **recommender** (`claude-code-setup`) | Suggests helpful automations (hooks, connections) for this project. Optional; offer once. |
| Is it worth building? | **`/discover`** | Checks real demand before you spend effort (pain-mines users, scores the gap). |
| Pin down the plan | **`grill-me`** | Interviews you one question at a time until the plan is solid. |
| …with real evidence | **`research-scout`** *(consent)* | Finds cited prior-art ("how others built this") so answers aren't guesses. ASK before running. |
| How the build runs | **`loop-design`** | Picks the shape: once / repeat-until-right / split across helpers / steps (+ a STOP rule). |
| If the app has AI inside | **`agent-architect`** *(auto-driven inside `idea-to-app` GATE 5 — confirm, don't re-run; see v2 section)* | Designs the AI agents (how many, which model, approval gates). |
| What to build it with | **light stack suggestion** | A sensible default (kit defaults + project type) + one-line why. Full decider = a later version. |
| Before coding vs a library | **GitMCP** | Lets the AI read the library's REAL current docs, so it can't invent functions. |
| …building an AI feature | **cookbook** | Real, tested Claude recipes (evals, tool use, caching) instead of guessed code. |
| Write spec / plan / tasks | **`/speckit-*`** (via `idea-to-app`) | The gated planning spine — drive it, don't rebuild it. |
| …plan approved, want it failure-tested first | **`/wargame`** | Simulates each step going wrong BEFORE the build: what success looks like, the likely failure, the pre-decided countermove, and when to stop — written into a contract the build follows instead of improvising. |
| Build it | **Superpowers** | Tests first, isolated copy, fresh-eyes review. |
| …and it has a screen | **`/design-craft`** | Decides the LOOK before markup (a written design contract), then scans the result for the "looks AI-generated" tells. |
| …and it must remember things | **`/data-model`** | Interviews you in plain English, writes the table plan into a contract you approve — before any table exists. |
| …and it needs user accounts | **`/add-login`** | Adds login the boring, safe way (managed auth, magic links default) and proves one user can't read another's data. |
| …and it takes money / sends email / stores uploads | **`/wire-up`** | Connects the outside service in test mode first; nothing real moves until you flip the keys. |
| Just went live | **`/uptime`** + **`/cost-watch`** | A free robot that emails you if the site stops loading; a cap or alert on every service that can bill you. |
| Prove the AI output is good | **`agent-eval`** | Scores fuzzy AI output against a rubric + a CI gate (only if the app has AI). |
| Confirm it works | **`/verify`** | Runs the real thing + a risk rating + proof. |
| Check it's safe | **`/security-review`** | Inputs validated, no secrets, database locked down. |
| Save + ship | **`git-safety`** | Branch → PR → preview. The Conductor STOPS before anything goes live. |

## v2 — the extras are now DRIVEN, not just named

In v1 the Conductor *named* the five optional extras at their moment. **v2 drives them**: each fires on
a **trigger**, is **availability-checked** against the live session tool list, **consent-asked**, then
routed in. The four-step rule (trigger → availability → consent → route in → checkpoint) and the full
table live in the skill's section 3a. Quick reference:

| Extra | Trigger | Availability check |
|---|---|---|
| **recommender** | Fresh project, at the greeting | Plugin installed? |
| **GitMCP** | About to code against a named library | `gitmcp` tools loaded this session? |
| **cookbook** | AI-inside = YES, building the AI part | `cookbook` tools loaded this session? |
| **agent-architect** | AI-inside = YES, plan stage (already inside `idea-to-app` GATE 5) | Skill — always available |
| **agent-eval** | AI-inside = YES, after the build | Skill — always available |

The **AI-inside** answer (reused from `idea-to-app`'s GATE 0) is the trigger that gates the last three.
If any resource isn't connected/available, **say so and continue — never pretend it ran** (Principle VII).
The bold spine (discover → grill-me + research-scout → loop-design + stack suggestion → speckit/build →
verify → security → git-safety) is still driven directly. v3 = full stack-decider; v6 = a portable
on-disk availability-prober (deferred from v2). See memory `conductor-roadmap`.
