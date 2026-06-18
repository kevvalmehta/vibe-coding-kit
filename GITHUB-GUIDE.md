# GitHub Guide (Plain English)

You don't need to know git commands — the AI runs them. This explains what's happening and how to
ask for things, so your work is always safe and reversible.

## The ideas, in plain words
- **Commit** = a SAVE POINT. We save often, each with a short note ("added login page").
- **Branch** = a safe COPY to work on, so the main version never breaks while we build.
- **main** = the official, always-working version. It only changes after a change is tested.
- **Push** = upload to GitHub = a BACKUP in the cloud. If your laptop died, your work is safe.
- **Pull Request (PR)** = the reviewed way to fold a branch's work into main.
- **Revert** = the UNDO button. Any change can be undone, back to a working save point.
- **Tag** = a BOOKMARK of a known-good version (e.g. "v1") you can always return to.
- **.env + .gitignore** = your secrets (passwords/keys) stay in a file that is NEVER uploaded.

## How to ask the AI (just say it in plain English)
| You say | What happens |
|---|---|
| "Save my work" | Commit + push (backup to GitHub). Or run `scripts/save.ps1 -Message "what changed"` |
| "Start a new change/feature" | Makes a safe branch so `main` stays working |
| "It broke / undo that" | Safely reverts to the last working save point |
| "Go back to when X worked" | Finds that save point and rolls back safely |
| "I deleted something" | Restores it from history |
| "Where did we leave off?" | Reads history + HANDOFF.md and summarizes |
| "Publish / deploy" | Merges the tested branch to main via a PR, then deploys |

## Why you won't lose work or mess things up
1. We never edit the main version directly — always a safe branch/copy.
2. We save (commit) and back up (push) often — every step is recoverable.
3. `main` only changes after tests pass.
4. Secrets live in `.env`, which is never uploaded (`.gitignore` protects it).
5. Anything can be undone with revert — once pushed, nothing is truly gone.

## Starting a session from where you left off
Open Claude Code in this folder and say **"where did we leave off?"** — the AI reads `HANDOFF.md`
and recent history, then tells you the current state and what's next before doing anything.
