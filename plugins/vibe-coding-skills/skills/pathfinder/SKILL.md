---
name: pathfinder
description: >-
  For ideas TOO BIG AND FOGGY for one session — BEFORE /speckit-specify. Use when the owner says
  "pathfinder", "this idea is huge", "I don't know where to start", "too big to plan", "map this
  out", or describes something so large they can't see the shape of it yet. Keeps a local map
  (`pathfinder/map.md` in the project — no issue-tracker dependency) of standing Notes, a
  Decisions-so-far index, and Fog (questions felt but not yet sharp), plus one-file-per-question
  tickets routed to EXISTING kit skills. Resolves at most ONE ticket per session. Exits by handing
  the Decisions-so-far index to /speckit-specify once fog is empty and no tickets remain open.
---

# Pathfinder: chart an oversized idea down to something speccable

> Adapted from Matt Pocock's skills (github.com/mattpocock/skills, MIT) — his `wayfinder` skill
> (in-progress draft there). Rebuilt natively for this kit: no issue tracker, plain English
> throughout, every ticket routes to a skill this kit already has.

Some ideas are too big and too foggy to hand straight to `/speckit-specify` — you can feel there
are important questions in there, but you can't even phrase most of them yet. Trying to write a
spec now would mean guessing. Pathfinder's job is to slowly turn that fog into a short list of
resolved decisions, one small step at a time, until the idea is small and clear enough to spec.

**Where this sits in the kit:** `/discover` checks whether an idea is **worth** building at all.
`/pathfinder` is for the *next* problem — the idea already seems worth doing, but it's too big to
see the shape of in one sitting. Run `/discover` first if worth-building is still in question; run
`/pathfinder` once you're past that and staring at something too large to plan in one go. They
compose: discover, then pathfinder, then `/speckit-specify`.

## The map — `pathfinder/map.md`

A single markdown file, checked into the project (never an external issue tracker — the owner
should be able to read the whole state of the idea in one file, in their own repo). It has three
sections:

1. **Notes** — standing context about the idea: what it is, why it matters, anything worth
   remembering that isn't a decision or an open question. This grows slowly over time.
2. **Decisions so far** — an INDEX only. One line + a link per resolved ticket
   (e.g. `- Payments: one-time only, no subscriptions — see tickets/closed/0003-payments-model.md`).
   The actual reasoning lives in the ticket file, not here. Keeping this to an index means the map
   stays skimmable even after dozens of decisions.
3. **Fog** — questions you can feel coming but cannot phrase sharply yet. Written loosely, on
   purpose left incomplete. Example: "something about how refunds interact with the trial period,
   not sure what yet." Fog is not a task list — it is a place to note a shape without forcing it
   into a question before it's ready.

## Tickets — `pathfinder/tickets/`

Two subfolders: `open/` and `closed/`. Each ticket is one file holding exactly **one sharp
question**, sized to be answerable in a single session. A ticket may declare **"blocked by:
<other ticket>"** — the **frontier** is the set of open tickets that are not blocked by anything;
that's what you actually work from next.

Every ticket has a **type**, and every type routes to a skill this kit already has — pathfinder
never invents new machinery:

| Type | Routes to | What it means |
|---|---|---|
| **research** | `research-scout` | Needs real, cited evidence before it can be answered (how do others do this, what does the market look like). |
| **prototype** | `/prototype` | Needs a throwaway build to feel out whether an approach works, before committing. |
| **grilling** | `grill-me` or `grill-with-docs` | Needs an interview to pressure-test a decision — `grill-with-docs` if the project already has code/terms to check against, `grill-me` otherwise. |
| **task** | manual work the owner does | Something only the human can do (an account to sign up for, a person to ask, a legal question to check). Pathfinder gives a precise checklist and waits for the answer, rather than doing it itself. |

## HARD RULES

- **Resolve at most ONE ticket per session.** Pick the single most valuable open, unblocked ticket
  and work only that one. This keeps each session small enough to actually finish and keeps
  decisions traceable to a single sitting.
- **The charting session never also resolves tickets.** A session spent updating the map (writing
  Notes, moving fog into new tickets, reordering the frontier) is a distinct session from one spent
  resolving a ticket. Don't blend the two — mixing "restructure the map" with "answer this question"
  makes both harder to review later.
- **The fog-vs-ticket test: can you phrase the question SHARPLY now?** If yes — even if it's
  blocked by something else — it's a ticket. If no, it stays fog. "Sharp" means someone else could
  read the question and know exactly what answer would resolve it.
- **Never pre-slice fog into fake tickets.** Don't manufacture a precise-looking ticket just to feel
  productive. A vague feeling written honestly as fog is more useful than a fake-sharp ticket that
  turns out to be the wrong question.
- **Resolving a ticket can change everything downstream.** It may graduate some fog into new
  tickets (now that you know more, a fuzzy feeling becomes phraseable), and it may invalidate
  existing open tickets (a decision you just made makes another ticket's question moot, or wrong).
  When that happens, update or delete the affected tickets in the same pass — don't leave stale
  tickets sitting in `open/`.

## Exit — handing off to `/speckit-specify`

When **Fog is empty** and **no tickets remain open** (everything is in `tickets/closed/`), the idea
is no longer foggy — it's ready to spec. Hand the **Decisions-so-far index** from `map.md` to
`/speckit-specify` as grounding: it becomes the set of resolved calls the spec is written against,
so the spec-writing step isn't re-litigating decisions pathfinder already settled.

## Fit with this project
- Sits **before** `/speckit-specify`, and before `grill-me`/`grill-with-docs` are run standalone —
  pathfinder is for when the idea is too large to even get to a single plan worth grilling yet.
- The owner is non-technical: explain "ticket," "fog," and "frontier" in plain English the first
  time each appears in a session, with a real example from their own idea — not an abstract
  definition.
- Read/write only inside `pathfinder/` (the map + tickets). It does not touch app code, and it does
  not run `research-scout` / `/prototype` / `grill-me` / `grill-with-docs` itself without the
  owner's go-ahead each time — it identifies which ticket needs which skill, then hands off.
