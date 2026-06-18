# Reusing This Scaffold for New Projects

This repo is a **reusable starter** for spec-driven projects. Every new app you start
gets the same rules (constitution), the same safety net (CI + Semgrep), and the same
portable docs — so you never set this up from scratch again.

## What's included (the reusable tree)
```
.
├── .github/workflows/ci.yml      # Auto: Semgrep security scan + tests on every push
├── .specify/                     # GitHub Spec Kit engine (templates, scripts, constitution)
│   └── memory/constitution.md    # Your hard rules (security, TDD, regression safety)
├── .claude/skills/speckit-*      # /speckit-* slash commands
├── docs/memory-snapshot/         # Portable memory for non-Claude AI tools
├── scripts/new-project.ps1       # One-command bootstrap for a NEW project
├── CLAUDE.md  AGENTS.md  HANDOFF.md  README.md  plan.md
├── .gitignore  .env.example
```

## Two ways to start a new project

### Option A — GitHub template (simplest)
This repo is marked as a GitHub **template**. To start a new project:
```powershell
gh repo create my-new-app --template kevvalmehta/Perfecting-Coding-Spec-Kit --private --clone
```
You get an exact copy. Then edit the project name in `CLAUDE.md` + `.specify/memory/constitution.md`,
or just run `/speckit-constitution` in Claude Code to refresh them.

### Option B — Bootstrap script (fresh Spec Kit install)
Run from inside THIS repo to scaffold a brand-new project folder with a fresh Spec Kit init
plus the reusable files copied in:
```powershell
.\scripts\new-project.ps1 -Name "My New App"
```
Creates `C:\Projects\My New App` ready to go.

## After starting a new project
1. Open Claude Code in the project folder.
2. Make sure Superpowers is installed: `/plugin install superpowers@claude-plugins-official`.
3. `/speckit-constitution` → `/speckit-specify` → `/speckit-plan` → `/speckit-tasks` → build.

## What's automatic vs manual
| Thing | Automatic? |
|---|---|
| Semgrep security scan on push | ✅ Yes (CI) |
| Reminders to add tests / RLS / review | ✅ Yes (baked into constitution; AI raises during planning) |
| Running tests on push | ✅ Yes (CI, once tests exist) |
| Creating Supabase / Vercel accounts + login | ❌ Manual, one-time per your credentials |
