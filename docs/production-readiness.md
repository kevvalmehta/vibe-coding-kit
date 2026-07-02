# Production Readiness — the six things a real app needs beyond working code

The 2026-07-02 kit audit found six gaps between "the app works" and "the app is safe to
run for real users". This doc is the canonical source; `git-safety` walks it whenever you
deploy, and CI enforces the parts a machine can enforce. Plain English throughout.

**How to use it:** before a first real deploy, walk all six. Each section says WHAT it
protects you from, the MINIMUM to do, and WHEN you can defer it.

---

## 1. Dependency vulnerability scanning (automatic — CI does this)

**Protects from:** a library you installed having a publicly known security hole
(a *CVE* — a catalogued vulnerability anyone can look up and exploit).

**Minimum (already wired):** the CI pipeline runs `pip-audit` (Python) and `npm audit`
(JavaScript) on every push — it checks your dependency list against the public
vulnerability databases and BLOCKS the build on known-vulnerable versions. A
`dependabot.yml` config makes GitHub open small update PRs weekly so patches arrive as
routine maintenance, not emergencies.

**Defer?** Never — it's free and automatic. If an audit blocks you on a vulnerability
with no fix released yet, pin the version, note it in HANDOFF.md with a revisit date.

## 2. Database migration safety (schema changes without losing data)

**Protects from:** editing a live database's structure and destroying real user data.
The moment real data exists, "just change the table" becomes dangerous.

**Minimum:**
- Change schema ONLY through migration files (Supabase: `supabase migration new <name>`,
  then `supabase db push`) — never by hand-editing the live database. A *migration* is a
  saved, ordered script of the schema change, so every environment applies the exact
  same change and there's a record of what changed when.
- **Additive-first rule:** add the new column/table first, move data, switch the app
  over, and only THEN (a release later) drop the old thing. Renames and drops are the
  data-killers; splitting them into two releases makes each step reversible.
- **Backup before every migration** that touches existing data (see section 4 — one
  command or one dashboard click). A migration with no backup is a bet.

**Defer?** Only while the app has zero real user data.

## 3. Error monitoring (know when the app breaks for a real user)

**Protects from:** the app silently failing for users while you assume it's fine.
(`/monitor` watches AI-output drift only — it does NOT catch crashes; this does.)

**Minimum:** add Sentry (free tier is enough to start): create a project at sentry.io,
`pip install sentry-sdk` (or `npm install @sentry/nextjs`), initialize it with the DSN
key from an environment variable at app startup. Every unhandled crash then emails you
with the exact line and context. Streamlit apps: wrap the main flow so exceptions reach
Sentry before the user sees a plain-English error.

**Defer?** Fine for an internal tool where the users sit next to you. Required before
strangers use the app — they don't report errors, they leave.

## 4. Data backup & restore (git saves your CODE, nothing saves your DATA by itself)

**Protects from:** losing every user's data to one bad migration, bug, or fat-finger.

**Minimum:**
- Supabase paid plans back up daily on their own — check the dashboard (Database →
  Backups) and note the retention window in HANDOFF.md. Free tier: no automatic
  backups — schedule a weekly `supabase db dump -f backup.sql` (or `pg_dump`) and keep
  copies somewhere that is not the same Supabase project.
- **Test the restore once.** A backup you've never restored is a hope, not a backup:
  restore the dump into a scratch project and check a few rows survive the round trip.
- Always take a manual backup right before a migration (section 2).

**Defer?** Only while there's no data anyone would miss.

## 5. Load sanity check (will it survive more than one user at once?)

**Protects from:** the app collapsing the first time 20 people open it together —
or one abusive script hammering an endpoint (that's also security six-check question 6).

**Minimum:** a 5-minute smoke, not a load-testing project: run the app and hit its
heaviest page/endpoint with a short burst — e.g. `npx autocannon -c 20 -d 15 <url>`
(20 concurrent connections for 15 seconds; any similar tool works). If it stays up and
response times are sane, done. If it dies: add caching on the heavy query or a rate
limit before launch.

**Defer?** Internal tools with a handful of known users. Required before a public URL.

## 6. Accessibility & legal basics (only for user-facing apps)

**Protects from:** shipping an app part of your audience literally cannot use, and the
legal exposure that increasingly follows (accessibility lawsuits are real and rising).

**Minimum:** every image has alt text, every form field a visible label, color contrast
readable (no gray-on-gray), the app is usable by keyboard alone (Tab through it once),
and one automated pass with Lighthouse (Chrome DevTools → Lighthouse → Accessibility —
free, takes a minute; fix what it flags red). If you collect personal data from EU/UK
users, you also need a one-page privacy note saying what you store and why.

**Defer?** Internal tools. Required for anything public-facing; trivially cheap to do
from day one versus retrofitting later.

---

## The 30-second pre-deploy recap

| # | Check | Enforced by |
|---|---|---|
| 1 | Dependency audit green | CI (blocking) + Dependabot |
| 2 | Schema changes via migrations, additive-first, backup first | you + `git-safety` reminder |
| 3 | Error monitoring wired (Sentry) | `git-safety` deploy walk |
| 4 | Backups exist AND a restore was tested once | `git-safety` deploy walk |
| 5 | Load smoke on the heaviest endpoint | `git-safety` deploy walk |
| 6 | Alt text, labels, contrast, keyboard, Lighthouse pass | `git-safety` deploy walk |

Related: `docs/security-six-check.md` (security questions asked at plan + audit time),
`/monitor` (AI-output drift after launch), constitution Principle IV (security first).
