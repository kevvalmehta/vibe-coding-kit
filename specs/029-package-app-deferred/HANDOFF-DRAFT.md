# FUTURE SKILL DRAFT — /package-app (mobile + desktop packaging)

> **Status: NOT BUILT.** This is a handoff note for whenever the owner has a mobile or desktop
> app ready to ship, not a working skill. Do not register this anywhere (SKILL-MAP, README,
> `/guide`, etc.) until the SKILL.md itself is actually written. Delete this file once that
> happens — its content should have migrated into the real skill + its references.

## Why this doesn't exist yet (2026-07-05 decision)

The kit's `/scaffold` only knows how to start a **website or web app** (`streamlit`, `fastapi`,
`python-script`, `nextjs`, `static-site`) — everything ships to a URL. Nothing in the kit covers
the other two shapes an app can take:

- **Mobile app** — installs from the App Store / Google Play, gets its own home-screen icon.
- **Desktop app** — installs and runs directly on a Mac or Windows computer, not in a browser
  (think a Slack or Notion desktop app, not their websites).

This was surveyed as gap item 6 in the 2026-07-05 full-kit audit (see memory `vibe-kit-gap-roadmap`)
and deliberately DEFERRED — unlike the five gap-fillers that shipped that day (`/data-model`,
`/add-login`, `/wire-up`, `/uptime`, `/cost-watch`), packaging involves real friction the kit
doesn't touch anywhere else: paid developer accounts, app-store review queues, code-signing
certificates, and a genuinely different build toolchain per platform. Building it speculatively,
before a real app needs it, risks guessing wrong about which toolchain actually matters.

## The trigger — when to actually build this

**Build `/package-app` the first time the owner has a real app they want on a phone or desktop**,
not before. At that point:
1. Confirm which platform(s): iOS, Android, both (cross-platform), Mac, Windows, or both.
2. Author the skill following the kit's contract-before-work house pattern (same shape as
   `/design-craft`, `/data-model`, etc. — see any of those SKILL.md files as the exemplar).
3. **Nudge the owner explicitly** about the parts that are NOT like a website launch — they will
   not expect these from the kit's usual "free tier, boring stack" pattern:
   - **Paid developer accounts are mandatory, not optional.** Apple charges ~$99/year, Google
     charges a one-time ~$25 fee. Neither has a free tier — this breaks the kit's usual promise
     of a free path to launch.
   - **App-store review is a real gate the kit cannot walk for the owner.** Apple's review can
     take days and can reject an app for reasons that feel arbitrary (design guidelines, missing
     privacy disclosures). This is the first place in the kit's whole flow where "the owner
     approves, then it's live" doesn't hold — a THIRD PARTY approves too.
   - **Code signing** is a new concept with no web equivalent — a certificate proving the app
     really came from the owner, without which app stores won't accept it. The kit should
     explain it in one plain sentence and route the setup, not skip it.

## Draft shape for the future skill (not finalized — a starting point)

- **Role**: the packaging coach. Owner's problem: their app now needs to be an actual installable
  thing on a phone/desktop, and that world has none of the free-tier safety nets the rest of the
  kit relies on.
- **Step 0**: confirm platform(s) + whether this is a NEW app (needs Expo/React Native or
  Electron/Tauri scaffolding from the start) or an EXISTING web app the owner wants wrapped
  (there are real tradeoffs here — a wrapped web app is faster to ship but feels less native;
  say so honestly).
- **Recommended defaults** (to verify at build time — mobile/native tooling moves fast):
  - Mobile, cross-platform, non-technical-friendly → **Expo** (React Native) — write once, run on
    iOS + Android; has a managed build service so the owner doesn't need Xcode/Android Studio.
  - Desktop, web-app-derived → **Tauri** (lighter) or **Electron** (more mature, heavier) —
    wraps the existing web app into a native window.
- **The contract file**: `PACKAGING.md` — platform(s), the developer accounts needed (with costs),
  app store listing basics (name, icon, description — the owner's own words), and the signing/
  certificate status. Same contract-before-work pattern as every other kit skill.
- **Hard rules to carry over**: owner creates and holds every developer account themselves (never
  the kit); the kit walks screens, never enters credentials or payment details (same rule as
  `/wire-up`, `/uptime`, `/cost-watch`); NEVER submits to a store on the owner's behalf without
  an explicit final "yes, submit this"; honest scope that review timelines and rejection reasons
  are outside the kit's control.
- **Where it plugs into the kit**: `/stack`'s escape hatch (line ~72-79 of `stack/SKILL.md`)
  currently sends anything exotic to `research-scout` + `/discover` — once this skill exists,
  `/stack` should recognize "mobile app" / "desktop app" as first-class options routing here
  instead of the escape hatch.

## Reminder mechanism

This file itself is the reminder — the AI mentor should proactively surface it (read this file,
summarize the "why not yet" + "build it now" trigger in plain English) the next time the owner:
- says anything about "app store", "Play Store", "phone app", "desktop app", "installer", "download
  my app", or similar, OR
- reaches `/stack`'s escape hatch for a mobile/desktop request.

When that happens: tell the owner packaging isn't built yet, explain the real-world differences
above in plain English (paid accounts, review process, code signing), confirm they actually want
to build it now, then follow the draft shape above to author the real skill (same registration
ritual as every other skill: SKILL-MAP, README, QUICKSTART, `/guide`, HANDOFF, `check_inventory.py`
green).
