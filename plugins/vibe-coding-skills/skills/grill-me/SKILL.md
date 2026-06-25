---
name: grill-me
description: >-
  Relentlessly interview the user about a plan or design — one question at a time, with a
  recommended answer for each — until every branch of the decision tree is resolved and you
  reach shared understanding. Use when the user wants to stress-test a plan, pressure-test a
  design, de-risk an idea before building, or says "grill me", "grill my plan", "poke holes",
  or "interview me". Fits BEFORE /speckit-specify or during the brainstorm/clarify stage.
---

# Grill Me: stress-test a plan by interrogation

> Adopted from Matt Pocock's skills (github.com/mattpocock/skills, MIT). The aggressive
> counterpart to Superpowers `brainstorming` — use it when a plan needs hard pressure, not
> gentle exploration.

Interview the user relentlessly about every aspect of this plan until you reach a shared
understanding. Walk down each branch of the design tree, resolving dependencies between
decisions one-by-one. For each question, provide your recommended answer so the user can
just say "yes" when the answer is obvious.

Ask the questions **one at a time**. Wait for the answer before asking the next.

If a question can be answered by exploring the codebase, explore the codebase instead of
asking.

If a question would be answered better with **real evidence** than your memory (e.g. "what stack do
similar apps use?", "how do others build this?"), OFFER to run the **`research-scout`** skill first —
*"Want me to research this before I recommend? (yes/no)"* — and run it only on **yes** (the consent
gate; the owner controls cost/time). Fold its cited findings into your recommended answer. On **no**,
continue.

When the decision tree is resolved, summarize everything you covered in plain English.

## Fit with this project
- Use this in the **brainstorm / clarify** stage of the pipeline — before `/speckit-specify`
  or `/speckit-plan`. It surfaces the unknowns a spec would otherwise miss.
- The user is non-technical: keep each question in plain language, give your recommended
  answer, and explain *why* it matters in one line.
- Honors the constitution rule "Plan before code" — grilling de-risks the plan, it does not
  start the build.
