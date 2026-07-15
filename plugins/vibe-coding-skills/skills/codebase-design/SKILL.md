---
name: codebase-design
description: >-
  Shared vocabulary for designing DEEP MODULES — a lot of behaviour behind a small, simple interface.
  Use when the owner (or another skill) is deciding how to structure code: designing or improving a
  module's interface, choosing where a seam between two parts goes, making code more testable or easier
  for an AI to navigate, or asking "should this be one piece or split?", "what should this expose?",
  "why is this so hard to change?". Says "codebase-design", "deep modules", "design this module",
  "where's the seam". Design-AID only — it gives the language and the principles; it never writes app
  code, never pushes/merges/deploys. NOT UI design (that's `/design-craft`) and NOT database tables
  (that's `/data-model`). The user is a NON-TECHNICAL business owner — plain English, define every term.
---

# codebase-design — design deep modules, not shallow ones

> Vocabulary + principles adapted from Matt Pocock's skills (github.com/mattpocock/skills, MIT) —
> his `codebase-design` skill (new in v1.1, 2026-07) — which draws on John Ousterhout's
> *A Philosophy of Software Design*. Rebuilt natively for this kit: plain English throughout, every
> term defined with a real use-case, and it hands off to the skills this kit already has. It adds
> **no new machinery** — it's a shared language other skills borrow.

Most code that becomes painful to change isn't buggy — it's badly *shaped*. The wrong parts are joined
together, and every part makes callers learn too much before they can use it. This skill gives you (and
every other skill) one consistent language for shaping code well, so the AI structures a build the way a
thoughtful engineer would instead of on autopilot.

**Where this sits in the kit** — it's a design *aid*, invoked during planning and building:
- `/speckit-plan` / `grill-with-docs` can pull this vocabulary when deciding how to structure a feature.
- `/audit` and `/lean-debt` can name *why* a piece of code is hard to work with ("this module is shallow").
- It does not overlap `/design-craft` (how a **screen** looks), `/data-model` (what **tables** you need),
  or the **domain-modeling** discipline in `grill-with-docs` (naming the **business** ideas). Those name
  the *problem*; this shapes the *code* that solves it.

## The glossary — use these words exactly

Consistent language is the whole point. Don't swap in "component", "service", "API", or "boundary" —
they mean different things to different people and the precision leaks away.

- **Module** — anything with an *interface* and an *implementation*. Deliberately scale-agnostic: a
  single function, a class, a whole package, or a slice that spans several. _Real use:_ a
  `sendReceiptEmail(order)` function is a module; so is the entire "billing" package. Avoid: "unit",
  "component", "service" (too tied to one scale).
- **Interface** — *everything a caller must know to use the module correctly.* Not just the function
  name and arguments, but also: what order to call things in, what happens on error, what it needs
  configured, and how fast/slow it is. _Real use:_ the interface of `chargeCard(amount)` includes "it
  throws `CardDeclined` on failure" and "you must call `setApiKey()` first" — a caller who doesn't know
  those will write broken code even with the right function name. Avoid: "API"/"signature" (too narrow —
  they cover only the name-and-arguments surface).
- **Implementation** — what's *inside* the module: the actual body of code. Callers never need to read it.
- **Adapter** — a module whose job is to connect your code to an outside thing (a database, Stripe, the
  file system). _Real use:_ a "Postgres orders repository" is an adapter with a *large* implementation;
  an "in-memory fake orders repository" you use in tests is an adapter with a *tiny* implementation but
  the *same* interface. Reach for "adapter" when the connection point is what you're talking about.
- **Depth** — how much behaviour a caller gets per unit of interface they have to learn. This is the
  whole game:
  - **Deep module** — a *large* amount of behaviour behind a *small, simple* interface. _Real use:_
    `saveDraft(doc)` — one obvious call — behind it: validation, versioning, retry on network failure,
    conflict resolution. The caller learns one thing and gets all of it. Deep = good.
  - **Shallow module** — an interface nearly as complicated as the code behind it: you have to learn a
    lot to get a little. _Real use:_ a "helper" that makes you pass eight arguments and call three
    methods in the right order to do one small thing. Shallow = a warning sign.
- **Seam** — the line where you split one module into two. A *good* seam puts the simple, stable
  interface on the outside and hides the messy, changeable details on the inside. _Real use:_ the seam
  between "the app" and "how we send email" is `sendEmail(to, subject, body)` — swap the email provider
  behind it and nothing outside changes.

## The principles (what "good shape" means)

1. **Make modules deep.** Aim for a lot of behaviour behind a small interface. If an interface is
   almost as hard to learn as reading the code would be, the module isn't earning its keep — either
   deepen it (hide more) or delete it (inline it).
2. **Put the seam where the interface is simplest.** A good split is one where the outside stays simple
   and stable while the complicated, likely-to-change stuff hides inside. If splitting a module forces
   callers to learn *more*, you split in the wrong place.
3. **Design the interface for the caller, not the implementer.** The right question is "what's the
   simplest thing a caller could need to know?" — not "what's easiest for me to expose from in here?"
4. **Pull complexity downward.** Given a choice, the module should absorb the hard part so its callers
   don't have to. One module handling a messy edge case beats ten callers each remembering to.
5. **A deep module is a testable module.** If you can exercise a lot of behaviour through a small
   interface, tests are small and stable too (they hit the interface, not the guts) — which is exactly
   what makes a build safe to change later (constitution: never break working code).

## How to use it in a session

- **Designing something new** (during `/speckit-plan`): for each part, name its *interface* in one line
  and ask "is this deep?" — lots of behaviour, small surface? If not, rethink the seam before any code.
- **Improving something that hurts** (via `/audit` or `/lean-debt` findings): name *why* in this
  language — "this module is shallow: eight arguments for one small result" or "the seam is in the wrong
  place: swapping the database means touching twenty files". Then route the actual change through
  `/safe-change` (isolated copy, tests first, full suite) — **this skill never edits code itself.**
- **Making code AI-navigable:** deep modules with small interfaces are also easier for an AI to work on
  safely later — it only has to understand the interface to use the module, not re-read the whole body.

## Hard rules

- **Plain English, every term defined the first time with a real use-case** — the owner is
  non-technical and wants to learn the words. Never an analogy to an unrelated object; always a concrete
  scenario of using the real thing. "make sense?" after each new idea.
- **Design-aid only.** It gives language and judgement. It does **not** write app code, run a build, or
  restructure anything — real changes go through `/safe-change`; new builds through the normal kit flow.
- **NEVER push / merge / deploy.**
- **Use the words exactly** — Module / Interface / Implementation / Adapter / Depth / Seam. Swapping in
  vaguer words is how the shared language rots.

## For non-Claude agents

Plain procedure — read this file, then apply the glossary and the five principles when helping structure
code: for each module name its interface in one line and check it's *deep* (lots of behaviour, small
surface); put seams where the outside stays simplest; design for the caller. It is advice only — route
any real code change through the kit's `safe-change` workflow. Everything here is plain Markdown; nothing
is Claude-only.
