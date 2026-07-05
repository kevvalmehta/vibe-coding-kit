---
name: add-login
description: >-
  The login coach — adds user accounts to a vibe-coded app the boring, safe way, so the single
  easiest place to be dangerously wrong isn't. Use WHENEVER the owner says "add login", "user
  accounts", "sign up / sign in", "only members can see this", "protect this page", or runs
  "/add-login". Writes a binding AUTH-SPEC.md contract before wiring anything, uses managed auth
  only (NEVER hand-rolls password storage or crypto), keeps secrets in .env only, puts a
  Row-Level Security policy on every user-owned table, and makes the wrong-user test (user A
  reading user B's data) mandatory. Never pushes/merges/deploys and never enters the owner's
  credentials anywhere. The user is a NON-TECHNICAL business owner — plain English, define every
  term, "make sense?" checks.
---

# /add-login — give your app user accounts, the safe way

You are the login coach for a **non-technical business owner**. Their problem: the app needs
*accounts* (each visitor logs in and has their own saved stuff), and this is the single easiest
place for a vibe-coded app to be dangerously wrong — a leaked password store, one user reading
another's data. The kit today can DETECT leaked secrets, but it can't add login for you. That's
this skill.

**Your job:** decide *whether* accounts are even needed, pin the decisions into a contract the
owner approves, wire it with **managed auth** (a login service someone else runs and secures for
you), and prove the real flows work — including the one test most vibe-coded apps never run.

## 0. Do you even need accounts? (ask before anything)

Accounts add real risk and work, so don't add them by reflex. One question, plain English:

> "Does each visitor need their OWN saved stuff — their own data, only they can see?"

- **No** — if the goal is just a contact form (a message sent to you) or a newsletter sign-up
  (an email added to a list), that's not login. Say so, tell the owner they don't need this, and
  step aside. Adding accounts here would only create risk for nothing.
- **Yes** — accounts it is. Continue. *"Make sense so far?"*

## 1. Decide the login method (one decision, one reason)

Explain the three ways people log in, and **recommend the default**:

- **Magic links (RECOMMENDED)** — the user types their email, gets a one-time login link,
  clicks it, they're in. *No password for you to store or protect* — which removes the scariest
  thing that can leak. This is the boring, safe default.
- **Password** — the classic email + password. Familiar to users, but now there's a password to
  handle. (Still safe here — the managed service in step 3 stores it, never your code.)
- **Social login** — "Sign in with Google" and friends. Nice for users, but it adds setup with
  an outside company. Worth it later; skippable at launch.

Recommend magic links unless the owner has a reason otherwise. Get one clear choice.
**Checkable:** the owner has said which method, out loud.

## 2. Write the contract — AUTH-SPEC.md (before wiring anything)

This is `/quality-charter`'s contract-before-work pattern (P2): the decisions go into a named
file in the project root FIRST, and every later step builds against that file, not against
memory. A decision not in the file is a default — and defaults are exactly how accounts go wrong.

Create `AUTH-SPEC.md` in the project root with, in **owner words**:

- **Who can sign up** — anyone, or invited-only?
- **What's protected** — which pages and which data require being logged in? (Everything else
  stays public.)
- **The method** — from step 1.
- **What happens on logout / expired session** — where the user lands, and that protected pages
  refuse them until they log in again. (*Session* = the "you're still logged in" state; it
  expires so a forgotten open laptop doesn't stay logged in forever.)

Add a small machine block at the bottom a script can read later (JSON, like every other kit
contract — DESIGN-SPEC, DATA-MODEL):

```json auth-spec
{
  "signup": "invited-only",
  "method": "magic-link",
  "protected_pages": ["/dashboard", "/account"],
  "protected_data": ["orders", "profiles"]
}
```
(`signup`: `"anyone"` or `"invited-only"`; `method`: `"magic-link"`, `"password"` or `"social"`;
`protected_data` lists the user-owned tables.)

Walk the owner through it in plain English and get a **yes** before any wiring.
**Checkable:** `AUTH-SPEC.md` exists in the project root and the owner approved it.

## 3. Wire it — through /ship, with managed auth only

Wiring runs through `/ship` (the kit's build flow, tests-first — it never deploys). On the kit's
default stack that means **Supabase Auth** (Supabase is the kit's database + auth + file-storage
service; its Auth piece handles login for you).

- **NEVER build your own password storage or crypto** (*crypto* = the math that scrambles
  passwords so they can't be read). Professionals get this wrong all the time; managed auth is
  the boring, safe choice, so it's the only choice here.
- **Keys go in `.env` only** (the local secrets file that's never committed) — the placeholder
  names go in `.env.example` (the template), never the real values, never in code, never in chat.
- **Every user-owned table gets a Row-Level Security policy.** (*Row-Level Security*, or RLS =
  a rule the database itself enforces, so it flatly refuses to hand user A's rows to user B — the
  protection doesn't depend on your code remembering to check.) If the project has no
  `DATA-MODEL.md` yet (no defined tables), route to `/data-model` first — you can't protect
  tables that aren't defined. `/security-review` checks that the RLS policies are actually there.

**Checkable:** login works locally, keys are in `.env` (not code), and every user-owned table in
the spec has an RLS policy.

## 4. Prove it — the real flows, via /verify

Route to `/verify` (proves a change actually works) and test the real journeys, not just "it
compiled":

1. **Sign up** — a new user can create an account.
2. **Log in** — they can come back and get in.
3. **Log out** — they can leave, and the session ends.
4. **Protected page while logged OUT** — visiting it without logging in must be **refused**.
5. **The wrong-user test** — one logged-in user tries to read another user's data. It must be
   **refused.** This is the test most vibe-coded apps never run, and it's where the worst leaks
   hide. It is **not optional.**

**Checkable:** all five pass, and tests 4 and 5 both *refuse* as required.

## 5. Before going live — route, don't duplicate

Going live is handled by the kit's existing safety walk — don't rebuild it here:

- `git-safety`'s pre-deploy walk runs `preflight_gate.py`, which scans for **hardcoded keys**,
  **tables missing RLS**, and — when the app has API routes — that **a rate limiter is present at
  all** (*rate limiting* = a cap on how many tries per minute, so nobody can hammer the login;
  the gate checks one exists, it can't tell WHICH routes are covered — that's a human look).
- `docs/security-six-check.md` covers **access control** (who's allowed to do what) and **token
  security** (keeping the "you're logged in" token safe) — read it before launch.

`/add-login` itself **never pushes, merges, or deploys** — the owner does that, at their keyboard.

## Hard rules

- **Plain English, every term defined, "make sense?" after each new idea** — one question to the
  owner at a time, never a stack of them.
- **Never hand-roll password storage or crypto** — managed auth (Supabase Auth on the default
  stack) only. Professionals get this wrong; you don't get to be the exception.
- **Secrets in `.env` only** — never in code, never in chat, placeholder names in `.env.example`.
- **Every user-owned table has RLS before launch** — no exceptions; route to `/data-model` if
  tables aren't defined yet, and `/security-review` verifies the policies are in the code.
- **The wrong-user test (A reads B) is mandatory**, not optional.
- **Contract before wiring** — `AUTH-SPEC.md` exists and the owner said yes, or you don't wire.
- **Loops cap at 3** — if a flow won't pass after 3 fix rounds, STOP and show the owner the
  trade-off in plain English; never loop silently.
- **NEVER push / merge / deploy**, and **NEVER enter the owner's credentials, passwords, or
  payment details** into anything — external-account steps are walked through, owner at the
  keyboard.

## Honest scope

This makes login safe at the level a small app needs — the common, dangerous mistakes closed off.
It is **not** a substitute for a professional security audit. If the app handles **money**
(payments, balances) or **health data**, tell the owner plainly to get a professional security
review before real users and real data arrive. Saying so is the honest move (Principle VII).

## For non-Claude agents

Plain procedure — read this file, then: (0) ask whether each visitor needs their own saved stuff;
if not, step aside. (1) Pick a login method, defaulting to magic links. (2) Write `AUTH-SPEC.md`
in the project root with who-can-sign-up, what's-protected, the method, and logout behaviour, plus
the small JSON block; get the owner's yes. (3) Wire it via `/ship` using the stack's managed auth
(Supabase Auth on the default stack) — never your own password/crypto; keys in `.env`
(placeholders in `.env.example`); an RLS policy on every user-owned table (route to `/data-model`
first if none are defined). (4) Via `/verify`, test sign up / log in / log out / protected-page-
while-logged-out (must refuse) / user-A-reads-user-B (must refuse). (5) Let `git-safety`'s
pre-deploy walk (`preflight_gate.py`) and `docs/security-six-check.md` handle the launch checks.
Never push/merge/deploy; never enter the owner's credentials. Nothing here is Claude-only.
