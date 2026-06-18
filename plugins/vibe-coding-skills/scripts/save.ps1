# One-command "save my work": stage everything, commit, and back up to GitHub.
#
# Usage:
#   .\scripts\save.ps1 -Message "added the login page"
#   .\scripts\save.ps1                      # uses a default message

param([string]$Message = "save work")

$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)

git add -A
$changes = git status --porcelain
if (-not $changes) {
  Write-Host "Nothing to save — already up to date." -ForegroundColor Yellow
  return
}

git commit -m $Message
git push

Write-Host ""
Write-Host "Saved + backed up to GitHub." -ForegroundColor Green
Write-Host "Branch: $(git rev-parse --abbrev-ref HEAD)   Commit: $(git rev-parse --short HEAD)"
