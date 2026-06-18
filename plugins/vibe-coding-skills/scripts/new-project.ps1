<#
.SYNOPSIS
  Stamp out a NEW spec-driven project from this kit -- carrying the FULL toolbox
  (every custom skill, every script, the docs, the rules, and CI) -- or refresh an
  existing project with your latest skills.

.DESCRIPTION
  The kit is a template you reuse; each project you build is its OWN folder and its OWN
  git repo. Nothing is built inside the kit, and nothing merges back into it.

  Whole directories are copied recursively, so ANY skill or script you add to the kit
  LATER comes along automatically -- you never have to edit this script when you build
  a new skill.

.EXAMPLE
  .\scripts\new-project.ps1 -Name "My CRM"
  Creates C:\Projects\My CRM with the full kit, ready for its own GitHub repo.

.EXAMPLE
  .\scripts\new-project.ps1 -Name "My CRM" -Update
  Re-syncs the kit's latest skills + scripts INTO an existing project.
  Leaves the project's own specs, code, and docs untouched.
#>
param(
  [Parameter(Mandatory = $true)][string]$Name,
  [string]$ProjectsRoot = "C:\Projects",
  [switch]$Update
)

$ErrorActionPreference = 'Stop'
$template = Split-Path $PSScriptRoot -Parent       # this kit's root
$dest     = Join-Path $ProjectsRoot $Name

# --- What travels from the kit -------------------------------------------------------
# ALWAYS-SYNC: the living toolbox. Copied on create AND on -Update. Whole folders, so
# new skills/scripts you add to the kit later are picked up with no edits to this file.
$alwaysSyncDirs = @('.claude\skills', '.agents\skills', 'scripts')

# SEED-ONCE: a starting point for a new project; copied on create only, then it's yours.
$seedOnceDirs  = @('docs')
$seedOnceFiles = @(
  '.specify\memory\constitution.md',
  '.github\workflows\ci.yml',
  '.gitignore', '.env.example', 'ruff.toml', 'biome.json',
  'AGENTS.md', 'CLAUDE.md', 'SKILL-MAP.md'
)

# --- Copy helpers (merge contents; avoids the Copy-Item nested-folder gotcha) ---------
function Copy-Tree($rel, $destRoot) {
  $src = Join-Path $template $rel
  if (-not (Test-Path $src)) { return }
  $dst = Join-Path $destRoot $rel
  New-Item -ItemType Directory -Force -Path $dst | Out-Null
  Copy-Item -Path (Join-Path $src '*') -Destination $dst -Recurse -Force
}
function Copy-File($rel, $destRoot) {
  $src = Join-Path $template $rel
  if (-not (Test-Path $src)) { return }
  $dst = Join-Path $destRoot $rel
  New-Item -ItemType Directory -Force -Path (Split-Path $dst) | Out-Null
  Copy-Item -Path $src -Destination $dst -Force
}
function Remove-PyCaches($root) {
  Get-ChildItem -Path $root -Recurse -Directory -Filter '__pycache__' -ErrorAction SilentlyContinue |
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
}

# --- Refresh an existing project ------------------------------------------------------
if ($Update) {
  if (-not (Test-Path $dest)) { throw "No project found at: $dest  (drop -Update to create it)" }
  Write-Host "Refreshing the kit toolbox in: $dest" -ForegroundColor Cyan
  foreach ($d in $alwaysSyncDirs) { Copy-Tree $d $dest }
  Remove-PyCaches $dest
  Write-Host "Synced the latest skills (.claude + .agents) and scripts." -ForegroundColor Green
  Write-Host "Your specs, code, README, HANDOFF, and constitution were left untouched." -ForegroundColor Green
  return
}

# --- Create a brand-new project -------------------------------------------------------
if (Test-Path $dest) { throw "Folder already exists: $dest" }
New-Item -ItemType Directory -Path $dest | Out-Null

# Spec Kit init (Claude integration, PowerShell scripts)
$env:Path = "$env:USERPROFILE\.local\bin;$env:Path"
Push-Location $dest
specify init --here --integration claude --script ps --force
Pop-Location

# The full kit
foreach ($d in $alwaysSyncDirs + $seedOnceDirs) { Copy-Tree $d $dest }
foreach ($f in $seedOnceFiles) { Copy-File $f $dest }
Remove-PyCaches $dest

# Make the copied CLAUDE.md belong to THIS project, not the kit
$claude = Join-Path $dest 'CLAUDE.md'
if (Test-Path $claude) {
  $c = Get-Content $claude -Raw
  $c = $c -replace '(?m)^# Perfecting Coding Spec Kit\b.*$', "# $Name"
  $c = $c -replace 'specs/001-autopilot-orchestrator/plan\.md\s*\(Autopilot workflow orchestrator\)\.', 'the spec in `specs/` once you create one with `/speckit-specify`.'
  Set-Content -Path $claude -Value $c -Encoding UTF8
}

# Seed the AI-portable files this project's entry docs expect to exist
$today = (Get-Date -Format 'yyyy-MM-dd')
$handoff = Join-Path $dest 'HANDOFF.md'
if (-not (Test-Path $handoff)) {
@"
# $Name -- Handoff

> Read first. Holds what's built, what's next, and recent decisions.

## Current state
Fresh project stamped from Perfecting Coding Spec Kit on $today. Nothing built yet.

## Next step
Run ``/speckit-constitution`` (review the rules), then ``/goal`` to shape a fuzzy idea, then
``/speckit-specify`` to write the first spec. Lost? Run ``/guide``. New here? ``SKILL-MAP.md``
maps every skill to the moment you'd use it.
"@ | Set-Content -Path $handoff -Encoding UTF8
}
$readme = Join-Path $dest 'README.md'
if (-not (Test-Path $readme)) {
@"
# $Name

Built with the Perfecting Coding Spec Kit -- spec-driven, test-first, and AI-portable.
Start with **HANDOFF.md**, or just run ``/guide``.
"@ | Set-Content -Path $readme -Encoding UTF8
}

Write-Host ""
Write-Host "New project ready at: $dest" -ForegroundColor Green
Write-Host "It carries the FULL kit: all skills (.claude + .agents), scripts, docs, rules, and CI." -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Open Claude Code in that folder"
Write-Host "  2. /plugin install superpowers@claude-plugins-official  (if not already)"
Write-Host "  3. /speckit-constitution  ->  /goal (shape a fuzzy idea)  ->  /speckit-specify  ->  /speckit-plan"
Write-Host "  4. Give it its own GitHub repo (git init / first push)"
Write-Host ""
Write-Host "Later, to pull your newest kit skills into this project, run from the KIT folder:" -ForegroundColor Cyan
Write-Host "  .\scripts\new-project.ps1 -Name `"$Name`" -Update"
