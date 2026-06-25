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
 → /discover               is it worth building? pain-mine real users, score the gap, cut V1, name first 10 users
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
| New / "just guide me through building" | **`/start`** (the Conductor) | The proactive front-door mentor: greets you, asks what you want, and DRIVES the whole journey in plain English — routing to the right skill at each step (drives `idea-to-app` + `guide`, weaves in discover / grill-me / research-scout / loop-design / a light stack suggestion), checkpoint at every stage, opt-in "just run it" bypass. Never pushes/merges/deploys. Greets once per project automatically |
| Lost / "what do I do now?" | **`/guide`** | Tells you your stage + the exact next skill (the Conductor calls this under the hood) |
| "What shape is this in? / safe to ship?" | **`/health`** | One 0–100 score across 12 checks + a plain-English ledger of what cost points and how to fix it |
| "What's actually worth fixing?" (existing code, deep) | **`/audit`** | Reads the repo, finds + verifies the highest-leverage issues across 9 categories, writes ready-to-run briefs routed to `safe-change`/`/speckit-specify`/`autopilot`. The deep follow-on to `/health`. Read-only; stops before push/merge/deploy |
| Want the whole planning flow run for you | **`autopilot`** | Runs specify→clarify→plan→tasks→checks, stops for "go" each step; never pushes/merges |
| Have a plan — want the whole BUILD run for you | **`/ship`** (build auto-chaining, Conductor v4) | The post-plan counterpart of autopilot: drives build (tests first) → `/verify` → a safe bug-fix loop → `/security-review`, ending at a green, reviewed branch. The fix loop carries anti-cheat guardrails (test files read-only, every fix diff-checked) + a multi-exit STOP (3 attempts / no-progress / cheat-detected) so it can't loop forever or fake a pass. Refuses to build with no plan; checkpoints + "just run it" bypass; never pushes/merges/deploys. `/start` build stage routes into it |
| Your ask is vague / you want guardrails up front | **`/goal`** | Turns it into a task contract: outcome + concrete verification + what-not-to-touch + when-to-stop-and-ask; then routes you to `/speckit-specify` (or runs as-is if tiny) |
| Starting any new idea (even vague) | **`idea-to-app`** | Walks intake → … → ship, won't let you skip a step |
| Have an idea — is it worth building? | **`/discover`** | Pain-mines real users (Reddit + paid-tool reviews), scores which need is most underserved (ODI), cuts V1, names your first 10 users → grounded problem statement for `/speckit-specify`. Runs before the spec; read-only. Never fabricates evidence |
| Pinning down a fuzzy plan | **`grill-me`** | Interviews you one question at a time until it's solid (offers `research-scout` with your consent when evidence beats a guess) |
| "How do others BUILD this? what stack/pattern fits?" | **`/research-scout`** | The third research lane: gathers REAL, CITED evidence (papers, repos, docs, blogs, Reddit) → a `research/<topic>.md` note + plain-English summary. Standalone or consent-offered by grill-me/plan/conductor. Quick default + hard ceiling; advises when deeper is worth it; never fabricates a source. Distinct from `/discover` (problem) + GitMCP (library APIs) |
| Same, but extending existing code | **`grill-with-docs`** | Grills against your real code + decisions |
| Unsure how a piece of code fits | **`/zoom-out`** | Plain-English map before you touch it |
| Want to try a design before committing | **`prototype`** | Throwaway demo to feel it out, then deleted |
| Writing what the app should do | **`/speckit-specify`** | Creates the spec |
| Spec feels unclear | **`/speckit-clarify`** | Targeted questions, answers folded back in |
| Deciding the architecture | **`/speckit-plan`** | The "how" |
| "What should I build it with?" / which stack | **`/stack`** (the stack-decider, Conductor v3) | Recommends the matching "boring, proven" stack (language/framework/database/hosting) per project type, asks your priority once (budget/scale/simplicity/speed) then shows tiered, cost-labelled options (free + pay-for-better) + the trigger that makes each default wrong. Honors your own tool choice; escape hatch for exotic builds. Encodes the Streamlit→Streamlit-Cloud-not-Vercel fix. `/start` stage 4 routes in. Recommendation-only — never scaffolds/deploys (scaffolding = v7) |
| Breaking work into steps | **`/speckit-tasks`** | Small testable tasks |
| Changing / fixing / editing existing code | **`safe-change`** | Impact map → tests → isolate → review |
| "Did I over-build what I just changed?" | **`/lean-review`** | Looks only at your current changes, lists what to cut (dead code, reinvented built-ins, single-use abstractions) + the simpler replacement. The fast, narrow follow-on to `/audit`. Read-only |
| "What shortcuts did we take on purpose?" | **`/lean-debt`** | Harvests every `shortcut:` comment into a ledger (what was simplified, when it stops being OK, when to revisit); flags shortcuts with no revisit plan. Read-only |
| Enforce "tests first" mechanically during a build | **TDD-Guard** | A safety hook that, during a build, won't let new code be written until a failing test exists for it. Off by default; switched on with a `.tdd-guard` file. Enforces the "tests first" rule mechanically. (Not a skill you run — it runs itself.) |
| Get reminded to set up Claude Code automations on a new project | **Recommender-nudge** | A SessionStart hook (`recommender_nudge.py`) that, the first time you open a real project (or when its dependencies change), adds a one-line offer to run the `claude-code-setup` recommender — then drops a marker and stays quiet. Only OFFERS; never runs it for you, never blocks. (Not a skill you run — it runs itself.) |
| Check (portably) which MCP servers + plugins are set up | **availability-prober** (Conductor v6) | `python scripts/availability_probe.py` reads `.mcp.json` + `.claude/settings.json` and reports which MCP servers + plugins (gitmcp, cookbook, the recommender) are CONFIGURED. The portable, cross-tool complement to `/start`'s in-session tool-list check; states "configured ≠ live". (Not a skill — a helper you/the Conductor can run.) |
| Stuck on a bug | **`systematic-debugging`** | Find the root cause before fixing |
| Anything git (save, undo, branch, PR, "it broke") | **`git-safety`** | Keeps `main` working; every change reversible |
| Confirming a change works | **`/verify`** | Real behavior + a screenshot, not just "tests exist" |
| Checking security before shipping | **`/security-review`** | Inputs validated, no secrets, database locked down |
| Your app CONTAINS AI (chatbot, agent, LLM feature, plugin/skill) | **`docs/ai-feature-checklist.md`** | 13 decisions to make in the spec + plan (12-Factor Agents); also: Managed Agents vs plain API; PLUS #14 Evals (score fuzzy AI output) + #15 Watch-after-launch (AgentOps) from Google's *New SDLC* whitepaper |
| Deciding what the AI sees each turn (AI-inside apps) | **`docs/context-engineering.md`** | The 6 context types, static vs dynamic, progressive disclosure, "review context boundaries in the PR." Use at `/speckit-plan`. Most AI mistakes are "it saw the wrong stuff" mistakes |
| Want the big-picture mental model of AI-era building | **`docs/agentic-engineering-primer.md`** | Plain-English tour of the *New SDLC* whitepaper ideas not covered elsewhere: the vibe→structured→agentic spectrum (pick your rigor), the 80% problem, conductor vs orchestrator, the cost curve + model routing, MCP/A2A. Read once for the model |
| Designing the AGENTS for an AI app (how many, which model, managed vs API) | **`agent-architect`** | Proposes the agent design + pre-filled checklist + diagram; suggests managed-vs-API (you decide); grills by default. Recommendation-only |
| Proving an AI feature's output is good (and stays good) | **`/agent-eval`** | Scaffolds an eval set (cases + rubric + passing bar), runs it for a plain-English pass/fail report, and wires an automatic CI gate so a change that makes the AI worse is blocked. Code-based grading where exact, cheap LLM-as-judge for fuzzy output; fails loud, cost-capped. Implements checklist #14 + constitution Principle VIII. v1 = build-time evals; live after-launch monitoring is a later phase |
| Worried the AI is guessing a library's API / functions | **GitMCP** (`gitmcp.io`) | Optional MCP connector — points the AI at a repo's REAL current docs + code so it grounds answers instead of hallucinating. Add `https://gitmcp.io/{owner}/{repo}` (pinned) or `gitmcp.io/docs` (any repo) to your tool's MCP config. See `AGENTS.md` → "Grounding against real library docs" |
| Building an app that CONTAINS AI and want real Claude recipes (evals, sub-agents, tool use, caching) | **`cookbook`** GitMCP source | Pinned in the kit's `.mcp.json` → `gitmcp.io/anthropics/claude-cookbooks`. Pull current Claude Cookbooks recipes during the `ai-feature-checklist` moments instead of guessing the SDK. Key recipe: `building_evals.ipynb` = the TDD answer for "is this on-brand?" |
| Want cheaper sessions (lower token cost) | **`docs/token-quick-wins.md`** | Six wins: Haiku routing, `/compact`, `/recap`, scope-bound prompts, caveman, prompt caching — with non-Claude fallbacks |
| Want a second opinion on which Claude Code automations to set up (hooks, MCP, sub-agents) | **`claude-code-setup`** (Anthropic plugin) | Read-only setup recommender. **You trigger it** — ask *"recommend automations for this project"* or *"what hooks should I use?"* — and it scans the repo once and suggests the top hooks, MCP servers, skills, sub-agents, and slash commands. It never auto-runs and never edits anything — though a SessionStart hook (**Recommender-nudge**, above) now proactively OFFERS it once per project. Bundled with this repo (offered when a cloner trusts the folder; Claude-Code-only, so other AI tools just ignore it). A **run-once advisor** — overlaps `/guide` + `/health` + `/audit` for everything except suggesting harness wiring (hooks + MCP). Use it once, keep the good ideas, no need to leave it on |

## Two habits that make all of this work
1. **Plan before you code.** If you catch yourself wanting to "just build it," run `/guide` or
   `idea-to-app` first — it stops you building the wrong thing or skipping a gate, and points you at
   the right next skill. Nothing gets built before a spec + plan are approved.
2. **Never break what already works.** For ANY change to existing code — fix, tweak, rename, remove —
   use `safe-change`, not a quick edit. It maps the impact, locks current behaviour in tests, makes
   the change on an isolated copy, runs the FULL suite, and gets a fresh-eyes review before anything
   merges. So changing one thing can't silently break another.
