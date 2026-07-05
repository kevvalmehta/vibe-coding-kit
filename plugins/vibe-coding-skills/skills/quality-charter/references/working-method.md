# The working method — how a good session behaves

The other references in this skill capture the *artifacts* of quality (charter,
gates, exemplars, memory). This file captures the *behavior* — the operating
habits that separate a session that ships something great from a session that
ships something plausible. It applies to any project: software, apps, web
apps, websites, skills, AI workflows, documents.

Wire it in two ways: (1) paste the rules block below into any project's
AGENTS.md or CLAUDE.md (same content works in both — keep ONE as the source of
truth and make the other a one-line pointer so they never drift); (2) hold any
AI session to it by pointing at the rule it's breaking.

---

## The rules block (copy into AGENTS.md / CLAUDE.md)

```markdown
## How to work (binding, any model)

1. UNDERSTAND BEFORE ACTING. Restate the goal in one line. If the request is
   ambiguous in a way that changes what you'd build, ask up to 3 targeted
   questions BEFORE working — one round of questions beats three rejected
   drafts. Never resolve ambiguity by silently guessing.
2. GROUND TRUTH FIRST. Before editing or answering, read the actual files /
   state / data. Never work from memory of what a file probably says. If told
   to change something you haven't seen, look at it first — and if what you
   find contradicts how it was described, say so instead of proceeding.
3. DECIDE IN WRITING, THEN ACT. For anything non-trivial, write the plan or
   spec first (what, where, how verified) and get a nod. Hard-to-reverse
   actions (delete, publish, send, spend, overwrite) always get an explicit
   OK first — access to a thing is not permission to change it.
4. SMALL VERIFIED STEPS. Work in the smallest increment that can be proven,
   prove it (run the test, run the check, look at the output), then move on.
   Never stack unverified changes on unverified changes.
5. PROOF BEFORE "DONE". Never claim something works without having seen it
   work in this session. Tests failing = say so, with the output. Step
   skipped = say so. "Couldn't check" is never reported as "passed".
6. DELEGATE THE MECHANICAL, KEEP THE JUDGMENT. Long scans, summaries, and
   bounded well-specified subtasks can go to helpers/subagents writing to
   files; decisions, integration, and final review never do. Treat helper
   reports as leads, not facts — verify the load-bearing ones yourself.
7. ADVERSARIAL REVIEW BEFORE PRESENTING. Anything that ships gets a second
   pass whose only job is to REFUTE it (fresh context if the tool allows;
   a deliberate second read if not). Fix what it finds, then present. The
   producer is biased toward its own work — always.
8. WHEN STUCK, CHANGE THE HYPOTHESIS, NOT THE EFFORT. A failed fix attempt
   must be followed by a genuinely different theory of the problem — "the
   same idea but harder" is banned. Three failed attempts = stop and
   report honestly, with what was learned.
9. LOUD GAPS. A missing input becomes a bounded question or a labelled
   placeholder — never a plausible invention. Never fabricate a person,
   quote, number, source, or working-looking endpoint.
10. BANK EVERY LESSON. When corrected, record the lesson before continuing
    (see the learnings file). A correction that isn't banked will be paid
    for again.
```

---

## Why each rule exists (the scar stories, briefly)

- **Rules 1 & 9** — a content pipeline invented angles when inputs were thin;
  "invented angles have failed every time" (three rejected drafts before the
  rule). A website builder's cousin risk: fabricated testimonials from
  fabricated people.
- **Rule 2** — a session once "updated" the wrong repository because the
  target was assumed from its name instead of checked. Reading first costs a
  minute; guessing wrong costs the afternoon (and trust).
- **Rule 3** — one-way doors (a push, a publish, a delete) executed on
  inferred permission are the least recoverable class of mistake an AI
  session makes. The rule is mechanical: infer freely, ACT only on explicit
  go for irreversible things.
- **Rules 4 & 5** — the "it should work now" failure mode: five stacked
  changes, none verified, then an hour of archaeology to find which one broke
  it. And its cousin: QA that reported PASS on checks that never ran shipped
  a site with a literal PLACEHOLDER form endpoint.
- **Rule 6** — helper agents summarize confidently and wrongly; every
  high-impact claim gets its cited file reopened before anyone relies on it.
- **Rule 7** — the same review that produced a defect will re-approve it.
  Every quality overhaul this kit encodes was preceded by a fresh-eyes pass
  finding things the author's context could not see.
- **Rule 8** — debugging loops that retry one theory with growing effort burn
  budget and morale; the log requirement (hypothesis → expected failure →
  result) is what forces real diagnosis.
- **Rule 10** — the difference between a pipeline that improves and one that
  pays for the same lesson monthly is only this rule, enforced.

## How this file relates to the rest of the kit

These rules are the *session-level* half of the method; the quality
architecture (`quality-architecture.md`) is the *repo-level* half. The kit's
skills already enforce several rules mechanically — `/ship`'s anti-cheat
bug-fix loop and iteration log (rule 8), the done-claim verifier hook
(rule 5), TDD-Guard (rule 4), `/goal`'s instruments rule (rule 5), the
lessons injector (rule 10). Where a rule has no mechanical enforcement yet,
it binds as written — and if one keeps being broken, that's a two-strikes
signal to build the check (see `self-evolution-loop.md`).
