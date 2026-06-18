---
name: zoom-out
description: >-
  Go up a level of abstraction and give a higher-level map of an area of code — the relevant
  modules and who calls them — using the project's own domain vocabulary. Use when you're
  unfamiliar with a section of code, need to see how a piece fits into the bigger picture, or
  the user says "zoom out", "give me the big picture", or "how does this fit together".
disable-model-invocation: true
---

# Zoom Out: map the bigger picture before diving in

> Adopted from Matt Pocock's skills (github.com/mattpocock/skills, MIT). A guardrail against
> editing code you don't yet understand — pairs with the constitution rule "Read before you write".

I don't know this area of code well. Go up a layer of abstraction. Give me a map of all the
relevant modules and callers, using the project's domain glossary vocabulary.

## Fit with this project
- Use this BEFORE a `safe-change` edit when the impact isn't obvious — it produces the
  "understand + locate callers" picture that gate depends on.
- Prefer the project's own terms (from `CONTEXT.md` if present, otherwise the spec). Explain
  the map in plain English for a non-technical owner.
- `disable-model-invocation: true` means this only runs when explicitly invoked (`/zoom-out`),
  not automatically — so it never fires unprompted mid-task.
