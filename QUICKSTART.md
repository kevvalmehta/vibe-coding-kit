# QUICKSTART — using this kit when you're not a software person

You don't need to memorize the 40+ skills. You need **two habits** and **one
fallback**. Everything else, the kit tells you when you need it.

## The one fallback

**When in doubt, type `/guide`** (or `/start` on a brand-new project). It looks
at where your project actually is and tells you the single next thing to do.
You can ask it anytime — "where am I, what's next?" — and it never guesses; it
reads the real state first.

## The two habits (these make everything else work)

1. **Plan before you build.** If you catch yourself wanting to "just build it,"
   run `/guide` or `idea-to-app` first. Nothing gets built before a plan is
   approved — that's what stops you building the wrong thing.
2. **Never break what already works.** For ANY change to something that already
   exists — fix, tweak, rename, remove — say `safe-change`, not "just edit it."
   It locks current behavior in tests first, so changing one thing can't
   silently break another.

---

## Situation → what to type

### Starting something new
| You want to… | Type |
|---|---|
| Be walked through the whole thing, plain English | **`/start`** |
| Check if the idea is even worth building | **`/discover`** |
| A big, foggy idea that's too much to plan at once | **`/pathfinder`** |
| Pin down a fuzzy idea by being interviewed | **`grill-me`** |
| See how others build this / which tools to use | **`/research-scout`** or **`/stack`** |
| Create the starter files once the tools are picked | **`/scaffold`** |

### Making it good (your quality system)
| You want to… | Type |
|---|---|
| Stop output being a coin flip — "make this actually good" | **`/quality-charter`** |
| Turn a vague ask into clear guardrails before work starts | **`/goal`** |
| Write a new skill/plugin the AI follows the same way every run | **`/skill-craft`** |
| Make anything with a screen *look* designed — "it looks AI-generated" | **`/design-craft`** |

> `/quality-charter` installs house rules + automatic checks so quality is
> enforced by files, not by hoping the AI remembers. Do it once per serious
> project. See its `references/working-method.md` for the 10 rules you can paste
> into any project's `AGENTS.md` / `CLAUDE.md` — that's how you make ANY model
> (Claude, or anything else, now or later) work carefully.

### Building & fixing
| You want to… | Type |
|---|---|
| War-game the plan first — know what failure looks like before building | **`/wargame`** |
| Run the whole build for me (after a plan exists) | **`/ship`** |
| Work out what the app must remember — "what tables do I need?" | **`/data-model`** |
| Add login / user accounts / "only members see this" | **`/add-login`** |
| Take payments, send emails, or let users upload files | **`/wire-up`** |
| Change / fix existing code safely | **`safe-change`** |
| Stuck on a bug | **`systematic-debugging`** |
| Confirm a change really works (not just "tests exist") | **`/verify`** |
| Understand how a piece of code fits before touching it | **`/zoom-out`** |

### Checking & shipping
| You want to… | Type |
|---|---|
| "What shape is this in? safe to ship?" | **`/health`** |
| "What's actually worth fixing?" (deep) | **`/audit`** |
| "Did I over-build this?" | **`/lean-review`** |
| Check security before going live | **`/security-review`** |
| Anything git — save, undo, branch, put it live, "it broke" | **`git-safety`** |
| Know the moment your live site goes down | **`/uptime`** |
| Make sure no service can quietly bill you | **`/cost-watch`** |

### If your app has AI inside it (chatbot, agent, any LLM feature)
| You want to… | Type |
|---|---|
| Design the AI part | **`agent-architect`** |
| Prove the AI's output is good and stays good | **`/agent-eval`** |
| Watch a live app's AI for quality drift | **`/monitor`** |

---

## The safety nets (these run themselves — nothing to type)

You don't invoke these; they watch in the background and speak up only when
needed:

- **Tests-first guard** — won't let new code be written before a failing test
  exists for it.
- **Done-claim verifier** — blocks the AI from saying "done / tests pass /
  pushed" unless the proving command actually ran.
- **Destructive-action gate** — pauses risky commands (delete a table, `rm -rf`)
  and asks your OK first.
- **Lessons injector** — every correction you've banked stays in force in future
  sessions, so the same mistake isn't repeated.
- **Import reality check** — catches the AI inventing a package/library that
  doesn't exist, right after it writes it.

---

## The whole normal journey, in order

```
idea → /guide → /goal → /discover → grill-me → /speckit-specify → /speckit-plan
     → /speckit-tasks → (install /quality-charter once) → /ship → /verify
     → /security-review → git-safety (save → preview → live)
```

Don't want to run the planning steps by hand? **`autopilot`** runs the middle
of that chain for you, stopping for your "go" at each step. It never puts
anything live — that always stays your call.

---

## Playbooks — the same kit, by project type

The skills never change per project; what changes is **which steps you actually
need and which contract files you'll be asked to say "yes" to**. Find your
project below. Each playbook is just "what to type, in order" — and remember,
**`/start` will drive any of these for you**; the playbooks exist so you can see
where you're going.

### A web app or SaaS — e.g. a CRM your clients log into

The full journey, nothing skipped. This is the project type the kit's defaults
were built for.

1. **`/start`** — or `/discover` first if you're not sure it's worth building.
2. Plan: `/speckit-specify` → `/speckit-clarify` → `/speckit-plan` (or let
   **`autopilot`** run them, stopping for your "go").
3. **`/stack`** then **`/scaffold`** — pick boring, proven tools; get starter files.
4. **`/data-model`** — a CRM *is* mostly its tables (contacts, companies, deals,
   notes). You'll approve a `DATA-MODEL.md` before any table exists.
5. **`/add-login`** — accounts, plus the rule that clients only ever see their
   OWN data (you'll approve `AUTH-SPEC.md`).
6. **`/design-craft`** — decide the look before any screen is built (`DESIGN-SPEC.md`).
7. **`/wargame`** — battle-plan the build: what failure looks like at each step
   and the pre-decided response (`WARGAME.md`).
8. **`/ship`** → **`/verify`** → **`/security-review`** → **`git-safety`** to go live.
9. Once live: **`/uptime`** + **`/cost-watch`**, and **`/wire-up`** the day you
   add payments or email.

### A second brain / personal knowledge tool

The same spine, lighter — it's a data-shaped app with one user: you.

- Skip `/discover` (you ARE the user). Start at `/speckit-specify`.
- **`/data-model`** is the heart: notes, tags, links between notes, sources.
  Get the "how do things connect" question right here and everything else is easy.
- **`/add-login`** the moment it lives on the public internet — even if the only
  account is yours.
- Design can stay light; `/wargame` is still worth it if an import step (your
  old notes, bookmarks, exports) could go wrong — imports are where data dies.

### An AI workflow — content pipeline, report generator, chatbot

Your app **contains AI**, so the AI-inside lane applies on top of the normal journey:

- At plan time: **`agent-architect`** (how many agents, which model) + the
  13 decisions in `docs/ai-feature-checklist.md`.
- **`/agent-eval`** before you trust the output — a scored test set, so "is it
  good?" has a number, and a change that makes it worse gets blocked.
- **`/monitor`** after launch — samples real output and alerts on drift.
- **`/cost-watch`** is not optional here: AI keys always get a monthly cap.

### A recurring loop — something that runs on a schedule, unattended

An automation nobody watches run. Two things matter more than anywhere else:

- Spec ONE run ("each morning it reads X and produces Y"), then schedule it.
  The stack is usually the smallest thing `/stack` offers — often a script, not an app.
- Because nobody's watching, it must **fail loud, never silently**: `/wargame`'s
  abort conditions decide when it stops instead of guessing, structured logs
  say what happened, and an outside heartbeat check (`/uptime` thinking) tells
  you when it *didn't* run.

### An internal tool / dashboard for your own business

The lightest path — no strangers, no accounts (usually), speed matters:

**`/goal`** (guardrails in one step) → **`/stack`** (it'll suggest the simple
tier) → **`/scaffold`** → `/data-model` only if it remembers things → **`/ship`**
→ **`/verify`**. Skip what doesn't apply; `/guide` will tell you what does.

### A public marketing website

Mostly pages, not data: skip `/data-model` and `/add-login`, lean hard on
**`/design-craft`** (the look IS the product), then `/ship` → `/verify` →
`git-safety` live, with **`/uptime`** after.

### A phone app

Honest scope: **`/scaffold` declines mobile stacks today** (packaging is a
planned, deferred spec). The practical route now: build it as a web app — it
runs in the phone's browser and can be added to the home screen — and revisit
native packaging when the kit supports it.

---

*Not sure which of these applies? That's exactly what `/guide` is for. Type it.*
