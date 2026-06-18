# Design — Vibe Coding Kit as installable Claude Code plugins

**Date:** 2026-06-18
**Status:** approved (shape) — pending written-spec review before implementation plan
**Repo:** `kevvalmehta/vibe-coding-kit` (public)

## Goal

Stop hand-copying the Perfecting-Coding-Spec-Kit workspace into every new project.
Turn the reusable parts into Claude Code **plugins** installed once at user scope, so
the skills/commands/hooks are available in every project automatically.

## Platform (verified)

- Plugins, skills, and hooks run in **Claude Code** — the `claude` CLI **and** the
  desktop app's **"Code" tab**. Install once at user scope → available in every project.
- They do **not** run in the desktop app's **"Chat" tab** (no plugins/hooks/local scripts there).
- Source: official docs (code.claude.com/docs/en/plugins, plugin-marketplaces, desktop).

## Key facts that shaped the design (verified, not from memory)

1. **A plugin is copied to a cache when installed**, not run in place. Any script a
   skill/hook calls must be referenced with `${CLAUDE_PLUGIN_ROOT}` (expands to the
   plugin's cache dir), never a bare relative path like `scripts/foo.py`.
2. **One GitHub repo can be a marketplace** via `.claude-plugin/marketplace.json`
   (fields: `name`, `owner`, `plugins[]`). Each plugin entry needs `name` + `source`.
3. **A plugin** = `.claude-plugin/plugin.json` (manifest) + `skills/`, `commands/`,
   `hooks/hooks.json`, `scripts/`, etc. at the plugin root.
4. **Hooks in a plugin** live in `hooks/hooks.json` (same JSON schema as settings.json)
   or inline in `plugin.json`.
5. The two hooks differ in risk:
   - `tdd_guard.py` (PreToolUse `Edit|Write|MultiEdit`) **blocks** edits when no failing
     test exists → disruptive in non-code projects → must be opt-in.
   - `capture-lessons.ps1` (Stop) is **self-gating and safe**: it `return`s immediately
     unless `.specify/memory/lessons.md` exists in the project, is append-only, swallows
     all errors, and always `exit 0`. Confirmed in source:
     `if (-not (Test-Path $lessonsPath)) { return }  # opt-in: no Scar Log, no-op`.
     → safe to install globally; no-op in any project that hasn't run `/vibe-init`.

## Decisions

| # | Decision |
|---|----------|
| D1 | Target = Claude Code (CLI + desktop Code tab). |
| D2 | The `vibe-coding-kit` repo becomes the **marketplace** (add `.claude-plugin/marketplace.json`, put plugins under `plugins/`). |
| D3 | **Two plugins**, not one. |
| D4 | Per-project Spec Kit paperwork handled by **Option A**: plugin ships the master `.specify/` templates + constitution and a `/vibe-init` command stamps them into the current project. No hand-copying. |
| D5 | The **learning hook (`capture-lessons`) goes in the always-on plugin** (safe + self-gating). The **blocking `tdd_guard` goes in the opt-in plugin**. |

## Architecture

### Marketplace
`.claude-plugin/marketplace.json` at repo root lists two plugins under `plugins/`.

### Plugin A — `vibe-coding-skills` (always-on, safe, global)
```
plugins/vibe-coding-skills/
├── .claude-plugin/plugin.json
├── skills/                      # 13 custom + 15 speckit-* skills (see inventory)
├── scripts/                     # python/ps1 helpers the skills call
├── hooks/hooks.json             # Stop → capture-lessons.ps1 (self-gating, safe)
└── scaffold/                    # master .specify/ paperwork stamped by /vibe-init
```
- Ships every skill and `/speckit-*` command.
- Ships the **learning hook** (Stop) — fires everywhere, no-ops unless the project has
  `.specify/memory/lessons.md`.
- Ships `/vibe-init` (the scaffolder) + the master `.specify/` paperwork it copies in.
- **No blocking hook** → cannot jam any project.

### Plugin B — `vibe-tdd-hooks` (opt-in, code repos only)
```
plugins/vibe-tdd-hooks/
├── .claude-plugin/plugin.json
├── hooks/hooks.json             # PreToolUse Edit|Write|MultiEdit → tdd_guard.py
└── scripts/tdd_guard.py
```
- Install only in repos where TDD enforcement is wanted.

### Path-rewrite glue
Every script reference inside skills/hooks rewritten:
`scripts/foo.py` → `${CLAUDE_PLUGIN_ROOT}/scripts/foo.py`
(and `powershell ... scripts/capture-lessons.ps1` likewise). To be audited per file
during plan-writing.

### `/vibe-init` scaffolder (Option A)
A command skill in Plugin A. In a target project it copies
`${CLAUDE_PLUGIN_ROOT}/scaffold/.specify/` (constitution + templates + memory seed,
incl. an empty `lessons.md` so the learning hook activates) into the project. Creates
`specs/` on demand. Idempotent: never clobber an existing project's `.specify/` without
asking.

## Install + use (end state)
```
# once, ever:
/plugin marketplace add kevvalmehta/vibe-coding-kit
/plugin install vibe-coding-skills@vibe-coding-kit
# in code repos where TDD is wanted:
/plugin install vibe-tdd-hooks@vibe-coding-kit
# in each new project:
/vibe-init        # stamps in constitution + templates; activates learning hook
```

## Inventory (verified from the clone, 2026-06-18)

**Custom skills (13):** agent-architect, audit, autopilot, git-safety, goal, grill-me,
grill-with-docs, guide, health, idea-to-app, prototype, safe-change, zoom-out.
**Spec Kit command skills (15):** speckit-agent-context-update, speckit-analyze,
speckit-checklist, speckit-clarify, speckit-constitution, speckit-git-commit,
speckit-git-feature, speckit-git-initialize, speckit-git-remote, speckit-git-validate,
speckit-implement, speckit-plan, speckit-specify, speckit-tasks, speckit-taskstoissues.
**Scripts (8):** autopilot_state.py, capture-lessons.ps1, check-plan.ps1,
check_inventory.py, lint-goal.py, new-project.ps1, save.ps1, tdd_guard.py.
**Hooks:** PreToolUse `tdd_guard.py`; Stop `capture-lessons.ps1`.

## Open items to verify during plan-writing (not yet line-verified)

1. Which skills reference which scripts, and the exact path strings to rewrite.
2. What `new-project.ps1` does — may already overlap with `/vibe-init`; reuse vs replace.
3. `tdd_guard.py`'s `.tdd-guard` marker file behavior (on/off switch) and whether the
   opt-in plugin needs to ship/handle it.
4. The `.agents/skills/` Codex mirror — does it ship in the plugin, or stay repo-only?
5. Whether the `/speckit-*` skills depend on `.specify/` existing (i.e., require `/vibe-init`
   first) and should say so.
6. PowerShell-only scripts (`.ps1`) → confirm the cross-platform story or mark Windows-only.

## Out of scope
- Cross-LLM (Codex/Cursor) plugin support — those tools can't run Claude Code plugins/hooks.
- Publishing to any third-party plugin registry.
- Changing the kit's actual skill logic — this is packaging only.
