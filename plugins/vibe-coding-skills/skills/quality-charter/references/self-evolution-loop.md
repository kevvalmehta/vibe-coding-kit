# The self-evolution loop — wiring memory so lessons are paid for once

A learnings file that nothing reads is a graveyard. The loop below is what
separates "we wrote the feedback down" from "this can never happen again."
Four verbs; each one is a **numbered step in a skill**, owned, not aspirational.

## The four verbs

### READ — step 1 of every producing skill

Before any work: load the charter, the skill's learnings Rules layer, the
instance-specific learnings (per-client/per-project), and the closest
exemplar. Loading memory is a workflow step with a number, not a habit you
hope for. If a skill can produce output without having read memory, the loop
is broken at the root — most failed pipelines fail exactly here (in one
audited plugin, only 2 of 8 skills read any learnings at all).

### CAPTURE — the round the correction happens, not at the end

When the owner corrects anything, append the lesson BEFORE redrafting:
- the generalizable craft lesson → the skill's learnings file
- the instance-specific lesson → the client/project learnings file

"An unbanked correction is a defect" — treat it with the same severity as a
failing test. End-of-session retros lose half the lessons; capture-per-round
loses none. Also bank approvals: on sign-off, copy the deliverable into the
exemplar folder with one line on why it's the bar.

### RECONCILE — never two live contradicting instructions

Learnings files have two layers:

```markdown
## Rules (current — apply all of these)
- <distilled, deduplicated, currently-true rules>

## Feedback log (history — dated, append-only)
- 2026-07-04 <client> — <what was corrected, verbatim-ish> [promoted: no]
- 2026-06-28 <client> — <…> — SUPERSEDED 2026-07-04 (see Rules #3)
```

New lesson contradicts an old rule? Rewrite the rule, mark the old log entry
SUPERSEDED with a date. An append-only pile accumulates live contradictions,
and a model reading contradictions picks one at random — the file becomes
noise with the authority of memory.

### PROMOTE — the two-strikes rule

When the same correction appears **twice** (any client, any project), it must
move up the hierarchy — and the entry gets marked `[promoted: yes]`:

    feedback log → skill Rules → charter numbered rule → validator script

Each hop makes the lesson harder to ignore: a log line can be skimmed past, a
charter rule gets cited at the gate, a validator makes the mistake impossible.
The endpoint of a mature lesson is code. Real examples: "write the spec file
first, always" became a linter that fails the build without one; "QA that only
checks links will ship broken sites" became an integrity script that catches
missing images and placeholder endpoints.

## Seeding — memory channels exist from day one

Create the learnings files at project/client setup, empty but with the layer
headers in place. A channel that doesn't exist won't be written to mid-crunch.
The exemplar folder starts with just its README (fetch-first rule inside) —
it fills through banking, not through pre-population.

## Scope separation

Two files, two scopes, never mixed:
- **Skill/craft learnings** — generalizable; travels to every future project.
- **Client/project learnings** — instance-specific corrections ("this client
  hates the word 'journey'"); read only when working that instance.

Mixing them either leaks one client's quirks into everyone's output or buries
universal lessons in instance noise.

## The meta-loop: fresh-eyes the system itself

After building or materially changing the charter/gates/validators, one
separate pass (fresh context if available) hunts three specific bugs:

1. **Self-flagging:** enforcement that fires on the owner's own approved
   patterns. False positives teach everyone to ignore the gate — each
   exemption added gets a test carrying its rationale.
2. **Overclaiming prose:** documentation that says the script checks more
   than it does. Drift between doc and code corrodes trust in both — correct
   the wording to match the code exactly.
3. **Scope inflation:** rules claiming to bind more than intended
   ("every skill" when three are exempt). Rescope explicitly.

And after any refactor that claims "nothing was deleted": an independent
content-loss diff, old vs new, looking for dropped *meaning* — not just
surviving headings. That pass is not optional; it is the only thing that has
ever caught the quiet losses.
