# SKILL MAP — which skill for which moment

Plain-English cheat sheet for this dev kit. **Not sure what to do? Just run `/guide`** — it reads
where your project is and tells you the one next step. This page is the same map it uses, written
out so you (or any AI tool: Codex, Cursor, Copilot) can eyeball it anytime.

## The normal order (new idea → live)

```
idea
 → /guide                  "where am I, what next?" (ask this anytime)
 → /goal                   vague ask → a task contract (outcome + verification + stop/pause); routes you on
 → idea-to-app             walks every gate below, refuses to skip
 → research                does it exist? competitors? which tools?
 → brainstorm + grill-me   pressure-test the idea until decisions are resolved
 → /speckit-specify        write WHAT + WHY (the spec)
 → /speckit-clarify        answer up to 5 questions to remove fuzziness
 → /speckit-plan           decide HOW (architecture)
 → /speckit-tasks          break into small steps, each with a "Done when"
 → build                   Superpowers: isolated copy, tests first, fresh-eyes review
 → /verify                 confirm it really works (+ risk rating + screenshot)
 → /security-review        inputs, secrets, database security
 → git-safety              save + Pull Request → preview → live
```

**Editing something that already exists is a different path** — use `safe-change`, NOT `idea-to-app`.

**Don't want to hand-run the planning steps?** Use **`autopilot`** — it runs
`/speckit-specify → /speckit-clarify → /speckit-plan → /speckit-tasks → pre-PR checks` as one guided
flow, stopping for your "go" at every step. It never pushes/merges/deploys, and hands back to you for
the build. (Covers the spec→tasks→checks middle of the order above; you still approve each step.)

## The map (situation → skill)

| When you're… | Use | What it does |
|---|---|---|
| Lost / "what do I do now?" | **`/guide`** | Tells you your stage + the exact next skill |
| "What shape is this in? / safe to ship?" | **`/health`** | One 0–100 score across 12 checks + a plain-English ledger of what cost points and how to fix it |
| "What's actually worth fixing?" (existing code, deep) | **`/audit`** | Reads the repo, finds + verifies the highest-leverage issues across 9 categories, writes ready-to-run briefs routed to `safe-change`/`/speckit-specify`/`autopilot`. The deep follow-on to `/health`. Read-only; stops before push/merge/deploy |
| Want the whole planning flow run for you | **`autopilot`** | Runs specify→clarify→plan→tasks→checks, stops for "go" each step; never pushes/merges |
| Your ask is vague / you want guardrails up front | **`/goal`** | Turns it into a task contract: outcome + concrete verification + what-not-to-touch + when-to-stop-and-ask; then routes you to `/speckit-specify` (or runs as-is if tiny) |
| Starting any new idea (even vague) | **`idea-to-app`** | Walks intake → … → ship, won't let you skip a step |
| Pinning down a fuzzy plan | **`grill-me`** | Interviews you one question at a time until it's solid |
| Same, but extending existing code | **`grill-with-docs`** | Grills against your real code + decisions |
| Unsure how a piece of code fits | **`/zoom-out`** | Plain-English map before you touch it |
| Want to try a design before committing | **`prototype`** | Throwaway demo to feel it out, then deleted |
| Writing what the app should do | **`/speckit-specify`** | Creates the spec |
| Spec feels unclear | **`/speckit-clarify`** | Targeted questions, answers folded back in |
| Deciding the architecture | **`/speckit-plan`** | The "how" |
| Breaking work into steps | **`/speckit-tasks`** | Small testable tasks |
| Changing / fixing / editing existing code | **`safe-change`** | Impact map → tests → isolate → review |
| "Did I over-build what I just changed?" | **`/lean-review`** | Looks only at your current changes, lists what to cut (dead code, reinvented built-ins, single-use abstractions) + the simpler replacement. The fast, narrow follow-on to `/audit`. Read-only |
| "What shortcuts did we take on purpose?" | **`/lean-debt`** | Harvests every `shortcut:` comment into a ledger (what was simplified, when it stops being OK, when to revisit); flags shortcuts with no revisit plan. Read-only |
| Enforce "tests first" mechanically during a build | **TDD-Guard** | A safety hook that, during a build, won't let new code be written until a failing test exists for it. Off by default; switched on with a `.tdd-guard` file. Enforces the "tests first" rule mechanically. (Not a skill you run — it runs itself.) |
| Stuck on a bug | **`systematic-debugging`** | Find the root cause before fixing |
| Anything git (save, undo, branch, PR, "it broke") | **`git-safety`** | Keeps `main` working; every change reversible |
| Confirming a change works | **`/verify`** | Real behavior + a screenshot, not just "tests exist" |
| Checking security before shipping | **`/security-review`** | Inputs validated, no secrets, database locked down |
| Your app CONTAINS AI (chatbot, agent, LLM feature, plugin/skill) | **`docs/ai-feature-checklist.md`** | 13 decisions to make in the spec + plan (12-Factor Agents); also: Managed Agents vs plain API |
| Designing the AGENTS for an AI app (how many, which model, managed vs API) | **`agent-architect`** | Proposes the agent design + pre-filled checklist + diagram; suggests managed-vs-API (you decide); grills by default. Recommendation-only |
| Worried the AI is guessing a library's API / functions | **GitMCP** (`gitmcp.io`) | Optional MCP connector — points the AI at a repo's REAL current docs + code so it grounds answers instead of hallucinating. Add `https://gitmcp.io/{owner}/{repo}` (pinned) or `gitmcp.io/docs` (any repo) to your tool's MCP config. See `AGENTS.md` → "Grounding against real library docs" |
| Building an app that CONTAINS AI and want real Claude recipes (evals, sub-agents, tool use, caching) | **`cookbook`** GitMCP source | Pinned in the kit's `.mcp.json` → `gitmcp.io/anthropics/claude-cookbooks`. Pull current Claude Cookbooks recipes during the `ai-feature-checklist` moments instead of guessing the SDK. Key recipe: `building_evals.ipynb` = the TDD answer for "is this on-brand?" |
| Want cheaper sessions (lower token cost) | **`docs/token-quick-wins.md`** | Six wins: Haiku routing, `/compact`, `/recap`, scope-bound prompts, caveman, prompt caching — with non-Claude fallbacks |

## Two habits that make all of this work
1. **Plan before you code.** If you catch yourself wanting to "just build it," run `/guide` or
   `idea-to-app` first — it stops you building the wrong thing or skipping a gate, and points you at
   the right next skill. Nothing gets built before a spec + plan are approved.
2. **Never break what already works.** For ANY change to existing code — fix, tweak, rename, remove —
   use `safe-change`, not a quick edit. It maps the impact, locks current behaviour in tests, makes
   the change on an isolated copy, runs the FULL suite, and gets a fresh-eyes review before anything
   merges. So changing one thing can't silently break another.
