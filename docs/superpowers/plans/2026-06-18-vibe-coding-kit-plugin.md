# Vibe Coding Kit Plugin Packaging — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the vibe-coding-kit repo into a Claude Code marketplace hosting two plugins, so the kit installs once (user scope) and is available in every project — no more hand-copying.

**Architecture:** The repo root becomes a marketplace (`.claude-plugin/marketplace.json`). Reusable content **moves** into `plugins/` (single source of truth, no drift): `vibe-coding-skills` (all skills + commands + helper scripts + the self-gating learning hook + a `/vibe-init` scaffolder + a `scaffold/.specify` master copy) and `vibe-tdd-hooks` (only the blocking `tdd_guard` PreToolUse hook). Docs, the `.agents/` Codex mirror, and `specs/` history stay at root.

**Tech Stack:** Claude Code plugins/marketplaces; JSON manifests; existing Python + PowerShell scripts (Windows-targeted); `${CLAUDE_PLUGIN_ROOT}` for portable script paths.

---

## Verified facts this plan relies on

- **Plugin manifest** `.claude-plugin/plugin.json`: only `name` required; `version`/`description`/`author` optional. Omitting `version` → Claude Code uses the git SHA.
- **Marketplace** `.claude-plugin/marketplace.json`: requires `name`, `owner{name}`, `plugins[]`; each plugin entry needs `name` + `source` (relative path like `./plugins/x` is valid).
- **Plugin commands**: a flat `commands/<name>.md` → `/<name>` (frontmatter `description` required). Plugin skills under `skills/<name>/SKILL.md` are **namespaced**: `/vibe-coding-skills:<name>`.
- **Plugin hooks**: `hooks/hooks.json`, same schema as `settings.json`; reference bundled scripts with `"${CLAUDE_PLUGIN_ROOT}"/scripts/...` (quoted for shell).
- **Scripts to rewrite** (relative `scripts/...` → `${CLAUDE_PLUGIN_ROOT}/scripts/...`): `.claude/skills/autopilot/SKILL.md:53`, `.claude/skills/git-safety/SKILL.md:24`, `.claude/skills/goal/SKILL.md:134`, plus the two hook commands.
- **Do NOT rewrite** the `.specify/scripts/...` references in `speckit-*` skills — they correctly target the *project's* `.specify/` (stamped by `/vibe-init`).
- **`tdd_guard.py` is internally plugin-safe**: it resolves the `.tdd-guard` marker and the test `cwd` from the hook payload's `cwd` (the project), not the script location. `.tdd-guard` absent → exit 0 (edit allowed). Marker is the per-repo on-switch.
- **`capture-lessons.ps1` is internally plugin-safe + self-gating**: resolves `lessons.md` from the hook payload `cwd`; no-op unless `.specify/memory/lessons.md` exists; swallows errors; always exit 0.
- **`/vibe-init` must copy the whole `.specify/` tree** (templates + `scripts/powershell` + `memory/constitution.md` + `extensions` + json config), because `speckit-*` skills call `.specify/scripts/powershell/*.ps1`. This also removes the external `specify` CLI dependency that `new-project.ps1:86` currently uses.
- **Windows-only limitation (accepted, not solved here)**: `capture-lessons.ps1`, `save.ps1`, `check-plan.ps1`, `new-project.ps1`, `vibe-init.ps1`, and `.specify/scripts/powershell/*` are PowerShell with no bash twin. The kit targets the user's Windows environment.

## Repo restructure decision (confirm at review)

Reusable content is **moved** (not copied) into `plugins/`. After this plan the repo's top-level `.claude/skills/`, `.claude/settings.json`, root `scripts/`, and root `.specify/` are removed; their canonical homes are inside `plugins/`. To develop the kit itself you install its own plugin (dogfood). If you'd rather keep a working top-level copy too (at the cost of drift), say so and Task 1/2 change from `git mv` to copy.

## Target layout

```
vibe-coding-kit/
├── .claude-plugin/marketplace.json
├── plugins/
│   ├── vibe-coding-skills/
│   │   ├── .claude-plugin/plugin.json
│   │   ├── skills/                 # 28 skill dirs (moved from .claude/skills/)
│   │   ├── commands/vibe-init.md
│   │   ├── scripts/                # all helpers EXCEPT tdd_guard.py + vibe-init.ps1
│   │   ├── hooks/hooks.json        # Stop → capture-lessons
│   │   └── scaffold/.specify/      # master Spec Kit tree (moved from root .specify/)
│   └── vibe-tdd-hooks/
│       ├── .claude-plugin/plugin.json
│       ├── hooks/hooks.json        # PreToolUse → tdd_guard
│       └── scripts/tdd_guard.py
├── .agents/skills/                 # Codex mirror — stays
├── specs/  audit/  docs/           # history/docs — stay
├── README.md CLAUDE.md AGENTS.md HANDOFF.md  # docs — stay (updated in Task 8)
└── (root .claude/, root scripts/, root .specify/ removed)
```

---

## Task 1: Marketplace skeleton + branch hygiene

**Files:**
- Create: `.claude-plugin/marketplace.json`
- Create: `plugins/vibe-coding-skills/` `plugins/vibe-tdd-hooks/` (dirs)

- [ ] **Step 1: Confirm on the work branch**

Run: `cd /c/Projects/vibe-coding-kit && git status -sb`
Expected: `## feat/plugin-packaging...`. If not, `git checkout feat/plugin-packaging`.

- [ ] **Step 2: Create plugin directories**

Run: `mkdir -p plugins/vibe-coding-skills/.claude-plugin plugins/vibe-coding-skills/commands plugins/vibe-coding-skills/hooks plugins/vibe-tdd-hooks/.claude-plugin plugins/vibe-tdd-hooks/hooks plugins/vibe-tdd-hooks/scripts .claude-plugin`

- [ ] **Step 3: Write the marketplace manifest**

`.claude-plugin/marketplace.json`:
```json
{
  "name": "vibe-coding-kit",
  "owner": { "name": "kevvalmehta" },
  "description": "Plain English -> spec -> plan -> tested build. Spec Kit + Superpowers coding workspace, as installable plugins.",
  "plugins": [
    {
      "name": "vibe-coding-skills",
      "source": "./plugins/vibe-coding-skills",
      "description": "All workflow skills + /speckit-* commands + /vibe-init scaffolder + the self-gating learning hook. Safe to install globally."
    },
    {
      "name": "vibe-tdd-hooks",
      "source": "./plugins/vibe-tdd-hooks",
      "description": "Opt-in TDD-Guard: blocks Edit/Write unless a failing test exists. Install only in code repos; enable per-repo with a .tdd-guard marker."
    }
  ]
}
```

- [ ] **Step 4: Validate JSON**

Run: `python -c "import json;json.load(open('.claude-plugin/marketplace.json'));print('ok')"`
Expected: `ok`

- [ ] **Step 5: Commit**

```bash
git add .claude-plugin/marketplace.json
git commit -m "feat(plugin): add marketplace manifest + plugin dirs"
```

---

## Task 2: Move skills, scripts, and the Spec Kit scaffold into vibe-coding-skills

**Files:**
- Move: `.claude/skills/` → `plugins/vibe-coding-skills/skills/`
- Move: all of root `scripts/` except `tdd_guard.py` → `plugins/vibe-coding-skills/scripts/`
- Move: root `.specify/` → `plugins/vibe-coding-skills/scaffold/.specify/`

- [ ] **Step 1: Move the skills tree (preserve git history)**

Run: `git mv .claude/skills plugins/vibe-coding-skills/skills`

- [ ] **Step 2: Move helper scripts (all except tdd_guard.py)**

```bash
for f in autopilot_state.py capture-lessons.ps1 check-plan.ps1 check_inventory.py lint-goal.py new-project.ps1 save.ps1; do
  git mv "scripts/$f" "plugins/vibe-coding-skills/scripts/$f"
done
```

- [ ] **Step 3: Move the Spec Kit tree into the plugin's scaffold/**

Run: `mkdir -p plugins/vibe-coding-skills/scaffold && git mv .specify plugins/vibe-coding-skills/scaffold/.specify`

- [ ] **Step 4: Verify the moves**

Run: `ls plugins/vibe-coding-skills/skills | wc -l` → Expected: `28`
Run: `ls plugins/vibe-coding-skills/scripts` → Expected: 7 files, NO `tdd_guard.py`
Run: `ls plugins/vibe-coding-skills/scaffold/.specify` → Expected: `templates extensions memory scripts ...`
Run: `git status -s | grep -c '^R'` → Expected: a positive number (renames tracked)

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "feat(plugin): move skills, helper scripts, and .specify scaffold into vibe-coding-skills"
```

---

## Task 3: Rewrite kit-script paths in moved skills to ${CLAUDE_PLUGIN_ROOT}

**Files:**
- Modify: `plugins/vibe-coding-skills/skills/autopilot/SKILL.md` (the `python scripts/autopilot_state.py` line)
- Modify: `plugins/vibe-coding-skills/skills/git-safety/SKILL.md` (the `scripts/save.ps1 ...` line)
- Modify: `plugins/vibe-coding-skills/skills/goal/SKILL.md` (the `python3 scripts/lint-goal.py goal.txt` line)

- [ ] **Step 1: Find the exact current strings**

Run: `grep -rn 'scripts/autopilot_state.py\|scripts/save.ps1\|scripts/lint-goal.py' plugins/vibe-coding-skills/skills`
Expected: 3 hits (autopilot, git-safety, goal). Note exact surrounding text per file.

- [ ] **Step 2: Rewrite autopilot**

In `skills/autopilot/SKILL.md`, replace `python scripts/autopilot_state.py`
with `python "${CLAUDE_PLUGIN_ROOT}/scripts/autopilot_state.py"`.

- [ ] **Step 3: Rewrite git-safety**

In `skills/git-safety/SKILL.md`, replace `scripts/save.ps1 -Message`
with `"${CLAUDE_PLUGIN_ROOT}/scripts/save.ps1" -Message`.

- [ ] **Step 4: Rewrite goal**

In `skills/goal/SKILL.md`, replace `python3 scripts/lint-goal.py goal.txt`
with `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/lint-goal.py" goal.txt`.

- [ ] **Step 5: Confirm no bare kit-script refs remain (but .specify refs untouched)**

Run: `grep -rn 'scripts/autopilot_state.py\|scripts/save.ps1\|scripts/lint-goal.py' plugins/vibe-coding-skills/skills | grep -v 'CLAUDE_PLUGIN_ROOT'`
Expected: no output.
Run: `grep -rln '.specify/scripts/powershell' plugins/vibe-coding-skills/skills | wc -l`
Expected: still 7+ (speckit refs deliberately unchanged).

- [ ] **Step 6: Commit**

```bash
git add plugins/vibe-coding-skills/skills
git commit -m "fix(plugin): point kit-script refs at \${CLAUDE_PLUGIN_ROOT}"
```

---

## Task 4: vibe-coding-skills manifest + learning hook

**Files:**
- Create: `plugins/vibe-coding-skills/.claude-plugin/plugin.json`
- Create: `plugins/vibe-coding-skills/hooks/hooks.json`

- [ ] **Step 1: Write the plugin manifest**

`plugins/vibe-coding-skills/.claude-plugin/plugin.json`:
```json
{
  "name": "vibe-coding-skills",
  "version": "0.1.0",
  "description": "Plain English -> spec -> plan -> tested build. All workflow skills, /speckit-* commands, /vibe-init scaffolder, and the self-gating learning hook.",
  "author": { "name": "kevvalmehta" }
}
```

- [ ] **Step 2: Write the learning hook (Stop), pointing at the bundled script**

`plugins/vibe-coding-skills/hooks/hooks.json`:
```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "powershell -NoProfile -ExecutionPolicy Bypass -File \"${CLAUDE_PLUGIN_ROOT}/scripts/capture-lessons.ps1\"",
            "timeout": 10,
            "statusMessage": "Capturing lessons..."
          }
        ]
      }
    ]
  }
}
```

- [ ] **Step 3: Validate both JSON files**

Run: `python -c "import json;json.load(open('plugins/vibe-coding-skills/.claude-plugin/plugin.json'));json.load(open('plugins/vibe-coding-skills/hooks/hooks.json'));print('ok')"`
Expected: `ok`

- [ ] **Step 4: Commit**

```bash
git add plugins/vibe-coding-skills/.claude-plugin plugins/vibe-coding-skills/hooks
git commit -m "feat(plugin): vibe-coding-skills manifest + learning hook"
```

---

## Task 5: /vibe-init scaffolder (command + copy script)

**Files:**
- Create: `plugins/vibe-coding-skills/scripts/vibe-init.ps1`
- Create: `plugins/vibe-coding-skills/commands/vibe-init.md`

- [ ] **Step 1: Write the idempotent copy script**

`plugins/vibe-coding-skills/scripts/vibe-init.ps1`:
```powershell
# vibe-init.ps1 -- stamp the Spec Kit paperwork into the current project.
# Copies the plugin's scaffold/.specify into ./.specify (never clobbering existing
# files), seeds an empty Scar Log so the learning hook activates, and ensures specs/.
[CmdletBinding()]
param(
    [string]$PluginRoot = $env:CLAUDE_PLUGIN_ROOT,
    [string]$Target = (Get-Location).Path
)
$ErrorActionPreference = 'Stop'
if (-not $PluginRoot) { Write-Error 'CLAUDE_PLUGIN_ROOT not set; run this via /vibe-init.'; exit 1 }

$src = Join-Path $PluginRoot 'scaffold\.specify'
if (-not (Test-Path $src)) { Write-Error "scaffold not found at $src"; exit 1 }
$dstSpecify = Join-Path $Target '.specify'

# robocopy /XC /XN /XO = copy only files that don't already exist (never overwrite).
robocopy $src $dstSpecify /E /XC /XN /XO /NFL /NDL /NJH /NJS /NP | Out-Null
if ($LASTEXITCODE -ge 8) { Write-Error "robocopy failed ($LASTEXITCODE)"; exit 1 }

$memory = Join-Path $dstSpecify 'memory'
if (-not (Test-Path $memory)) { New-Item -ItemType Directory -Path $memory | Out-Null }
$lessons = Join-Path $memory 'lessons.md'
if (-not (Test-Path $lessons)) {
    Set-Content -Path $lessons -Encoding UTF8 -Value "# Lessons (Scar Log)`n`nConfirmed lessons go here as L-# entries. The learning hook appends candidates below.`n"
}
$specs = Join-Path $Target 'specs'
if (-not (Test-Path $specs)) { New-Item -ItemType Directory -Path $specs | Out-Null }

Write-Host "vibe-init: Spec Kit paperwork ready in $dstSpecify (existing files left untouched)."
exit 0
```

- [ ] **Step 2: Write the command file**

`plugins/vibe-coding-skills/commands/vibe-init.md`:
```markdown
---
description: Stamp the Vibe Coding Kit Spec Kit paperwork (constitution, templates, scripts) into the current project and activate the learning hook.
---

Set up this project to use the Vibe Coding Kit workflow.

1. Run this command from the repo root (PowerShell):
   `powershell -NoProfile -ExecutionPolicy Bypass -File "${CLAUDE_PLUGIN_ROOT}/scripts/vibe-init.ps1"`
2. It copies the kit's `.specify/` (constitution + templates + scripts + extensions) into
   `./.specify` **without overwriting any file that already exists**, seeds an empty
   `.specify/memory/lessons.md` (which switches the learning hook on for this project),
   and creates `specs/`.
3. Report what landed. Then tell the user the next steps:
   `/vibe-coding-skills:speckit-constitution` -> `/vibe-coding-skills:goal` ->
   `/vibe-coding-skills:speckit-specify` -> `/vibe-coding-skills:speckit-plan`.
4. If they also want TDD enforcement, tell them to install `vibe-tdd-hooks` and create a
   `.tdd-guard` marker file in the repo root.
```

- [ ] **Step 3: Smoke-test the copy script against a temp target**

```bash
TMP=$(mktemp -d)
CLAUDE_PLUGIN_ROOT="$(pwd)/plugins/vibe-coding-skills" \
  powershell -NoProfile -ExecutionPolicy Bypass -File plugins/vibe-coding-skills/scripts/vibe-init.ps1 -Target "$TMP"
ls "$TMP/.specify" && ls "$TMP/.specify/memory/lessons.md" && ls -d "$TMP/specs"
```
Expected: `.specify` tree present, `lessons.md` exists, `specs/` exists. Then `rm -rf "$TMP"`.

- [ ] **Step 4: Idempotency check (run twice, no clobber)**

```bash
TMP=$(mktemp -d)
ROOT="$(pwd)/plugins/vibe-coding-skills"
CLAUDE_PLUGIN_ROOT="$ROOT" powershell -NoProfile -File plugins/vibe-coding-skills/scripts/vibe-init.ps1 -Target "$TMP"
echo "MINE" > "$TMP/.specify/memory/constitution.md"
CLAUDE_PLUGIN_ROOT="$ROOT" powershell -NoProfile -File plugins/vibe-coding-skills/scripts/vibe-init.ps1 -Target "$TMP"
cat "$TMP/.specify/memory/constitution.md"
```
Expected: prints `MINE` (second run did NOT overwrite). Then `rm -rf "$TMP"`.

- [ ] **Step 5: Commit**

```bash
git add plugins/vibe-coding-skills/commands plugins/vibe-coding-skills/scripts/vibe-init.ps1
git commit -m "feat(plugin): /vibe-init scaffolder (idempotent .specify stamp)"
```

---

## Task 6: Build vibe-tdd-hooks (the opt-in blocking plugin)

**Files:**
- Move: `scripts/tdd_guard.py` → `plugins/vibe-tdd-hooks/scripts/tdd_guard.py`
- Create: `plugins/vibe-tdd-hooks/.claude-plugin/plugin.json`
- Create: `plugins/vibe-tdd-hooks/hooks/hooks.json`

- [ ] **Step 1: Move tdd_guard.py**

Run: `git mv scripts/tdd_guard.py plugins/vibe-tdd-hooks/scripts/tdd_guard.py`

- [ ] **Step 2: Confirm root scripts/ is now empty and remove it**

Run: `ls scripts 2>/dev/null` → Expected: empty/no output. Then `rmdir scripts 2>/dev/null || true`.

- [ ] **Step 3: Write the manifest**

`plugins/vibe-tdd-hooks/.claude-plugin/plugin.json`:
```json
{
  "name": "vibe-tdd-hooks",
  "version": "0.1.0",
  "description": "TDD-Guard: blocks Edit/Write/MultiEdit unless a failing test exists. Opt-in per repo via a .tdd-guard marker file.",
  "author": { "name": "kevvalmehta" }
}
```

- [ ] **Step 4: Write the PreToolUse hook**

`plugins/vibe-tdd-hooks/hooks/hooks.json`:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "python \"${CLAUDE_PLUGIN_ROOT}/scripts/tdd_guard.py\"",
            "timeout": 60,
            "statusMessage": "TDD-Guard checking..."
          }
        ]
      }
    ]
  }
}
```

- [ ] **Step 5: Validate JSON + confirm tdd_guard reads marker from payload cwd (not script dir)**

Run: `python -c "import json;json.load(open('plugins/vibe-tdd-hooks/.claude-plugin/plugin.json'));json.load(open('plugins/vibe-tdd-hooks/hooks/hooks.json'));print('ok')"`
Expected: `ok`

Marker-off behavior (no `.tdd-guard` in target cwd → allow):
```bash
echo '{"tool_name":"Edit","cwd":"'"$(mktemp -d)"'"}' | python plugins/vibe-tdd-hooks/scripts/tdd_guard.py; echo "exit=$?"
```
Expected: no output, `exit=0` (edit allowed because no marker).

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "feat(plugin): vibe-tdd-hooks (opt-in TDD-Guard PreToolUse hook)"
```

---

## Task 7: End-to-end install verification from a local marketplace

**Files:** none (verification only)

- [ ] **Step 1: Remove the now-stale root hook wiring**

The old `.claude/settings.json` wired relative-path hooks for the *old* layout. With hooks now shipped by the plugins, delete it so it can't double-fire or error:
Run: `git rm .claude/settings.json && git commit -m "chore: drop root settings.json (hooks now ship in plugins)"`
(Confirm nothing else under `.claude/` is needed: `ls .claude` — if empty, `git rm -r .claude` is fine; otherwise leave the rest.)

- [ ] **Step 2: Add the marketplace from the local path**

In Claude Code (interactive), run: `/plugin marketplace add C:/Projects/vibe-coding-kit`
Expected: marketplace `vibe-coding-kit` added; lists 2 plugins.

- [ ] **Step 3: Install both plugins (local) and verify skills appear**

Run: `/plugin install vibe-coding-skills@vibe-coding-kit`
Then `/plugin install vibe-tdd-hooks@vibe-coding-kit`
Expected: both install. `/vibe-init` is offered; `/vibe-coding-skills:speckit-plan` (and the other speckit/skill commands) appear namespaced.

- [ ] **Step 4: Verify the learning hook fires + self-gates**

In a scratch project WITHOUT `.specify/memory/lessons.md`: complete a turn → no lessons file created (no-op). Run `/vibe-init` → `.specify/memory/lessons.md` created. Complete a turn that contains a correction phrase → a candidate appears appended to `lessons.md`.
Expected: no-op before `/vibe-init`, captures after.

- [ ] **Step 5: Verify TDD-Guard self-gates on the marker**

In the scratch project (vibe-tdd-hooks installed) with NO `.tdd-guard`: an Edit is allowed. Create `.tdd-guard` (contents `mode: strict`) and try editing a non-test file with no failing test → the edit is blocked with the deny message.
Expected: allowed without marker, blocked with marker.

- [ ] **Step 6: Clean up test install (optional)**

`/plugin uninstall ...` and `/plugin marketplace remove vibe-coding-kit` if you don't want the local copy registered (you'll re-add from GitHub in Task 8).

---

## Task 8: Update docs, push, open PR

**Files:**
- Modify: `README.md` (install instructions), `HANDOFF.md` (new layout)

- [ ] **Step 1: Add an "Install as a plugin" section to README.md**

Document the real end-state flow:
```markdown
## Install as a plugin (Claude Code: CLI or desktop Code tab)

    /plugin marketplace add kevvalmehta/vibe-coding-kit
    /plugin install vibe-coding-skills@vibe-coding-kit   # skills + /speckit-* + /vibe-init + learning hook (safe everywhere)
    /plugin install vibe-tdd-hooks@vibe-coding-kit        # optional: TDD enforcement, code repos only

In each new project: run `/vibe-init` to stamp in the constitution + templates and turn
on lesson capture. For TDD enforcement, create a `.tdd-guard` marker file in that repo.

Skills are namespaced: e.g. `/vibe-coding-skills:speckit-specify`.
```

- [ ] **Step 2: Update HANDOFF.md** to describe the marketplace/plugin layout and that hooks now ship in plugins (not root `settings.json`).

- [ ] **Step 3: Commit docs**

```bash
git add README.md HANDOFF.md
git commit -m "docs: plugin install instructions + new layout"
```

- [ ] **Step 4: Push and open the PR (noreply identity already on the branch)**

```bash
git push
gh pr create --repo kevvalmehta/vibe-coding-kit --base main --head feat/plugin-packaging \
  --title "Package the kit as Claude Code plugins" \
  --body "Two plugins (vibe-coding-skills + vibe-tdd-hooks) served from this repo as a marketplace. Install once, use in every project. See docs/superpowers/specs/2026-06-18-vibe-coding-kit-plugin-design.md."
```
Expected: PR URL printed.

- [ ] **Step 5: Final verify from GitHub (not local)**

After merge (or on the branch): `/plugin marketplace add kevvalmehta/vibe-coding-kit` on a clean machine/project → install → `/vibe-init` works.

---

## Self-review (done)

- **Spec coverage:** marketplace (D2 → T1), two-plugin split (D3 → T2/T4/T6), Option A `/vibe-init` (D4 → T5), learning hook in always-on plugin + tdd_guard opt-in (D5 → T4/T6), `${CLAUDE_PLUGIN_ROOT}` rewrites (T3 + hooks), whole-`.specify` scaffold (T2/T5), install/use flow (T7/T8). All covered.
- **Open items from the spec:** script refs (T3), `new-project.ps1` overlap (kept as-is, ships in scripts/; `/vibe-init` supersedes its `.specify` provisioning — noted), `.tdd-guard` marker (T6 verified), Codex mirror (stays root, not in plugin), speckit `.specify` dependency (T5 stamps whole tree), cross-platform (Windows-only, documented). All resolved.
- **Placeholders:** none — every step has exact paths, code, and a verification command.
- **Consistency:** plugin names (`vibe-coding-skills`, `vibe-tdd-hooks`) and `${CLAUDE_PLUGIN_ROOT}` usage match across marketplace.json, manifests, hooks, and skill rewrites.

## Out of scope
- Cross-platform (bash) equivalents for the PowerShell scripts.
- Publishing to a third-party registry.
- Any change to skill *logic* — packaging only.
