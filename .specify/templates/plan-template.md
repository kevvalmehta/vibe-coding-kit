# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]

**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/speckit-plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

[Extract from feature spec: primary requirement + technical approach from research]

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: [e.g., Python 3.11, Swift 5.9, Rust 1.75 or NEEDS CLARIFICATION]

**Primary Dependencies**: [e.g., FastAPI, UIKit, LLVM or NEEDS CLARIFICATION]

**Storage**: [if applicable, e.g., PostgreSQL, CoreData, files or N/A]

**Testing**: [e.g., pytest, XCTest, cargo test or NEEDS CLARIFICATION]

**Target Platform**: [e.g., Linux server, iOS 15+, WASM or NEEDS CLARIFICATION]

**Project Type**: [e.g., library/cli/web-service/mobile-app/compiler/desktop-app or NEEDS CLARIFICATION]

**Performance Goals**: [domain-specific, e.g., 1000 req/s, 10k lines/sec, 60 fps or NEEDS CLARIFICATION]

**Constraints**: [domain-specific, e.g., <200ms p95, <100MB memory, offline-capable or NEEDS CLARIFICATION]

**Scale/Scope**: [domain-specific, e.g., 10k users, 1M LOC, 50 screens or NEEDS CLARIFICATION]

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

[Gates determined based on constitution file]

## Running cost implications

*Call out anything in this plan that costs money per-usage at scale — not one-time build cost, but
cost that grows with usage. The owner approves these before build, not after the bill arrives.*

- **Realtime listeners** (e.g. Supabase Realtime, WebSockets): [one-line plain-English cost note, or "N/A"]
- **LLM API calls** (e.g. Claude, OpenAI): [one-line plain-English cost note, or "N/A"]
- **Image/file storage + bandwidth** (e.g. Supabase Storage, S3, CDN egress): [one-line plain-English cost note, or "N/A"]
- **Per-seat services** (e.g. per-user pricing on a hosted tool): [one-line plain-English cost note, or "N/A"]

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit-plan command output)
├── research.md          # Phase 0 output (/speckit-plan command)
├── data-model.md        # Phase 1 output (/speckit-plan command)
├── quickstart.md        # Phase 1 output (/speckit-plan command)
├── contracts/           # Phase 1 output (/speckit-plan command)
└── tasks.md             # Phase 2 output (/speckit-tasks command - NOT created by /speckit-plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
# [REMOVE IF UNUSED] Option 1: Single project (DEFAULT)
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# [REMOVE IF UNUSED] Option 2: Web application (when "frontend" + "backend" detected)
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# [REMOVE IF UNUSED] Option 3: Mobile + API (when "iOS/Android" detected)
api/
└── [same as backend above]

ios/ or android/
└── [platform-specific structure: feature modules, UI flows, platform tests]
```

**Structure Decision**: [Document the selected structure and reference the real
directories captured above]

## Background Work

<!--
  ACTION REQUIRED: Fill this ONLY if the app does work OUTSIDE a direct request/response —
  i.e. something runs on a schedule, reacts to an event, or happens after the user has
  moved on. Examples: sending a weekly summary email, refreshing a cached report every
  hour, notifying someone when a new row appears, processing an uploaded file in the
  background.

  MOST simple apps (a form, a dashboard, a CRUD tool) have NO background work.
  If that is the case here, write "None" and DELETE the table below.

  Vocabulary borrowed from the iii project (github.com/iii-hq/iii) — a plain-English way to
  describe each piece of background work in three words. We borrow ONLY the words, not the
  engine; the "Worker" column stays in our own stack (Supabase Edge Functions, Vercel cron,
  Supabase DB webhooks).

    - Worker   = what runs the work   (e.g. Supabase Edge Function, Vercel cron)
    - Function = the unit of work     (e.g. "send weekly summary email")
    - Trigger  = what kicks it off    (e.g. cron schedule, a database row change, a queue message)
-->

| Worker (what runs it) | Function (the unit of work) | Trigger (what kicks it off) |
|-----------------------|-----------------------------|-----------------------------|
| [e.g. Supabase Edge Function] | [e.g. send weekly summary email] | [e.g. cron — every Monday 08:00] |
| [e.g. Supabase DB webhook] | [e.g. notify on new signup] | [e.g. row inserted in `users`] |

> If this table is empty, the app has no background work — that is the common, simple case.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
