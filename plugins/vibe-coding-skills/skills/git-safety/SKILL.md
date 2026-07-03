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

## Merge conflicts — rescue (nothing is lost)
A **merge conflict** happens when you and another change (another branch, another session, a
teammate) both edited the **same lines** of the same file. Git can merge most changes
automatically, but when two edits overlap, git refuses to guess which version should win — it
stops and asks a human to decide.

**Nothing is lost.** Both versions are still sitting right there in the file — git just needs
you to pick. Nothing has been deleted or overwritten.

**What the owner will literally see** in the conflicted file, between markers git inserts:
```
<<<<<<< HEAD
(your current version of these lines)
=======
(the other version of these lines)
>>>>>>> other-branch
```
Everything from `<<<<<<<` down to `=======` is one version; everything from `=======` down to
`>>>>>>>` is the other. Both are real, both are preserved — git is just waiting to be told which
one (or what combination) to keep.

**Division of labor:** the AI runs the git mechanics (starts the merge, finds every conflicted
file, removes the markers once a choice is made) and explains **both versions in plain English** —
what each one does, not just the raw code. The **owner picks** which version wins, or asks for a
blend. The AI never silently picks a side.

**The always-safe escape hatch:** `git merge --abort` cancels the merge in progress and puts
everything back exactly to how it was the moment before the merge started — no conflict markers,
no half-finished merge, no risk. If a conflict looks confusing or high-stakes, abort first and
regroup; you can always try again.

**Special rule — never resolve conflicts blind in migration/schema files.** A conflict in a
database migration or schema file is destructive-action-gate territory (spec 017): both sides may
have changed what the database looks like, and guessing wrong can corrupt real data. For these
files, stop, show the owner both versions in plain English, and get explicit confirmation on the
resolution before continuing — never auto-merge and move on.

## Never
- Never `git push --force` to `main`/`master`. Never rewrite shared history.
- Never commit secrets (`.env`, keys) — they live in `.gitignore`; keep them there.
- Never delete a branch with unmerged work without the user's OK.

## Going public (deploy escalation)
When the owner signals they want to put an app **live for real external users** — deploy/ship/launch
*publicly* — read the **intent**, not just the word "public" ("put it live", "on Vercel for everyone",
"send customers the link" all count). At that moment, STOP and do this before helping them deploy:

1. **Run the pre-flight security gate first**: `python plugins/vibe-coding-skills/scripts/preflight_gate.py`. This is a
   deterministic, no-AI scan — it mechanically checks for leaked secrets (API keys/tokens hardcoded
   in tracked files), missing Row-Level Security (a Supabase/Postgres setting that stops one user
   reading another user's data), and missing rate limiting (a cap on how many times someone can hit
   an endpoint). Show the owner the result before any deploy step continues.
2. **Remind them, in plain English, of the heavier security methods deferred for internal tools** —
   from `docs/security-six-check.md`: per-app **attack-tests** (hit login 1,000× → assert blocked;
   fetch another user's record → assert denied), **custom Semgrep rules**, a **live attack scan
   (DAST)**, and a **threat-modeling step**. These were skipped on purpose because the app was internal;
   going public is exactly when they start to matter.
3. **Offer to add the per-app attack-tests** for the **login** and **money/data** endpoints before go-live.
4. **Record the owner's decision** (accept or decline) in plain markdown (the deploy conversation /
   HANDOFF.md) — a conscious, logged choice, never a silent skip.
5. **Warn, do not block.** Declining does not stop the deploy — the owner decides; you log it.
6. **Fire on the internal→public transition** while these items are still open. Do **not** nag on
   routine re-deploys once they are resolved or explicitly declined (check the log first).
7. **Walk `docs/production-readiness.md` with them** (spec 016 Phase 3) — the six checks between
   "works" and "safe to run for real users": dependency audit green (CI does it), schema changes
   via additive-first migrations with a backup taken first, error monitoring wired (Sentry-style —
   crashes, not just AI drift), data backups exist AND a restore was tested once, a load smoke on
   the heaviest endpoint, and accessibility basics for anything user-facing. Same rule as above:
   record decisions, warn, never block.

**Never run Claude Code with `--dangerously-skip-permissions`.** That flag removes every human
approval gate this skill (and the kit) relies on — no more "ask before deploy," no more pausing on
a destructive command. It is never appropriate for this project, deploy or otherwise.

This lives in the kit (this file + `docs/security-six-check.md` + `docs/production-readiness.md`),
so any AI tool reaches it — not only Claude's memory (Principle VI).

## Resuming a session (start where you left off)
On a new session: run `git status` + `git log --oneline -5`, run `git pull`, and read `HANDOFF.md`.
Then summarize in plain English where things stand and what's next BEFORE doing anything.
