# Decision routine — detail + a worked golden example

This is the detailed recipe behind `SKILL.md`, plus one fully worked example so the output shape is
unambiguous.

## The routine, condensed

1. **AI-inside?** No → decline, hand back. Yes → continue.
2. **Jobs:** list the distinct jobs the AI does.
3. **Structure:** multi-job → orchestrator + one small agent per job; single-job → one agent.
4. **Model per agent:** mechanical → Haiku (+ reason); judgment → default tier.
5. **Managed vs API:** suggest one with a reason; owner decides.
6. **Approval gates:** name actions that always need human sign-off.
7. **Checklist:** pre-fill all 13 factors of `docs/ai-feature-checklist.md` (tick+reason or N/A+reason).
8. **Diagram:** simple text diagram of agents + flow.
9. **Reminder:** recommendation only; scaffolding is deferred.
10. **Grill:** offer + run `grill-me` by default; skip only on explicit decline.

---

## Worked golden example

**Idea (owner's words):** "A tool that researches a topic, drafts a blog post about it, and emails the
draft to me for approval."

### Step 0 — AI-inside?
Yes — it researches, drafts, and decides what to send. Proceed.

### Step 1 — Jobs
1. Research the topic. 2. Draft the post. 3. Classify/clean the research (mechanical). 4. Email the draft.

### Step 2 — Structure (recommended)
**1 orchestrator + 3 focused subagents** (one per real job). The orchestrator sequences them and holds
state; each subagent does one job (12-factor #10).

```
            ┌─────────────────────────┐
            │      Orchestrator       │  (default tier — sequences jobs, holds state)
            └───────────┬─────────────┘
        ┌───────────────┼───────────────────────┐
        ▼               ▼                        ▼
  ┌───────────┐   ┌───────────┐           ┌──────────────┐
  │ Research  │   │  Drafting │           │   Export /    │
  │  agent    │   │   agent   │           │   Email agent │
  │ (default) │   │ (default) │           │ (Managed)     │
  └─────┬─────┘   └───────────┘           └──────┬───────┘
        ▼                                        ▼
  ┌───────────┐                          ⛔ HUMAN-APPROVAL GATE
  │ Classify/ │                          (owner approves before any email is sent)
  │ clean     │
  │ (Haiku)   │
  └───────────┘
```

### Step 3 — Model per agent
- Research → **default tier** (judgment: what's relevant).
- Classify/clean research → **Haiku** (mechanical tidy-up — don't pay premium).
- Drafting → **default tier** (judgment: quality writing).
- Email/export → **default tier** for the message, but see Step 4 (it's long/async → Managed).

### Step 4 — Managed vs API
**Recommend a Managed Agent for the export/email job because** it runs after the owner has moved on
(async) and benefits from hosted pause/resume. The other jobs are short request/response → **Messages
API** is fine. **You decide.**

### Step 5 — Approval gates
**Sending the email ALWAYS needs the owner's approval** (it leaves the system). Nothing is sent
without an explicit yes.

### Step 6 — 12-factor checklist (pre-filled, abbreviated)
- #1 NL→structured: ✓ each agent emits structured output (research notes, draft, send-or-not).
- #2 own prompts: ✓ one prompt file per agent in the repo.
- #7 human-as-tool: ✓ email send is an approval gate (Step 5).
- #8 own control flow: ✓ orchestrator sequences jobs in code; LLM decides inside steps.
- #10 small agents: ✓ 3 focused subagents, not one giant agent.
- #13 pre-fetch: ✓ hand the research to the draft agent up front.

> _Abbreviated here for space — in a real run, fill in ALL 13 factors (every numbered item plus the
> bonus Factor 13), each with a tick+reason or an explicit N/A+reason. Don't trail off._

### Step 7 — Diagram
See above.

### Step 8 — Reminder
Recommendation only — no code generated. Scaffolding (prompt files + tool stubs for the 3 agents) is a
**deferred** next step; ask when ready to build.

### Step 9 — Grill
Offer + run `grill-me` on this design by default (e.g. "should classify+research be one agent? is email
really async? what if research returns nothing?"). Skip only if the owner explicitly declines.
