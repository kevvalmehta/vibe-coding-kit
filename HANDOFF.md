# HANDOFF — Current State

_Last updated: 2026-07-05_

<!-- AUTOPILOT-STATE -->
**Autopilot — idle.** No feature in progress. Last completed: `002-token-quick-wins` (merged). Start a
new run with "use autopilot on <idea>" (default gate mode `stop-at-every-step`; `big-3`/`auto` opt-in).
<!-- /AUTOPILOT-STATE -->

## Built 2026-07-05 — Specs 024–028: the five gap-fillers (branch `023-design-craft` — NOT merged, owner reviews → PR → merge)
Five new skills closing the kit's gaps for non-website builds (from the 2026-07-05 full-kit gap
survey), all following the contract-before-work house pattern (a named file the owner approves,
then checkable steps, honest scope, plain English):
- **`/data-model`** (024) — the database design coach: entity interview → binding `DATA-MODEL.md`
  (JSON machine block, RLS sentence per user-owned table) BEFORE any table; additive-first
  migrations; backups route to production-readiness.
- **`/add-login`** (025) — the login coach: magic-links default, `AUTH-SPEC.md` contract, managed
  auth only, secrets in `.env`, RLS everywhere, mandatory wrong-user test via `/verify`.
- **`/wire-up`** (026) — the integrations coach: Stripe / transactional email / stack storage,
  `INTEGRATIONS.md` contract, test mode first always, webhook-signature verification mandatory,
  owner flips live keys at their own keyboard.
- **`/uptime`** (027) — the "is my site down?" coach: free checker (owner opens the account),
  `UPTIME.md` watch list + incident runbook, proves the test alert arrives before claiming setup.
- **`/cost-watch`** (028) — the bills coach: inventories billable services from `.env.example`,
  `COSTS.md` row per service, owner-at-keyboard cap-or-alert (AI keys get monthly usage limits),
  monthly 5-minute review.
Weave-ins: `/stack` hand-off (database → `/data-model`), `git-safety` going-public walk item 8
(post-live → offer `/uptime` + `/cost-watch`), `/start` stage-resource-map (4 rows), `/guide` map,
SKILL-MAP, README, QUICKSTART. Drafted by delegated agents against a shared style brief, reviewed
and integrated by the orchestrator, adversarially verified before landing.
**State:** registered everywhere; `check_inventory.py` green. **Next / owner actions:** review → PR → merge.

## Built 2026-07-05 — Spec 022 Skill Craft (branch `022-skill-craft` — MERGED via PR #33)
New skill `/skill-craft`: the skill-writing coach for creating new skills/plugins that get followed
the same way every run. Five steps: one job + one leading word; AI-triggered vs owner-triggered
invocation (description context cost, `disable-model-invocation`); tripwire descriptions
(front-loaded leading word, one quoted trigger per branch); short cores with checkable steps +
gates near the top; review against five failure modes (premature completion, duplication, sediment,
sprawl, no-ops) then the registration ritual. Routes to skill-creator (scaffolding/evals) and
`/quality-charter` (quality system) — writing craft only, no duplication. Adapts invocation-economics
/ leading-words / failure-modes ideas from mattpocock/skills `writing-great-skills` (MIT, credited
in-skill); merged with the kit's own conventions and quality-charter's laws.
**State:** registered in `SKILL-MAP.md` + `README.md` + `/guide` map + `QUICKSTART.md`;
`check_inventory.py` green. **Merged.**

## Built 2026-07-05 — Spec 023 Design Craft (branch `023-design-craft` — WORK IN PROGRESS, not yet reviewed/PR'd)
New skill `/design-craft`: the UI/frontend design coach — the missing craft layer for anything with a
screen. Forces a deliberate look BEFORE markup (stated reference/direction + a binding `DESIGN-SPEC.md`
contract: palette, real fonts, grid, named layout skeletons H1–H4/B1–B8/F1, ≤3-move motion budget),
applies real typographic + grid craft while building (taste rules, Swiss grid + Vignelli discipline,
mono register, premium motion patterns), then verifies: `scripts/devibe_scan.py` (deterministic tell
scan — AI purple, gradients, emoji icons, default fonts; exit code gates CI) + a scored 14-question
self-critique (≥12/14 to present, never present a failing page). Bans UNDECIDED defaults, never the
owner's choices — no house style imposed. Vendors the working core (~170KB) of three MIT bodies of
work (leonxlnx/taste-skill, JCarterJohnson/vibecoded-design-tells, ui-ux-pro-max design ingredients;
licenses in `references/licenses/`; the 1.5MB ui-ux CSV database was deliberately left out),
battle-tested in a real client website overhaul (speakr website-builder v0.2.0, where a first
render without these rules failed the owner's design gate and the redo that applied them passed).
It is quality-charter's contract-before-work pattern
(P2) applied to design. Woven in: `/ship` step 1 (route in when the work has a screen), `/scaffold`
hand-off, `/start` stage-resource-map, `/guide` map.
**State:** registered in `SKILL-MAP.md` + `README.md` (skill + `devibe_scan.py` script rows) +
`QUICKSTART.md` + `/guide`; `check_inventory.py` green. **Next / owner actions:** review → PR → merge.

## Built 2026-07-05 — Spec 020 Quality Charter (branch `020-quality-charter` — NOT merged, owner reviews → push → PR)
New skill `/quality-charter` + 5 references: the 8-pattern quality architecture extracted from three
real plugin overhauls (M1-M4 copy charter v0.4.0, M5-M6 taste-as-contract v0.2.0, blog-pipeline
quality gates). Patterns: numbered charter with failure provenance (P1), contract-before-work (P2),
pre-flight brief (P3), deterministic MUST-PASS validator scripts (P4), scored self-review gate (P5),
exemplar banks (P6), loud labelled failure — never fabrication (P7), READ/CAPTURE/RECONCILE/PROMOTE
learnings loop (P8). References: quality-architecture (the catalog + 3 cross-cutting laws),
charter-template, gates-and-validators, self-evolution-loop, project-seed (starter AGENTS.md for any
new project). Adversarially reviewed before landing: accuracy pass (all load-bearing claims verified
against the three source repos) + kit-fit pass (frontmatter/heading/jargon/routing findings fixed).
Second pass on the same branch added `references/working-method.md` (the 10 binding
session-behavior rules — how a good session works, for any project type, pasteable into any
AGENTS.md/CLAUDE.md) and completed the FULL weave-in: `/guide` map row, `/start` post-plan offer,
`/scaffold` opt-in quality-file seeding, `/ship` charter-gate exit condition, `/goal` charter-rules
contract line, `/audit` presence check, `/health` check-12 extension, `speckit-implement` charter
read, `agent-eval` rubric↔gate cross-link, `lessons.md` SUPERSEDED/[promoted:] conventions.
`INTEGRATION-TODO.md` deleted per its own rule (all items done).
**State:** registered in `SKILL-MAP.md` + `README.md`; `check_inventory.py` green; weave-in complete.
**Next / owner actions:** review the branch → push → PR → merge.

## Built 2026-07-04 — Spec 019 Feedback-Loop Hardening (branch `019-feedback-loop-hardening` — NOT merged, owner reviews → push → PR)
Mirrors PCK spec 019 into this plugin repo. Two sources reviewed 2026-07-04 (OpenAI "harness
engineering" post + the loss-function-development thread) found the kit's harness fundamentals solid
but its FEEDBACK LOOPS soft. Five doc/skill-only edits, no scripts:
1. **`agent-eval` — answer-key blinding** — any agent iterating on a fix against an eval set now sees
   the score + failed-case categories only, never the expected answers (a 28-item eval got memorized
   in one round when answers were visible; blinding forces a real fix instead).
2. **`/goal` — instruments rule + target mode** — every constraint must name the command/check that
   measures it (wall-clock, spend, test count) since an unmeasurable constraint is a vibe an agent
   can't tell it's violating; plus an optional "target mode" for optimization goals (a bar to descend
   toward, answer-key blinded per item 1).
3. **`/ship` — iteration log + entropy on stall** — every bug-fix attempt now logs hypothesis →
   expected failure mode → diagnostic result before/after running; a stalled attempt's next try must
   state a genuinely different hypothesis (same idea "but harder" is banned). All existing exits
   (3-attempt cap, no-progress stop, cheat-detection, budget) are unchanged.
4. **Scar Log graduation path** (`.specify/memory/lessons.md`) — a mechanically-checkable L-# scar
   should graduate into a hook/lint/CI check instead of staying prose-only; the prose entry stays for
   the why, with a line naming which check now enforces it.
5. **`/scaffold` — legibility line** — starter READMEs now advise structured logs (one event per
   line, plain words) so an AI debugging the app later can read what happened instead of guessing.
**State:** all five registered in `AGENTS.md` + `SKILL-MAP.md` (Principle VI); guard test
`tests/test_feedback_loop_hardening.py` (5 checks) green; full suite green. **Next / owner actions:**
review the branch → push → PR → merge.

## Built 2026-07-03 — Spec 018 Adopted Patterns (branch `018-adopted-patterns` — NOT merged, owner reviews → push → PR)
Mirrors PCK spec 018 into this plugin repo (stacked on `017-production-burn-guards`, same as source).
Four patterns adapted natively from mattpocock/skills (MIT) — never install, rebuild.
1. **`/pathfinder`** (new skill, `plugins/vibe-coding-skills/skills/pathfinder/SKILL.md`, adapted
   from his in-progress `wayfinder` draft) — for ideas too big and foggy to plan in one sitting: a
   local `pathfinder/map.md` (Notes, Decisions-so-far index, Fog) plus one-sharp-question tickets
   routed to existing skills; one ticket resolved per session; hands off to `/speckit-specify` when
   fog + open tickets are both empty.
2. **Merge-conflict rescue** (`git-safety`) — plain-English walkthrough of what a conflict is, the
   `<<<<<<<`/`=======`/`>>>>>>>` markers, `git merge --abort` as the safe escape hatch, and a rule
   never to resolve conflicts blind in migration/schema files (spec 017 gate territory).
3. **Two-axis review lens** (`/ship`) — review reports SPEC FIDELITY and STANDARDS separately, so a
   pass on one can't mask a failure on the other.
4. **domain-modeling named entry** (`SKILL-MAP.md`) — registers the discipline (challenge fuzzy
   terms, `CONTEXT.md` glossary, sparse ADRs) by name, home = `grill-with-docs`.
**State:** all four registered in `AGENTS.md` + `SKILL-MAP.md` + `README.md` (Principle VI); guard
test `tests/test_adopted_patterns.py` (6 checks) green; full suite green. **Next / owner actions:**
review the branch → push → PR → merge.

## Built 2026-07-02 — Spec 017 Production Burn Guards (branch `017-production-burn-guards` — NOT merged, owner reviews → push → PR)
Mirrors PCK spec 017 into this plugin repo.
- **Why:** Gemini deep-research flagged the "90-day solo-founder burn vectors" — leaked secrets,
  missing Row-Level Security, unthrottled endpoints, destructive database commands run by an agent,
  and spec/code drift after v1 — none of which the kit's existing gates caught mechanically.
- **What's built, in plain English:**
  1. **`preflight_gate.py`** — a mechanical pre-deploy scan (no AI) that checks for leaked
     secrets, database tables missing Row-Level Security (the setting that stops one user seeing
     another user's data), and API routes with no rate limit (a cap on how many times someone can
     hammer an endpoint).
  2. **`destructive_action_gate.py`** — pauses and asks for your OK before running a
     destructive command (like deleting a database table) or editing a database migration file.
  3. **`spec_drift_warn.py`** — a warning (never a block) when code changes but the spec
     doesn't, so the plan and the build don't quietly drift apart.
  4. **Five doc tweaks**: a "Running cost implications" section in the plan template (call out
     anything with a running per-usage cost before you approve the build); a lean-specs note in the
     spec template (~300 lines max); a rule in `agent-eval` that AI judges must use fixed labels
     (pass/fail/unsafe) instead of unreliable 1-10 scores; a `git-safety` update to run the preflight
     gate before every deploy and never use `--dangerously-skip-permissions`; and a dependency-pinning
     rule in `CLAUDE.md`/`AGENTS.md` (exact versions, `npm ci` not `npm install` in CI).
- **New CI job**: `preflight` (blocking) runs `preflight_gate.py --json` against the repo.
- **Note:** VCK's `.claude/settings.json` has no `permissions`/`hooks` blocks (hooks live in the
  plugin's `hooks/hooks.json` instead), so PCK's `permissions.deny` (G4) was not mirrored there —
  no equivalent settings surface exists in this repo to carry it.
- **State:** all three guards registered in `AGENTS.md` + `SKILL-MAP.md` + `README.md`
  (Principle VI); hooks wired in `plugins/vibe-coding-skills/hooks/hooks.json`. **Next / owner
  actions:** review the branch → push → PR → merge.

## What this is
Spec-driven development workspace. Tools: **GitHub Spec Kit** (planning) + **Superpowers** (safe building),
both inside Claude Code. Deploy via Vercel + Supabase.

## Built / Installed
- **uv 0.11.19** — Python tool manager (installed via pip).
- **GitHub Spec Kit** (`specify-cli 0.9.6`) — initialized here. Added `/speckit-*` skills (in `.claude/skills/`) + `.specify/` templates and PowerShell scripts.
- **git repo** initialized. Set your global git identity (`git config --global user.name` / `user.email`) before committing.
- **Constitution** written: `.specify/memory/constitution.md` — security + TDD + regression-safety rules.
- **Portable MD files** + `.gitignore` + `.env.example` + `docs/memory-snapshot/` created.
- **GitHub repo** (private): https://github.com/kevvalmehta/Perfecting-Coding-Spec-Kit — pushed, marked as a reusable template.
- **CI workflow** `.github/workflows/ci.yml` — auto-runs Semgrep security scan + ruff Python lint + tests on every push.
- **Python linter** `ruff` (2026-06-09) — `ruff.toml` at the kit root; CI `lint` job runs `ruff check .`
  (BLOCKING) on any project with `.py` files; skipped automatically otherwise. `new-project.ps1` copies
  `ruff.toml` into every new project. Catches real bugs (undefined names, unused imports, syntax errors)
  locally + keyless. Python counterpart of what fallow does for TS/JS — fallow itself deliberately NOT
  adopted (kit default stack is Python).
- **JS/TS linter + type check** Biome + `tsc` (2026-06-09) — `biome.json` at the kit root (lint only,
  recommended bug rules; formatter off); CI `lint-js` job runs `npx @biomejs/biome@2.4.16 lint .` (BLOCKING;
  version pin must match the `$schema` in `biome.json` — bump both together)
  on any project with `package.json`, plus `npx tsc --noEmit` on any project with `tsconfig.json`;
  both skipped automatically otherwise. `new-project.ps1` copies `biome.json` into every new project.
  TS/JS counterpart of ruff — kit now lints BOTH default stacks. fallow still optional/deferred
  (deeper health scan for large TS/JS codebases only).
- **Deploy CLIs** installed: Vercel + Supabase (login is manual, per project, when deploying).
- **Reusability**: `SETUP.md` + `scripts/new-project.ps1` — spin up new projects from this scaffold.
- **Superpowers** v5.1.0 — installed + enabled (brainstorm + TDD + isolated builds + two-stage review).
- **Multi-LLM**: Spec Kit integrations = `claude` + `codex`. `AGENTS.md` has a BOOTSTRAP CHECK so any
  other LLM self-prompts to install what it needs and must plan before writing code.
- **Guardrail skill** `idea-to-app` (`.claude/skills/idea-to-app`) — auto-triggers on ANY build idea
  and walks the full gated pipeline (intake→research→brainstorm→specify→clarify→plan→tasks→build→
  test/verify→security→push), refusing to skip steps. Cross-LLM via the AGENTS.md sequence.
- **Guardrail skill** `safe-change` (`.claude/skills/safe-change`) — auto-triggers on edit/fix/change
  requests; enforces regression-safe edits (locate callers→impact map→tests-first→isolate→surgical
  change→full test run→review→verify→security→push). Stops if an existing test breaks.
  On LARGE codebases it recommends installing Graphify (`uv tool install graphifyy`) to map edit
  impact via a real call graph before changing anything.
- **Guardrail skill** `git-safety` (`.claude/skills/git-safety`) — GitHub best practices: branch per
  change, commit+push save points, PR to main, safe revert/recovery, tag good versions, resume-session
  steps. Plain-English human guide in `GITHUB-GUIDE.md`; `scripts/save.ps1` = one-command backup.
- **Validation skill** `discover` (`.claude/skills/discover`) — the pre-spec reality check (Phase A + B
  shipped): grills the problem, pain-mines real users (Reddit + paid-tool reviews via an honest fetch
  ladder, never fabricates), scores the underserved gap (ODI), cuts V1, names first 10 users, finds a
  growth loop, and handles two-sided marketplaces (cold-start + minimum liquidity) → verdict in a
  `discovery/` note + a problem statement handed to `/speckit-specify`. Read-only; never builds.
  Method harvested from `vibe-check` (TexasBedouin, MIT), rebuilt native — repo NOT installed.
  Spec: `specs/006-discover/spec.md`.
- **AI-quality skill** `agent-eval` (`plugins/vibe-coding-skills/skills/agent-eval`) — makes evals
  runnable for apps that contain AI (checklist #14 + constitution **Principle VIII**). Scaffolds an
  eval set (`evals/<feature>/` with human-readable `config.yaml` + `cases.yaml` + `feature_adapter.py`)
  and **vendors** the runner (`eval_runner.py` + `judge-prompt.md`) into the project's `evals/` so the
  CI gate works without the plugin installed. Runs it for a plain-English pass/fail report; grading =
  code-based where exact (free) + cheap LLM-as-judge (Haiku, temp 0, prompt caching) for fuzzy output;
  passing = percentage bar + critical-cases tier + borderline re-run; fails loud (exit 2 = eval broke,
  never a false pass); cost estimate + hard cap. ONE tested runner (25 unit tests, judge mocked). **v1
  = Standard scope** (create + run + CI gate, build-time only). Later phases: #15 after-launch live
  monitoring and fuller trajectory evals. Spec/plan/tasks: `specs/007-agent-eval/`. Mirrored from
  Perfecting-Coding-Spec-Kit; came from the Google *New SDLC* whitepaper gap analysis.
- **Whitepaper gap docs** (Google's *New SDLC With Vibe Coding*, 2026): `docs/context-engineering.md`
  + `docs/agentic-engineering-primer.md` + checklist #14/#15 + constitution Principle VIII.
- **Planning skills (adopted from Matt Pocock, MIT — github.com/mattpocock/skills)** in `.claude/skills/`:
  `grill-me` (interrogate a plan one Q at a time), `grill-with-docs` (grill against existing code +
  a `CONTEXT.md` glossary / `docs/adr/` records), `zoom-out` (`/zoom-out`: plain map before editing),
  `prototype` (throwaway demo to feel out a design). Lightly adapted to our constitution; registered in
  `AGENTS.md` + `CLAUDE.md`. They sharpen the PLAN stage only — they never start the build.
- **Mentor skill** `guide` (`.claude/skills/guide`) + **`SKILL-MAP.md`** (repo root) — ask `/guide`
  anytime for "where am I, what's next, which skill?". It diagnoses the stage from HANDOFF/specs/git,
  routes intent to the right skill, and course-corrects if a step is skipped. Widened
  `idea-to-app` + `safe-change` triggers so correction fires on casual phrasings too. Registered in
  `AGENTS.md` + `CLAUDE.md`. (Background auto-nudge hook deliberately deferred.)
- **Health-score skill** `health` (`.claude/skills/health`, 2026-06-10) — `/health` gives ONE 0–100
  score across 12 checks (plan-before-code, tests pass, tests mean something, main green, secrets safe,
  inputs/RLS, simple+surgical, docs match, AI-portable, git reversible, CI gate, risks logged), starts
  at 100 and docks points with a plain-English ledger (what's wrong + how many points + which skill
  fixes it), ends with one "fix this first". Diagnostic-only, hands off like `/guide` — never edits.
  Bands: 85+ Healthy, 60–84 Watch, <60 At risk. Original concept inspired by EvoMap's "Vibe Risk"
  (12-dim score + deduction ledger) — concept only, ZERO EvoMap code/plugin/dependency (their `evolver`
  is GPL-3.0; nothing copied). Rest of EvoMap rejected as duplicate of Spec Kit / TDD / CI / autopilot /
  memory we already have. Registered in `AGENTS.md` + `SKILL-MAP.md` + `guide` skill map.
- **Learning hook** `scripts/capture-lessons.ps1` + project `.claude/settings.json` (Stop hook) —
  after every turn it scans the transcript for correction signals ("no, don't do that", "from now
  on", "revert", "you broke", "never/always…") and appends a **candidate lesson** to the bottom of
  `lessons.md` for you to promote into a real `L-#` entry or delete. Opt-in (no-op unless `lessons.md`
  exists), append-only, swallows all errors so it can never break a session. Per-session scan state in
  `.specify/memory/.lessons-state.json` (gitignored). Borrowed from ECC's "observe with a hook, not a
  probabilistic skill" idea. (PreCompact hook considered + deferred — marginal value.)
- **Skill `agent-architect`** (`.claude/skills/agent-architect/`, 2026-06-10) — Evolution B. For apps
  that CONTAIN AI, it proposes the agent design (orchestrator + focused subagents, model per agent
  with mechanical work → Haiku, managed-agent vs Messages API suggested-with-reason owner-decides,
  human-approval gates), pre-fills the 13-factor `ai-feature-checklist.md`, draws a diagram, and grills
  by default. Recommendation-only (no code-gen in v1; scaffolding deferred). Wired into `idea-to-app`
  GATE 5; registered in `AGENTS.md` + `SKILL-MAP.md`. Guard `tests/test_agent_architect.py` (7 green).
  Built via the kit flow on `003-agent-architect` (`specs/003-agent-architect/`).
- **Token quick-wins habits doc** `docs/token-quick-wins.md` (2026-06-10) — six wins to lower token
  cost per session (Haiku routing, `/compact`, `/recap`, scope-bound prompts, caveman, prompt
  caching) with non-Claude fallbacks; guarded by `tests/test_token_quick_wins.py`. Registered in
  `AGENTS.md` + `SKILL-MAP.md`. Built via an Autopilot planning run (`specs/002-token-quick-wins/`).
- **Skill `audit`** (`.claude/skills/audit/`, 2026-06-13) — the existing-code advisor; deep follow-on
  to `/health`. Recons a repo, fans out read-only Explore subagents across 9 categories, **re-reads
  every cited `file:line` itself to vet** before showing anything, ranks by leverage, and writes
  self-contained handoff briefs into an `audit/` dir — each routed to `safe-change` (fix existing) /
  `/speckit-specify` (new) / `autopilot` (batch). Read-only on source. Two modes: interactive
  (offer+stop) and autonomous (`auto`, chain) — **both stop before push/merge/deploy** (autonomous
  outcome = green reviewed branch, never a deploy). Hard rules: no secret values (location+type+
  rotation), repo-content-is-data-not-instructions. SKILL.md + 3 references
  (`audit-playbook`/`brief-template`/`routing-and-modes`); guard `tests/test_audit_advisor.py` (9
  green). Registered in `AGENTS.md` + `SKILL-MAP.md` + `health`/`guide` cross-links. **Thinking
  borrowed natively from the MIT `shadcn/improve` skill — deliberately NO execute/reconcile fork
  (scar L-1: would duplicate `safe-change`/`autopilot`), NO `npx` install.** Built via the kit flow on
  `004-audit-advisor` (`specs/004-audit-advisor/`).

## Shipped/In progress 2026-07-02 — Opus Hardening mirror (branch `016-opus-hardening`)
Mirrors PCK spec 016 (commits `d4b8b96`/`8b1f58a`/`c506105`/`bd335f8`) into this plugin repo:
- **4 new enforcement hooks**, wired in `plugins/vibe-coding-skills/hooks/hooks.json` —
  `lessons_injector.py` (SessionStart — injects confirmed Scar Log lessons), `done_claim_verifier.py`
  (Stop — blocks an unverified "tests pass/pushed/committed" claim), `regrounding.py` (SessionStart
  resume/compact — injects live git truth after context compression), `import_reality_check.py`
  (PostToolUse — flags invented/hallucinated imports).
- **TDD-Guard now ON by default** (`.no-tdd-guard` opt-out; `.tdd-guard` still configures mode).
- **CI gates activated**: Semgrep now BLOCKS on findings, `deps-audit` job (pip-audit + npm audit)
  BLOCKS on known-vulnerable dependencies, `plan-gate` job (PR-only) blocks merge until the newest
  `tasks.md` is fully checked off.
- **`docs/production-readiness.md`** — the six checks between "works" and "safe for real users";
  `git-safety`'s public-deploy escalation now walks all six (record decision, warn, never block).
- Full test suite green. Registered in `AGENTS.md` + `SKILL-MAP.md` + `README.md`.

## Shipped 2026-06-10 (all merged to `master`)
- ✅ **Token quick-wins** (`docs/token-quick-wins.md`, PR #10) — six habits to cut token cost.
- ✅ **Evolution B — Agent-Architect** (`.claude/skills/agent-architect/`, PR #11) — proposes agent
  designs for AI apps; recommendation-only (scaffolding deferred — see memory).
- ✅ **Autopilot v2** (PR #12) — opt-in gate modes (`big-3`/`auto`, default still stop-at-every-step),
  new-idea-mid-flight (finish-vs-park), pre-PR no-build-yet guard.

## Next — say ONE of these to resume (any chat / any AI tool)
The kit is set up; Autopilot + Agent-Architect live on `master`. Pick up by saying any of:

- **"use autopilot on <my idea>"** — drive a NEW feature through specify→clarify→plan→tasks→checks.
  Default stops at every step; add "in big-3 mode" or "in auto mode" to stop less often.
- **"design the agents for <my AI app idea>"** — run **agent-architect** for an app that contains AI
  (proposes agent count, model per agent, managed-vs-API, gates; grills the design).
- **Autopilot v2 (c) — `Workflow`-tool fan-out** — the one remaining deferred v2 item (optional
  token optimization for the parallel plan/pre-PR steps). EDITS the skill → runs through `safe-change`.

Older setup follow-ups (still optional): connect Supabase (RLS on every table) + Vercel when you first deploy.

## Removed (fresh start, 2026-06-06)
- TaskMaster engine (global npm `task-master-ai`) — uninstalled.
- `prd-taskmaster` skill — removed.
- Reason: both overlapped Spec Kit. One source of truth = Spec Kit.
- NOTE: `Arham-Sales` / `Final-Arham-Sales` still hold their own `.taskmaster` data; their TaskMaster
  is paused until reinstalled (`npm i -g task-master-ai`) if those projects need it again.

## Hard Rules (summary — full text in constitution)
Plan before code · TDD always · never break working code (isolated copy + regression tests)
· security first (validate inputs, secrets in env, RLS) · simple + surgical.

## Recent Decisions
- **2026-06-13:** **Added a pinned `cookbook` GitMCP source** to `.mcp.json` →
  `gitmcp.io/anthropics/claude-cookbooks`. Lets agents pull REAL Claude Cookbooks recipes
  (verified: `misc/building_evals.ipynb`, `multimodal/using_sub_agents.ipynb`, `tool_use/*`,
  `misc/prompt_caching.ipynb`) during the `ai-feature-checklist` moments instead of guessing the
  SDK. Kept the generic `gitmcp.io/docs` server for general library grounding. Registered in
  AGENTS.md + SKILL-MAP.md + `docs/ai-feature-checklist.md` (Principle VI). New `.mcp.json` servers
  connect on next Claude Code reload, not mid-session — restart to activate `cookbook` tools.
- **2026-06-10:** **Decided to evolve the kit in two directions** (map:
  `docs/superpowers/specs/2026-06-10-workflow-evolution-map-design.md`). **(A) Autopilot** —
  an orchestrator skill that chains the spec-kit steps with approval gates, fans out
  subagents for parallel planning + parallel verify/security checks, routes mechanical
  work to Haiku, and auto-updates HANDOFF.md (saves tokens via subagent context isolation).
  **(B) Agent-Architect** — turns the passive `docs/ai-feature-checklist.md` into an active
  skill that, given an AI-app idea, proposes its agent/subagent/managed-agent design.
  **Chose to build A FIRST** (compounds — speeds/cheapens every later build incl. B); B is
  deferred but fully documented in the map doc (with a "start B cold in a new chat" section).
  Rejected adopting **ruvnet/ruflo** as the harness (alpha; independent audit found fabricated
  security counts + broken MCP; violates Simple+Surgical and one-source-of-truth). Also logged
  6 zero-build token quick-wins (model routing to Haiku, `/compact`, `/recap`, scope-bound
  prompts, caveman, prompt caching). Branch: `feat/autopilot-orchestrator`.
- **2026-06-10 (build):** **Autopilot BUILT + test-driven** on `feat/autopilot-orchestrator`
  (pushed to GitHub; PR open; NOT merged). Full Spec Kit flow done (spec/plan/tasks under
  `specs/001-autopilot-orchestrator/`). Shipped: `scripts/autopilot_state.py` (deterministic
  resume helper, TDD — 9 pytest green, ruff clean), `.claude/skills/autopilot/` (SKILL.md +
  references gates.md/parallel-plan.md/prepr-checks.md), registered in AGENTS.md + SKILL-MAP.md +
  guide (portability). Security review: clean. Test-drive PASS for US1 (stop-every-step,
  ambiguous→ask, advance-on-go, clarify auto-skip, push refusal). **Pre-merge gate FAILS by
  design — 2 open items:** T016 live scenarios **D** (parallel competing plans) + **E** (combined
  verify/security report) not yet exercised, and T017 (the gate). **Next: run quickstart D + E
  live on a real planning task → check off T016/T017 → gate passes → merge the PR.** Deferred v2
  ideas: relaxed "big-3"/"auto" gate mode; "new idea while another feature is mid-flight" handling;
  optional `Workflow`-tool fan-out. Evolution **B (Agent-Architect)** still queued (see map doc).
- **2026-06-09:** **LLM portability is now a Hard Rule** — constitution **v1.4.0** adds Principle VI:
  nothing in the kit (or a project built with it) may depend on a single AI tool; a skill/guardrail/
  process change is NOT done until registered in `AGENTS.md` + `SKILL-MAP.md`. AGENTS.md gained a
  Portability-rule section telling non-Claude agents (Codex, Gemini, Cursor) to read + follow the
  plain-markdown `SKILL.md` files in `.claude/skills/` directly (no duplication into `.agents/` —
  one source of truth; scar L-1). Claude-only mechanisms must document a manual fallback (e.g.
  lessons hook -> append to lessons.md by hand). Also: promoted the lessons.md auto-capture scaffold
  (deleted 1 false-positive candidate) on `chore/lessons-scaffold`. Branch: `feat/llm-portability-rule`.
- **2026-06-09:** Reviewed **12-Factor Agents** (github.com/humanlayer/12-factor-agents, 19K stars,
  CC BY-SA) — principles for building AI-*powered* products (agents, chatbots, LLM features), not for
  AI-assisted coding. **Rejected adopting it wholesale** (different layer — our kit governs HOW we
  build; it governs WHAT we build when the product contains an LLM). **Adopted as a checklist:** new
  `docs/ai-feature-checklist.md` — plain-English 13-point checklist to walk during /speckit-specify +
  /speckit-plan whenever a project includes an AI feature, plugin, skill, or agent; grill-me can use it.
  Same doc explains **Claude Managed Agents** (Anthropic-hosted agent harness, beta) and when to choose
  it vs the plain Messages API for future agent builds. **Hard-wired (LLM-agnostic):** `idea-to-app`
  GATE 0 now has a mandatory "AI-inside check" with the checklist enforced at GATES 3 + 5 (Claude Code);
  AGENTS.md has the same rule as a pipeline paragraph for Codex/Gemini/Cursor/any agent; SKILL-MAP.md
  row added. Branch: `feat/12-factor-ai-checklist`.
- **2026-06-09:** Reviewed **ECC** (github.com/affaan-m/ECC) — a 211K-star, MIT, multi-harness agent
  optimization framework (64 agents, 261 skills, per-language rules, hooks). **Rejected switching to
  it** (wrong fit — built for technical power-users running many AI tools; 261 skills would overwhelm
  a non-technical solo owner and kill our "one source of truth" + plain-English mentor). **Stole one
  idea:** its auto-learning loop, but its key engineering lesson — *observe with a hook (100% reliable),
  not a skill (~50-80%)*. Built the **learning hook** (see Built/Installed). Rejected the rest of ECC
  (its 261 skills, per-language rule dirs, AgentShield — we already gate with Semgrep, multi-harness
  adapters — already covered by AGENTS.md). Done on branch `feat/lessons-capture-hook`.
- **2026-06-09:** Borrowed 2 patterns from `mvanhorn/last30days-skill` (MIT). (a) **Scar log** —
  new `.specify/memory/lessons.md`: rules earn teeth from a real past mistake + a self-check the agent
  runs before "done"; wired into constitution Governance + AGENTS cold-start. Seeded with 1 real scar
  (TaskMaster duplication). (b) **Plan↔build seam** — new `scripts/check-plan.ps1` (lint = is the plan
  measurable; `-Gate` = did the build match it: fails on unchecked tasks / vague Independent Tests).
  Wired into tasks-template + constitution Quality Gate 1. Constitution now **v1.3.0**. Rejected: the
  full last30days engine, multi-source search, HTML briefs — wrong layer for a spec kit. Not yet committed.
- **2026-06-08:** Added a **mentor/router layer**: new `guide` skill (`/guide`) + root `SKILL-MAP.md`,
  plus widened `idea-to-app` / `safe-change` trigger wording so course-correction fires on casual
  phrasings ("let's build the X", "make the button bigger"). Chose **on-demand guide + reliable
  auto-triggers** over a background settings hook (safer for a non-technical solo owner; hook
  deferred until proven necessary). Done on branch `feat/guide-mentor-skill`.
- **2026-06-08:** Adopted **3 workflow upgrades** from Kun Chen's video (ex-Meta L8, "40 PRs/day";
  youtu.be/88B6DimMD2g): (1) measurable **"Done when"** criteria per task in the tasks template;
  (2) **fresh-context review** + **risk rating + visual proof** on every change — added to the
  constitution (now **v1.1.0**, Quality Gate 6 + Principle III) + `idea-to-app` GATE 8 + `AGENTS.md`;
  (3) **"turn manual checks into agent test instructions"** (end-to-end + screenshots) in `AGENTS.md`.
  Rejected his custom tools (Lavish, Treehouse, No Mistakes) and the "stop reviewing / 20-30 parallel
  agents" scale — wrong for a non-technical solo owner. Done on branch `feat/workflow-insights-from-video`.
- **2026-06-08:** Reviewed **iii** (github.com/iii-hq/iii) — a Rust backend orchestration engine.
  **R