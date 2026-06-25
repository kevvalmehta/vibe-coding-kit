---
name: scaffold
description: Stack scaffolding (Conductor v7) — creates a MINIMAL, runnable starter for a chosen stack so an empty folder becomes something that runs locally. The doer companion to /stack (which only recommends). Use WHENEVER the owner has a stack picked and says "scaffold it", "set up the starter", "create the project files", "/scaffold", "make the skeleton", or reaches the setup step after /stack. It drives scripts/scaffold_stack.py, which writes a small safe skeleton (dependency file, a hello-world entry, .gitignore, .env.example, a README with run + deploy notes). HARD GUARANTEES: it NEVER overwrites an existing file (only creates what's missing, reports what it skipped), declines stacks it can't scaffold instead of writing a wrong skeleton, and NEVER pushes/merges/deploys. The user is a NON-TECHNICAL business owner — plain English, define every term, "make sense?" checks.
---

# /scaffold — create your project's starter files (Conductor v7)

The owner is a **non-technical business owner**. *Scaffold = auto-create the starter files for a stack*
(the *stack* = the tools the app is built from). Your job: turn the stack `/stack` recommended into a
**minimal, runnable starter** — an empty folder becomes something that runs on their computer — then
explain how to run it and how to grow it. Define every term the first time; give a "make sense?".

This is **Option 1 (minimal)** by the owner's choice: a small, safe skeleton, not a full app. The owner
grows it via the kit's build flow afterward (so richness is built to fit, not guessed).

## 1. Confirm the stack + the folder

- **Stack:** use the one `/stack` recommended. Supported keys: `streamlit`, `fastapi`, `python-script`,
  `nextjs`, `static-site`. If the recommended thing isn't one of these (e.g. a no-code mobile builder),
  say it isn't scaffoldable here and point to that tool's own setup — don't write a wrong skeleton.
- **Folder:** ask where to create it (the target folder). Confirm before writing.

## 2. Run the scaffolder

Run `python scripts/scaffold_stack.py <stack> <target-folder>`. It writes the minimal starter:
a dependency file, a hello-world entry file (for code stacks), `.gitignore` (so junk + secrets aren't
saved), `.env.example` (a template for secret keys, no real values), and a `README.md` that includes
**how to run it** and a **"How to put this live"** note naming the matching host.

## 3. Never overwrite — report honestly

The scaffolder **never overwrites an existing file** — it only creates what's missing and reports what
it **skipped**. Relay that plainly: list what was created and what already existed (left untouched). If
the owner wants to replace a file, that's their explicit call — never do it silently.

## 4. Explain + hand off

Tell the owner, in plain English: what was created, the one command to run it, and where the README's
"put this live" note is. Then hand off:
- **Run it** locally with the printed command.
- **Grow it** → `/safe-change` (edits) or `/start` / `/ship` (new features) — each built tests-first.
- **Put it live** → `git-safety` → preview → the matching host (Vercel / Streamlit Cloud / Render) +
  Supabase. **`/scaffold` itself never deploys** — going live stays the owner's manual step.

## Hard rules
- **Plain English, every term defined**; "make sense?" checks.
- **Minimal (Option 1)** — a runnable skeleton, not a full app (richer templates = a future v7.5).
- **NEVER overwrite** an existing file — create only what's missing; report skips.
- **Decline** an unsupported/non-scaffoldable stack instead of writing a wrong skeleton (Principle VII).
- **NEVER** push / merge / deploy.

## For non-Claude agents
Plain procedure — confirm the stack + folder, then run `python scripts/scaffold_stack.py <stack>
<target>` and relay created-vs-skipped. The never-overwrite + never-deploy guarantees are enforced by
the script + this contract. Nothing here is Claude-only.
