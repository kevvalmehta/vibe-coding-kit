<#
.SYNOPSIS
  Plan <-> build seam checker for Spec Kit.

  Plain English: the AI writes the plan (tasks.md). THIS SCRIPT - not the AI's word -
  checks two things:
    1. LINT  (default)  : is the plan specific enough to build from? Every user story
                          must carry a real, measurable "Independent Test" (a pass/fail
                          the build can self-check), and no template scaffolding left over.
    2. GATE  (-Gate)    : did the build actually match the plan? Fails if any task is
                          still unchecked or any placeholder text remains.

  Code does the checking, so "done" means done - the build cannot quietly drift from
  the plan the AI agreed to.

.PARAMETER TasksFile
  Path to a tasks.md. If omitted, auto-finds the most recently edited specs\*\tasks.md.

.PARAMETER Gate
  Pre-merge mode: also require every task checked [x] and zero placeholders.

.EXAMPLE
  powershell -File scripts\check-plan.ps1            # lint the latest plan
.EXAMPLE
  powershell -File scripts\check-plan.ps1 -Gate      # full pre-merge gate
.EXAMPLE
  powershell -File scripts\check-plan.ps1 -TasksFile specs\003-thing\tasks.md -Gate
#>
[CmdletBinding()]
param(
  [string]$TasksFile,
  [switch]$Gate
)

$ErrorActionPreference = 'Stop'
# Repo root: script-relative works in the dev repo (scripts/ at root) but not when this
# script ships nested inside a plugin — prefer the caller's cwd when it has a specs\ dir.
$repoRoot = Split-Path -Parent $PSScriptRoot
if (Test-Path (Join-Path (Get-Location).Path 'specs')) { $repoRoot = (Get-Location).Path }

function Say-Fail($m) { Write-Host "  [X]  $m" -ForegroundColor Red }
function Say-Pass($m) { Write-Host "  [OK] $m" -ForegroundColor Green }
function Say-Warn($m) { Write-Host "  [!]  $m" -ForegroundColor Yellow }

# --- 1. Locate the plan -----------------------------------------------------
if (-not $TasksFile) {
  $specsDir = Join-Path $repoRoot 'specs'
  $candidate = $null
  if (Test-Path $specsDir) {
    # "Most recent" by GIT commit time, not filesystem time: a fresh CI checkout stamps
    # every file with checkout time, which would make this pick a coin flip.
    $candidate = Get-ChildItem -Path $specsDir -Filter 'tasks.md' -Recurse -ErrorAction SilentlyContinue |
      Sort-Object {
        $ts = $null
        try { $ts = (git -C $repoRoot log -1 --format=%ct -- $_.FullName 2>$null | Select-Object -First 1) } catch {}
        if ($ts) { [long]$ts } else { [long](($_.LastWriteTime.ToUniversalTime() - [datetime]'1970-01-01').TotalSeconds) }
      } -Descending | Select-Object -First 1
  }
  if (-not $candidate) {
    Write-Host "No tasks.md found under specs\. Run /speckit-tasks first, then re-run this." -ForegroundColor Yellow
    exit 2
  }
  $TasksFile = $candidate.FullName
}
if (-not (Test-Path -LiteralPath $TasksFile)) {
  Write-Host "Plan file not found: $TasksFile" -ForegroundColor Red
  exit 2
}

$lines = Get-Content -LiteralPath $TasksFile
$rel = $TasksFile.Replace($repoRoot + '\', '')

Write-Host ""
$modeLabel = if ($Gate) { "GATE (pre-merge)" } else { "LINT (plan quality)" }
Write-Host "Checking plan: $rel   [$modeLabel]" -ForegroundColor Cyan
Write-Host ("=" * 64)

$problems = 0

# --- 2. Each user story has a measurable Independent Test -------------------
Write-Host ""
Write-Host "1. Each user story has a measurable 'Independent Test'"
$storyHeaders = @()
for ($i = 0; $i -lt $lines.Count; $i++) {
  if ($lines[$i] -match '^##\s+Phase.*User Story') { $storyHeaders += $i }
}
$vague = '(?i)\bworks?( correctly| as expected)?\b|\bas expected\b|\bis correct\b|\bproperly\b|\bfunctions?\b'
if ($storyHeaders.Count -eq 0) {
  Say-Warn "No user-story phases found (small/early plan?). Skipping this check."
} else {
  foreach ($h in $storyHeaders) {
    $title = ($lines[$h] -replace '^##\s+', '').Trim()
    $testText = $null
    $stop = [Math]::Min($h + 9, $lines.Count)
    for ($j = $h + 1; $j -lt $stop; $j++) {
      if ($lines[$j] -match '^\*\*Independent Test\*\*\s*:?\s*(.*)$') { $testText = $Matches[1].Trim(); break }
    }
    if ($null -eq $testText) {
      Say-Fail "$title  ->  no 'Independent Test:' line."; $problems++
    } elseif ($testText -eq '' -or $testText -match '^\[.*\]$') {
      Say-Fail "$title  ->  Independent Test is still a placeholder: '$testText'"; $problems++
    } elseif ($testText.Length -lt 15 -or $testText -match $vague) {
      if ($Gate) { Say-Fail "$title  ->  Independent Test too vague to verify: '$testText'"; $problems++ }
      else       { Say-Warn "$title  ->  Independent Test looks vague: '$testText'. Make it pass/fail." }
    } else {
      Say-Pass "$title"
    }
  }
}

# --- 3. No leftover template scaffolding -----------------------------------
Write-Host ""
Write-Host "2. No leftover template scaffolding"
$scaffold = @('[FEATURE NAME]','TXXX','[Entity1]','[Entity2]','[Entity]','[Title]',
              '[language]','[framework]','[endpoint','[user journey]','[Service]','[location]')
$hit = @()
foreach ($tok in $scaffold) {
  for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i].Contains($tok)) { $hit += ("line {0}: {1}" -f ($i + 1), $tok); break }
  }
}
if ($hit.Count -gt 0) {
  Say-Fail "Sample/placeholder text still present (the plan was not fully filled in):"
  foreach ($h in $hit) { Write-Host "        $h" -ForegroundColor Red }
  $problems++
} else {
  Say-Pass "No template placeholders found."
}

# --- 4. Task completion (GATE only) ----------------------------------------
$open = @(); $done = 0
for ($i = 0; $i -lt $lines.Count; $i++) {
  if ($lines[$i] -match '^\s*-\s*\[\s\]\s*(.+)$') { $open += ("line {0}: {1}" -f ($i + 1), $Matches[1].Trim()) }
  elseif ($lines[$i] -match '^\s*-\s*\[[xX]\]') { $done++ }
}
$total = $done + $open.Count
Write-Host ""
Write-Host "3. Task completion  ($done of $total tasks checked off)"
if ($Gate) {
  if ($open.Count -gt 0) {
    Say-Fail "$($open.Count) task(s) still unchecked - build does NOT match the plan yet:"
    foreach ($o in $open | Select-Object -First 15) { Write-Host "        $o" -ForegroundColor Red }
    if ($open.Count -gt 15) { Write-Host "        ... and $($open.Count - 15) more" -ForegroundColor Red }
    $problems++
  } else {
    Say-Pass "All $total tasks checked off."
  }
} else {
  if ($open.Count -gt 0) { Say-Warn "$($open.Count) task(s) not yet done (fine during build; run -Gate before merge)." }
  else { Say-Pass "All $total tasks checked off." }
}

# --- 5. Verdict -------------------------------------------------------------
Write-Host ""
Write-Host ("=" * 64)
if ($problems -eq 0) {
  if ($Gate) { Write-Host "PASS - build matches the plan. Safe to merge." -ForegroundColor Green }
  else       { Write-Host "PASS - plan is specific enough to build from." -ForegroundColor Green }
  exit 0
} else {
  $what = if ($Gate) { "Do NOT merge yet." } else { "Tighten the plan before building." }
  Write-Host "FAIL - $problems problem area(s) above. $what" -ForegroundColor Red
  exit 1
}
