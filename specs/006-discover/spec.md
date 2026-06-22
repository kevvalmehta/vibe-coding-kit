# Spec — Discover (the pre-spec reality check)

## Why (problem)
The kit is strong at *building the thing right* (spec → plan → TDD → review → gates) but has **no step
that asks whether the thing is worth building at all**. An owner can take a pure hunch straight to
`/speckit-specify` and the kit will flawlessly build something nobody wants. Nothing grounds the idea in
what real people say, ranks which need is most worth solving, or forces an answer to "once it's built,
how does one human find it?" `grill-me` pressure-tests a *plan*; it does not validate the *problem*.

This gap is exactly what the external `vibe-check` skill (TexasBedouin, MIT) covers. We adopt the
*method*, not the code — rebuilt natively in the kit's voice and registered (Constitution VI), the same
way ponytail became `/lean-review` + `/lean-debt`.

## What (outcome)
`/discover` — a read-only advisor that runs **before `/speckit-specify`**. It takes an idea (even vague),
checks whether the problem is real and worth building using evidence from what people actually say, and
ends with a plain-English verdict plus a grounded hand-off to `/speckit-specify`.

Output, written to a `discovery/<NNN>-<slug>.md` note (mirrors how `/audit` writes to `audit/`):
- **Verdict** — one of: *real & worth building* / *real but aim elsewhere* / *not enough evidence — go look first*.
- **Ranked underserved needs** with evidence tags.
- **V1 cut** — the one thing to win on + the basics that can't be skipped.
- **First 10 users** — the specific people/place, or a flag that this is the riskiest open question.
- A ready-to-paste **problem statement** for `/speckit-specify`.

It never edits source code and never writes the spec itself — it hands off.

## Scope

### Phase A — the spine (build + ship first)
1. **Grill the problem** — who exactly hurts, the worst moment, today's workaround, why existing tools
   miss, why now. The pain, not the features.
2. **Cast a wide net (pain-mining)** — Reddit (raw venting) + reviews of tools people already pay for
   (G2/Capterra/Trustpilot/app stores). Uses a **fetch ladder**: web-search with `site:` first → read
   endpoints → if nothing loads, hand the owner exact searches to paste back. **Never fabricate
   findings** (Constitution VII / truth-over-confidence). Honest about being directional, not statistical.
3. **Score the gaps (ODI) + competitor matrix** — per need, rate Pain (1–10) and how well today's tools
   serve it (1–10); `Opportunity = Pain + max(0, Pain − Served)`. Rank. Tag each *seen-it / hunch / guess*.
   Build a small competitor matrix (needs × real alternatives, incl. "do nothing").
4. **Cut V1 + name first-10-users** — V1 = top-scoring underserved need (the differentiator) + the
   high-Pain/well-served basics (table stakes). Everything else → V2. Then force a specific first-10-users
   answer and channel; if they can't name it, flag it as the idea's riskiest part.

### Phase B — additions (built after Phase A is shipped, as their own sections)
5. **Growth-loop finder** — does using the app recruit the next user (content / invite / signal loop)?
   Draw it; put its enabling feature on the V1 list; name the one cheap metric that proves it spins.
   Honest escape hatch: if there's no real loop, say so and lean on the Phase A channel.
6. **Marketplace / cold-start** — detect two-sided ideas, discover *both* sides, name the harder side,
   and a cold-start plan + minimum-liquidity threshold so it doesn't launch into an empty room.

### Deliberately dropped (kit already covers — do NOT port)
Build-time checkpoints, GitHub/deploy teaching (`git-safety`, `GITHUB-GUIDE.md`), code-checkup
(`/audit`, `/health`, `/lean-review`), managing-the-AI (constitution + TDD-Guard + `verification-before-completion`),
the HTML diagram engine, the interactive PRD, and the 20-section plan doc (`/speckit-specify` → `/plan` → `/tasks`).

## Functional requirements
- **FR-001:** A single `SKILL.md` (prose skill, like `guide`/`audit`) — no scripts. Frontmatter description
  carries trigger phrases ("discover", "validate my idea", "is this worth building", "who wants this",
  "pain mining", `/discover`) and the NON-TECHNICAL-owner note.
- **FR-002:** Read-only on source code. Its only writes go to `discovery/`. It never runs `/speckit-specify`
  itself — it ends by handing off.
- **FR-003:** The fetch ladder degrades gracefully and **must not invent quotes/sources**; when it can't
  fetch, it asks the owner to paste results. Every kept need is tagged *seen-it / hunch / guess*.
- **FR-004:** Phase B sections are additive and self-contained, so Phase A ships and works without them.

## Success criteria
- **SC-001:** Given a vague idea, `/discover` produces a verdict + ranked needs + V1 cut + first-10-users,
  in plain English, then names `/speckit-specify` as the next step with a paste-ready problem statement.
- **SC-002:** When web fetches fail, it never fabricates — it falls back to the paste-back path and says so.
- **SC-003:** Registered everywhere (Constitution VI) in BOTH repos: see Propagation. The README File-index
  CI gate (`check_inventory.py`) stays green.
- **SC-004:** `/guide` routes idea-validation intent to `/discover`, slotting it before `/speckit-specify`.

## Architecture
One `SKILL.md`, stdlib of the kit's own conventions: numbered STEPs, hard rules, plain English, read-only,
explicit hand-off. No new scripts, no CI step. Slots in the flow as:
`idea → /guide → /goal → idea-to-app → /discover → grill-me → /speckit-specify → …`

## Propagation (Constitution VI — "not done until registered in BOTH repos")
Lands in:
- **Skill:** PCK `.claude/skills/discover/SKILL.md` + VCK `plugins/vibe-coding-skills/skills/discover/SKILL.md`.
- **This spec:** `specs/006-discover/spec.md` in both repos.
- **Docs (both repos):** `AGENTS.md`, `SKILL-MAP.md`, `guide` routing table + normal-order line, `README.md`
  File index (required by the CI gate), and `HANDOFF.md` (PCK).
- **VCK only:** bump plugin version (`plugins/vibe-coding-skills/.claude-plugin/plugin.json` 0.2.1 → 0.3.0).
- **Not** `.agents/skills/` — workflow skills (guide/audit/health/lean-*) live in `.claude/skills/` + plugin
  only; only `speckit-*` and `goal` are mirrored to `.agents/skills/`. `/discover` follows the workflow pattern.
