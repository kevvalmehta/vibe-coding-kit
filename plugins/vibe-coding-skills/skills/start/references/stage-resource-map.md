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
| If the app has AI inside | **`agent-architect`** | Designs the AI agents (how many, which model, approval gates). |
| What to build it with | **light stack suggestion** | A sensible default (kit defaults + project type) + one-line why. Full decider = a later version. |
| Before coding vs a library | **GitMCP** | Lets the AI read the library's REAL current docs, so it can't invent functions. |
| …building an AI feature | **cookbook** | Real, tested Claude recipes (evals, tool use, caching) instead of guessed code. |
| Write spec / plan / tasks | **`/speckit-*`** (via `idea-to-app`) | The gated planning spine — drive it, don't rebuild it. |
| Build it | **Superpowers** | Tests first, isolated copy, fresh-eyes review. |
| Prove the AI output is good | **`agent-eval`** | Scores fuzzy AI output against a rubric + a CI gate (only if the app has AI). |
| Confirm it works | **`/verify`** | Runs the real thing + a risk rating + proof. |
| Check it's safe | **`/security-review`** | Inputs validated, no secrets, database locked down. |
| Save + ship | **`git-safety`** | Branch → PR → preview. The Conductor STOPS before anything goes live. |

**v1 note:** the Conductor *drives* the bold spine (discover → grill-me + research-scout → loop-design
+ stack suggestion → speckit/build → verify → security → git-safety) and *names* the rest
(recommender, GitMCP, cookbook, agent-architect, agent-eval) at their moment. Deep-wiring those is v2
(see memory `conductor-roadmap`). If any resource isn't connected/available, say so and continue —
never pretend it ran.
