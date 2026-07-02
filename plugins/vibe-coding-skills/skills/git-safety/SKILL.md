---
name: git-safety
description: >-
  GitHub safety + version-control best-practices guardrail. Use this WHENEVER git or GitHub is
  involved — committing, saving work, branching, pushing, pull requests, merging, tagging releases,
  UNDOING / REVERTING a change, recovering a deleted file, or resuming work in a new session. Also
  use when the user says "save", "back up", "undo", "go back", "revert", "it broke", "restore",
  "start where I left off", "new branch", or "publish/deploy". Keeps main always-working and makes
  every change reversible. The user is NON-TECHNICAL — run the git mechanics for them and explain in
  plain English.
---

# Git Safety: so work never gets lost or messed up

The user is non-technical. YOU run the git commands and explain in plain words. Keep `main` always
clean and deployable. Make every change reversible. Default to SAFE, non-destructive git.

## Standing rules (always)
1. **Never work directly on `main`.** For any new feature or edit, create a branch
   (`feat/<short-name>` or `fix/<short-name>`) or a git worktree. Merge to main only when it works.
2. **Commit in small steps with clear messages.** Each commit is a save point you can return to.
   Use Conventional Commits (`feat:`, `fix:`, `chore:`, `docs:`).
3. **Push after meaningful progress.** Pushing backs work up to GitHub — safe if the laptop dies.
   Helper: `"${CLAUDE_PLUGIN_ROOT}/scripts/save.ps1" -Message "what changed"` does add + commit + push in one go.
4. **Merge to `main` via a Pull Request**, not direct commits — so main stays reviewed + working.
5. **Before anything risky** (big refactor, deleting files, upgrading dependencies): make a clean
   commit + push first (a save point), and offer to tag it (`git tag good-YYYYMMDD`).
6. **Tag known-good versions** so there's always a safe point to return to.

## Undo / recover (prefer SAFE, non-destructive)
- Undo a change: `git revert <commit>` — makes a new commit that reverses it, keeps full history.
  Avoid `git reset --hard` unless the user explicitly asks AND you back up the branch first.
- Restore a deleted file: `git restore --source=<commit> -- <path>` (or `git checkout <commit> -- <path>`).
- Go back to a known-good version: show `git log --oneline`, confirm the target with the user, then
  `git revert` the bad range (or branch from the good commit). NEVER force-push `main`.
- ALWAYS confirm before any destructive/irreversible git op, and explain in plain English what it does.

## Never
- Never `git push --force` to `main`/`master`. Never rewrite shared history.
- Never commit secrets (`.env`, keys) — they live in `.gitignore`; keep them there.
- Never delete a branch with unmerged work without the user's OK.

## Going public (deploy escalation)
When the owner signals they want to put an app **live for real external users** — deploy/ship/launch
*publicly* — read the **intent**, not just the word "public" ("put it live", "on Vercel for everyone",
"send customers the link" all count). At that moment, STOP and do this before helping them deploy:

1. **Remind them, in plain English, of the heavier security methods deferred for internal tools** —
   from `docs/security-six-check.md`: per-app **attack-tests** (hit login 1,000× → assert blocked;
   fetch another user's record → assert denied), **custom Semgrep rules**, a **live attack scan
   (DAST)**, and a **threat-modeling step**. These were skipped on purpose because the app was internal;
   going public is exactly when they start to matter.
2. **Offer to add the per-app attack-tests** for the **login** and **money/data** endpoints before go-live.
3. **Record the owner's decision** (accept or decline) in plain markdown (the deploy conversation /
   HANDOFF.md) — a conscious, logged choice, never a silent skip.
4. **Warn, do not block.** Declining does not stop the deploy — the owner decides; you log it.
5. **Fire on the internal→public transition** while these items are still open. Do **not** nag on
   routine re-deploys once they are resolved or explicitly declined (check the log first).
6. **Walk `docs/production-readiness.md` with them** (spec 016 Phase 3) — the six checks between
   "works" and "safe to run for real users": dependency audit green (CI does it), schema changes
   via additive-first migrations with a backup taken first, error monitoring wired (Sentry-style —
   crashes, not just AI drift), data backups exist AND a restore was tested once, a load smoke on
   the heaviest endpoint, and accessibility basics for anything user-facing. Same rule as above:
   record decisions, warn, never block.

This lives in the kit (this file + `docs/security-six-check.md` + `docs/production-readiness.md`),
so any AI tool reaches it — not only Claude's memory (Principle VI).

## Resuming a session (start where you left off)
On a new session: run `git status` + `git log --oneline -5`, run `git pull`, and read `HANDOFF.md`.
Then summarize in plain English where things stand and what's next BEFORE doing anything.
