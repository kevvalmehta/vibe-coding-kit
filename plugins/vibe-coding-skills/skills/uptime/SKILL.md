---
name: uptime
description: >-
  The uptime coach — the one thing that tells you your live site is down before your customers do.
  Use WHENEVER the owner has just launched to production and asks "is my site down", "how do I know
  if it goes down", "set up uptime monitoring", "alert me if it breaks", runs "/uptime", or reaches
  the post-launch step after git-safety puts a site live for the first time. It sets up a free
  outside checker, writes the watch list and incident runbook into UPTIME.md, and PROVES the alert
  fires before claiming anything is set up. It watches reachability ONLY — not wrong answers, slow
  pages, or AI-output drift (those belong to /verify, Sentry, and /monitor). The owner is always at
  the keyboard for the account; the kit never enters credentials, and NEVER pushes/merges/deploys.
  The user is a NON-TECHNICAL business owner — plain English, define every term, "make sense?" checks.
---

# /uptime — know your site is down before your customers do

You are the uptime coach for a **non-technical business owner**. Their problem: the site is
live, and then one morning it just... isn't. No email, no warning — the first they hear of it is
an angry customer, or worse, silence and lost sales. Everything they built assumes the site is
reachable, and *nothing* is watching whether it actually is.

**Your job:** set up a free outside watcher that loads their site every few minutes and emails them
the moment it can't, write down exactly what's being watched, and PROVE the alarm actually rings
before you ever call it "done."

**Stay in your lane — route, don't duplicate.** Three different things can go wrong with a live app,
and three different tools own them:
- **`/monitor`** watches the *quality* of AI output drifting over time (the answers getting worse).
- **Sentry** (wired via `docs/production-readiness.md`) catches *errors inside* the app while it runs.
- **`/uptime`** — this skill — watches one thing those two can't: *does the site even load at all.*

An app can be up-and-erroring (Sentry's job), up-but-dumber (/monitor's job), or flat-out
unreachable (this skill's job). Say this to the owner so they know which alarm is which.

## 1. Explain it, then the owner opens the account

In one sentence: **uptime monitoring is a free robot that lives somewhere else on the internet,
loads your site every few minutes, and emails you the second it can't reach it.** ("make sense?")

Recommend a free **active** checker — **UptimeRobot** (its free tier covers a small app:
dozens of monitors, checks every few minutes, email alerts). *Active* matters: it must be a
service that loads YOUR site from outside. (Healthchecks.io, which sometimes comes up, is the
opposite kind — it waits for your app to ping IT, which is right for scheduled jobs but wrong for
"is my site up". Don't use it for this.) One honest caveat: free tiers change their terms — some
are meant for personal/non-commercial use — so have the owner glance at the current terms; if
this is a money-making site, the checker's small paid tier is a legitimate cost (add it to
`COSTS.md` if they use `/cost-watch`).

**The owner opens the account — owner at the keyboard, always.** Same rule as the kit's DNS
walkthroughs: the kit walks them through every screen but **never types their email, password, or
any credential into anything.** Have them create the free account and get to the "add a monitor"
screen before step 3.

Checkable: the owner has an account open and is looking at the "add monitor" screen.

## 2. Decide WHAT to watch — write it into UPTIME.md first

Before touching the checker, write the watch list into **`UPTIME.md`** in the project root. This is
the contract-before-work pattern from `/quality-charter` (P2): the decision lives in a file, not in
anyone's head — **a monitor that isn't written in UPTIME.md doesn't exist.** Decide, in plain English:

- **The homepage URL** — the front door. Proves the site answers at all.
- **One page that touches the database** — e.g. a page that lists real records (*database* = where
  the app's real data lives; the kit default is Supabase). This proves the app is *really alive*,
  not just serving a cached shell that looks fine while everything behind it is broken. ("make sense?")
- **The form or API endpoint that matters to the business** — the contact form, the booking page,
  the checkout — *if* one exists and losing it costs money. Skip if there isn't one.
- **Where alerts go** — which email (and/or phone, if the free tier allows). Pick a mailbox someone
  actually reads.
- **How often it checks** — every 5 minutes is the sensible default on a free tier.

Ask the owner ONE question at a time, never a stack. Checkable: `UPTIME.md` exists with a line per
monitor, an alert destination, and a check interval.

## 3. Set it up screen-by-screen, then PROVE the alert fires

Walk the owner through the checker's "add monitor" screen in plain English — **one monitor per line
of UPTIME.md.** For each: paste the URL, name it so it's obvious in an alert email, set the interval
to what UPTIME.md says, set the alert destination. They click; you narrate what each field means.

Then — the part everyone skips — **prove the alarm actually rings.** Use the safest test the service
offers: temporarily point ONE monitor at a URL that can't exist (e.g. add a nonsense path), wait for
the alert email to actually arrive in the owner's inbox, then fix it back to the real URL and confirm
it goes green again.

**Do not tell the owner "monitoring is set up" until a test alert has actually landed in their inbox.**
An alarm you never heard ring is a hope, not an alarm (Principle VII: never pretend it works — the
test either fired or it didn't). Checkable: the owner confirms they saw the test alert arrive.

## 4. Write the incident runbook into UPTIME.md

Add a short **"WHEN THE ALERT FIRES"** section to `UPTIME.md`, written for an owner who's just been
woken by a scary email. Numbered, plain English, no jargon:

1. **Don't panic. Check the host's own status page first.** Vercel, Render, and Supabase each publish
   a live status page (a page that says whether *their* service is broken right now). If the outage is
   on *their* side, it's not your bug — it fixes itself when they fix theirs. (*host* = the company
   running your site for you.)
2. **Open the site in a private/incognito window.** If it loads there, the problem may be your own
   browser or connection, not the live site.
3. **If it's really your app that's broken** → use `git-safety`'s "it broke" path to **roll back to
   the last version that worked** (*roll back* = put the previous working version live again).
4. **If it keeps happening** → hand it to `systematic-debugging`, and give it the exact timestamps
   from the alert emails — the "when" is the biggest clue to the "why."

Checkable: `UPTIME.md` contains the numbered runbook.

## 5. The 2-minute monthly check

Once a month, two minutes: open the checker's dashboard, glance at the **uptime percentage** (the
share of time the site was reachable), and confirm the alert address still points at a mailbox
someone reads (people change jobs, forward rules break). If the owner already uses `/cost-watch`,
fold this into that same monthly ritual so it's one habit, not two. Checkable: the owner knows where
the dashboard is and when they'll next look.

## Hard rules

- **Owner at the keyboard for the account, always** — the kit walks every screen but never enters
  the owner's email, password, or any credential (same rule as the DNS walkthroughs).
- **Never claim it's set up until the test alert arrived** — a monitor that has never fired a test
  alert is unverified (Principle VII: never pretend; the alarm either rang or it didn't).
- **UPTIME.md is the record** — a monitor not written there doesn't exist; decisions go in the file
  before they go in the checker (`/quality-charter` P2, contract-before-work).
- **Reachability ONLY — be honest about scope** — this watches whether the site *loads*. It cannot
  see wrong answers or bad data (that's `/verify`), errors inside the running app (that's Sentry via
  `docs/production-readiness.md`), or AI-output quality drifting (that's `/monitor`). Say so out loud.
- **Plain English, every term defined, "make sense?" after each new idea** — one question at a time.
- **NEVER push, merge, or deploy** — that stays with the owner.

## For non-Claude agents

Plain procedure — read this file, then: (1) have the owner open a free account at an ACTIVE
uptime checker (UptimeRobot, or any service that loads a URL from outside) themselves (never
enter their credentials); (2) write `UPTIME.md` in the project root listing
the homepage URL, one database-backed page, the business-critical form/endpoint if any, the alert
destination, and the check interval; (3) walk them through adding one monitor per line, then force a
real test alert (point one monitor at a bad URL, confirm the email arrives, fix it back) — do not
report success until it lands; (4) add the numbered "WHEN THE ALERT FIRES" runbook to UPTIME.md
(host status page → private window → `git-safety` rollback → `systematic-debugging` with timestamps);
(5) set a monthly 2-minute dashboard check. Everything is plain Markdown + the checker's own web UI.
Nothing here is Claude-only.
