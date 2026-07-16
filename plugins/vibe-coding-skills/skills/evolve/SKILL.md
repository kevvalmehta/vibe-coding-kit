---
name: evolve
description: >-
  The learning-loop distiller — turns raw captured material (candidate lessons, session
  corrections, stated preferences) into the small set of files that auto-load every session,
  so the AI measurably adapts to the owner over time instead of accumulating junk. Use when
  the session starts with an "[evolve] N unreviewed candidate lessons pending" or
  "[evolve] ... budget — consolidate" nudge, when the owner says "/evolve", "evolve now",
  "learn from this", "remember how I work", "update your profile", or right after the owner
  states a durable preference/correction worth keeping. Distill-then-approve: the model
  proposes at most 3 one-line edits, the owner approves in one word, junk gets deleted.
  Adapted from the Hermes Agent pattern (background review + capacity-forced consolidation),
  with the blind-capture step replaced by owner-approved distillation. The user is a
  NON-TECHNICAL business owner — plain English, define every term.
---

# Evolve: distill captured signal into rules that persist

You are closing the learning loop. Capture already happens automatically (full transcripts
on disk + `capture-lessons` candidates in `.specify/memory/lessons.md`). Injection already
happens automatically (confirmed lessons + memory + the owner's global profile load every
session). **The missing step is distillation — that is this skill, and nothing else does it.**

Why owner-approved instead of fully automatic (the Hermes way): unattended capture provably
rots — the capture hook once logged the same junk phrase as a candidate **14 times**. A blind
auto-distiller would have promoted noise. You propose; the owner vetoes in one word; the
profile stays true.

## STEP 1 — Gather (read, never guess)

- Read `.specify/memory/lessons.md` → the `### candidate --` entries (the unreviewed pile).
- Recall this session's (and recent sessions') corrections: moments the owner said
  "no", "always", "never", "from now on", "I prefer", or corrected your approach.
  If unsure what happened recently, run `python scripts/recall.py <keywords>`.
- Read the current targets so you never duplicate: confirmed `L-#`/`P-#` entries,
  `~/.claude/CLAUDE.md` (the owner's global profile), and the project memory index.

## STEP 2 — Distill (the judgment step)

For each piece of raw signal, decide its ONE destination — or the trash:

| Signal | Destination |
|---|---|
| A mistake that must never repeat (has a story + a self-check) | `lessons.md` as a confirmed `L-#` |
| A proven habit worth enforcing | `lessons.md` as a `P-#` |
| A durable owner preference about HOW to work (style, tone, workflow, tools) | the owner's global profile (`~/.claude/CLAUDE.md`) or a `type: user`/`feedback` memory file |
| A project fact not derivable from the repo | a `type: project` memory file |
| Duplicate, mis-capture, garbled text, one-off context | **delete — deleting junk is a first-class outcome, not a failure** |

Rules of distillation:
- **Propose at most 3 edits per run.** More means you are transcribing, not distilling.
- Each proposal is ONE line: destination + the exact text to add. No essays.
- Merge near-duplicates into the sharpest single phrasing; never add a rule that already
  exists in different words (grep the target first).
- A candidate that appears N times is still ONE lesson (or one deletion).

## STEP 3 — Owner approval (one word each)

Show the proposals as a short numbered list: `1. [profile] "..."  2. [L-3] "..."  3. [delete 14 junk candidates]`.
The owner replies with approvals ("1 and 3", "all", "skip 2"). **Never write without approval** —
except pure junk deletion of candidates, which you may include in the same confirmation.

## STEP 4 — Write + clean (make it stick)

- Apply approved edits to their destinations. New memory files follow the standard
  frontmatter + one-line MEMORY.md index pointer.
- Delete every processed candidate from `lessons.md` (promoted or junked) — the pile
  must be EMPTY after a run, or the nudge becomes noise.
- **Capacity duty (Hermes rule):** if the session-start nudge said a file is past 80% of
  its budget, you must consolidate that file (merge overlapping entries, sharpen wording,
  delete stale ones) BEFORE adding anything new. The cap is the distillation trigger:
  learning and token-efficiency are the same mechanism.
- Confirm in one line per write: file + what changed.

## Hard rules

- Distill-then-approve. Never silently rewrite the owner's profile or confirmed lessons.
- Deletion is success. An empty candidate pile and a leaner file are the win conditions.
- Never fabricate a "lesson" the transcript does not support; when in doubt, ask or drop.
- This skill writes ONLY to: `lessons.md`, memory files + `MEMORY.md`, and (with explicit
  approval) `~/.claude/CLAUDE.md`. Nothing else. Never code, never settings, never git.
- Works in any AI tool: the capture/injection hooks are Claude-specific, but this
  procedure (read candidates → distill → approve → write) is plain text — a non-Claude
  agent follows it manually per `AGENTS.md` (Principle VI).
