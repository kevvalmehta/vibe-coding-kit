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
| Run the whole build for me (after a plan exists) | **`/ship`** |
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

*Not sure which of these applies? That's exactly what `/guide` is for. Type it.*
