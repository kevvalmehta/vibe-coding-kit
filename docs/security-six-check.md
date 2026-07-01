# The Six-Question Security Check

The single source of truth for the kit's security checklist. `/speckit-plan`, `/audit`, and the
`git-safety` deploy guardrail all point here so they never drift apart.

Written for a non-technical owner — every term defined inline, real use-case not analogy.

## Why six questions

Before shipping any app, six things decide whether it's safe. The kit's automated code-scan
(ripgrep + Semgrep) can *prove* three of them, because they're a **bad line of code you can search
for**. The other three are **absence-of-a-thing** problems — nothing bad is written; a protective
thing is simply *missing* — so a search tool cannot spot them. Those rely on a human/AI *remembering*
to build the defence. This checklist makes the kit ask all six, every time.

**The checklist REMINDS. It does not PROVE.** Ticking "yes, we rate-limit" in a plan does not mean
the code actually does — proof comes from the deferred attack-tests below, run when an app goes public.

## The six questions

| # | Question | What it means (plain English) | Can code-search catch it? |
|---|---|---|---|
| 1 | **Authorization** | Can a user see data that isn't theirs? *Use case: user opens `/invoice/41`, edits the URL to `/invoice/42`, and sees someone else's invoice.* | ✅ **Yes** — finds object-by-ID lookups with no ownership check (**IDOR** = Insecure Direct Object Reference) and missing **RLS** (Row-Level Security — the database refusing rows a user doesn't own). |
| 2 | **Rate limiting** | Can someone hammer an endpoint to spam or abuse it? *Use case: a bot tries 10,000 passwords on the login form in one minute.* | ❌ **No** — a *missing* limit is the absence of code; there's no bad line to find. |
| 3 | **Secrets management** | Are API keys, passwords, or tokens exposed in code or committed files? *Use case: a Stripe key pasted into a source file and pushed to GitHub.* | ✅ **Yes** — finds hardcoded key patterns. Fix requires **rotation** (replacing the leaked key — once public it's burned), not just deleting the line. |
| 4 | **Access control** | Can a user tamper with a request to reach something they shouldn't? *Use case: the "is admin" check runs only in the browser, so skipping it reaches the admin page.* | ✅ **Yes** — finds endpoints with no **server-side** identity check / client-only auth. |
| 5 | **Token security** | If a login token is stolen, can it be killed quickly? *Use case: a laptop is stolen with an active session that stays valid for 30 days.* | ⚠️ **Partial** — hardcoded tokens are found, but short expiry + a revoke list (the real defence) is absence-of-code. |
| 6 | **Resilience** | Can one expensive request take the whole system down? *Use case: a single unbounded report query floors the database for every user.* | ❌ **No** — **DoS** (Denial of Service) resistance is a *missing* safeguard, not a bad line. |

**Answer states (per app):** `covered` · `gap` · `not-applicable (+ reason)` · `unanswered`.
Unanswered items are always **surfaced**, never hidden.

## The deferred heavier methods (offered only when an app goes public)

For an **internal tool** (a handful of users behind a login) these are overkill — building them now
is the over-engineering Principle V warns against. They become essential the moment the app is
**public** — open to the internet with real external users.

| Method | What it is (plain English) | Guards questions |
|---|---|---|
| **Per-app attack-tests** | Tests that attack your own app: hit login 1,000× and assert it gets blocked; try to fetch another user's record and assert "denied". Real **proof**, and auto-fails the build if a defence breaks. | 1, 2, 4, 5 |
| **Custom Semgrep rules** | Extra code-scanner rules tuned to *this* app's risky patterns (Semgrep = the automated scanner in your CI gate). | 1, 3, 4 |
| **Live attack scan (DAST)** | Dynamic Application Security Testing — a tool that pokes the *running* app from outside like a hacker, catching holes code review can't see. | 2, 4, 6 |
| **Threat-modeling step** | A short "who would attack this, and how?" exercise done before build, to catch design-level holes early. | all six |

## The public-deploy trigger (owned by `git-safety`)

**Fires when** the owner signals intent to deploy/ship/launch an app **publicly** — by *intent*, not
only the literal word "public" (e.g. "put it live", "on Vercel for everyone", "share the link with
customers").

**Then the deploy guardrail MUST:**
1. Remind the owner — plain English — of the deferred methods above still open.
2. Offer to add per-app attack-tests for the **login** and **money/data** endpoints before go-live.
3. Record the owner's decision (accept or decline) as a conscious, logged choice.
4. **Warn, never block** — declining does not stop the deploy; it is logged.
5. Fire on the internal→public **transition** while items are open; stay quiet on routine re-deploys
   once items are resolved or explicitly declined.
