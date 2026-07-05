# The quality architecture — 8 patterns, with the failures that proved them

This catalog was extracted from three real plugin overhauls (a website copy
pipeline, a website builder, and a blog/LinkedIn pipeline). Each had shipped
weak output despite instructions that looked reasonable on paper — sometimes
because a good session got lucky where a bad one defaulted, sometimes because
most sessions silently skipped the instructions that would have prevented it.
The fix, in every case, was the same architecture. One overhaul's trigger
incident says it all: a site shipped with the default font, a missing image,
and a literal `PLACEHOLDER` form endpoint — **and QA passed it**, because QA
was a discipline, not a mechanism.

**The unifying move: convert adjectives into artifacts.** Every vague quality
wish becomes a file with a lifecycle:

| The wish | The artifact |
|---|---|
| "write good copy" | numbered charter rules R1–Rn |
| "make it look designed" | a machine-parseable spec written before any markup |
| "know the client's voice" | a per-client learnings file, seeded at onboarding |
| "match the bar" | an exemplar folder with fetch-first + banking rules |
| "learn from feedback" | capture-per-round + reconcile + promote |
| "review before presenting" | a scored gate citing rule IDs |

And the one-line method: *read your memory before producing; write your
decisions before executing; gate your output before presenting; check
mechanically what can be checked; compare against banked exemplars; bank every
correction and approval; promote what recurs; and fresh-eyes-review the system
itself.*

---

## Pattern 1 — The charter: numbered, citable rules with failure provenance

**Weakness:** craft knowledge lived in scattered feedback and implicit taste.
Every skill improvised its own standard; reviews argued vibes.

**Mechanism:** one rulebook file, opening "this file is the single source of
truth for HOW X is made." Rules are numbered (R1–R24) so drafts and reviews
can cite them ("fails R3"), grouped by concern, and each carries the real
failure that motivated it ("Why: inward audience-feelings copy was rejected on
a real run as fluffy and unbookable"). Every producing skill names the charter
as binding input.

**Rule:** a rule you can't cite by ID is an opinion; a rule with an ID and a
scar story is a contract. Never renumber existing rules — append.

## Pattern 2 — Contract before generation

**Weakness:** decisions (palette, fonts, copy angle, API shape) were made
implicitly mid-generation, so the model silently defaulted to the safe generic
choice, and nothing downstream could check output against intent — "good" was
unfalsifiable.

**Mechanism:** a spec file written *before* generating, with concrete
falsifiable values instead of adjectives — exact hex colors with a cap on how
many, named fonts with an explicit banned-defaults list, numeric scales — plus
a machine-readable JSON block (JSON: a simple structured data format scripts
can parse) inside the human-readable file. The build step refuses to run
without it; the QA check parses the same JSON and fails the build on mismatch.

**Rule:** before generating any artifact whose quality depends on decisions,
force the decisions into one machine-parseable file. Every downstream step
validates against that file, never against memory. The test: could a
*different* model, with zero taste, read only this file and reproduce the same
decisions? If a decision isn't in the file, it's a default — and defaults are
slop.

## Pattern 3 — Pre-flight brief: forced articulation before production

**Weakness:** key judgment calls (who is this for? what register? what's
off-limits?) were discovered by trial and error in front of the human.

**Mechanism:** a 5-line structured brief written before drafting, embedded at
the top of the draft — buyer, register, owned phrases, hard exclusions,
closest exemplar — each line citing the charter rule it operationalizes, with
a hard stop: "if you cannot fill a line, STOP and go read the missing input."

**Rule:** force the key judgment calls into writing before the expensive work
starts, and make an unfillable line a *blocking* signal. This converts "the
model forgot to consider X" into a checkable artifact.

## Pattern 4 — Deterministic script gates for the mechanical slice

**Weakness:** quality requirements were prose checklists the model self-graded
("✅ Strong hook"). The same judgment that produced a defect re-approves it.
The #1 recurring correction (a banned punctuation habit) recurred forever
because the validator checked structure, never writing.

**Mechanism:** small, dependency-free scripts (Python stdlib — the language's
built-in toolkit, nothing extra to install) that compute the check mechanically — banned-phrase lists, missing-file detection, placeholder
tokens, form endpoints, readability metrics — invoked as a MANDATORY phase
gate: "run script X; all must report PASS before the next phase." Deterministic
by design (identical input → identical output; no timestamps, no randomness),
so they behave the same on any model. Each script's docstring states honestly
what it does NOT check ("taste is NOT checked here — this supplements the
gate, never replaces it").

**Rule:** partition every quality rule into machine-checkable vs judgment-only.
The machine-checkable slice becomes tested, stdlib-only code wired in as a
required command — never a self-certified checkbox. A recurring correction
that could be a regex (a text-search pattern) MUST become one. And state each
validator's scope
honestly so judgment checks are never skipped because "the linter passed."

## Pattern 5 — Scored self-review gate for the judgment slice

**Weakness:** first drafts went straight to the human; her corrections WERE
the QA process. "The strategist's time is the most expensive resource in this
pipeline."

**Mechanism:** a named, mandatory gate between "produced" and "presented":
run the cheap mechanical checks first, then answer a fixed list of concrete,
closed-ended questions derived from the charter (e.g. "cover the logo — does
anything remain that couldn't be any company's site?"), with numeric
thresholds: full marks → present; near → fix and present with honest notes;
below the bar → do NOT present, rework. If the same question fails twice, the
approach is wrong — go back to the spec; don't patch symptoms. Run from a
fresh context where the tool allows: the writer is biased toward its own work.

**Rule:** for judgment-based quality, use a closed-ended scored checklist with
a hard pass bar and a reject-and-rework path. The gate's checklist derives
from the charter so the two can't drift. The purpose is economic: the human
reviews for taste, never for defects. And as one overhaul put it: "a model
with weaker taste should trust the checklist MORE, not less — the questions
encode the judgment so you don't have to have it."

## Pattern 6 — Exemplar banks: approved output as institutional taste memory

**Weakness:** approved deliverables — the only ground truth of "good" —
evaporated after sign-off. Drafts were compared against nothing.

**Mechanism:** per-deliverable exemplar folders with three rules in a README:
(1) fetch-first — loading the closest approved exemplar is step zero, and if
none exists, ask the owner for one thing they consider the bar rather than
drafting blind; (2) banking — on approval, copy the deliverable in with a
one-line header on why it's exemplary ("an approval that isn't banked teaches
nothing"); (3) gate use — final check is side-by-side: "if yours reads like a
competent summary and theirs reads like crafted writing, redraft."

**Rule:** exemplars communicate the bar better than any prose rule, and the
bank compounds with every approval.

## Pattern 7 — Loud, labelled failure — never fabrication, never silent decay

**Weakness:** when inputs were thin, the model invented angles ("invented
angles have failed every time" — three rejected drafts), shipped
placeholder-shaped values that read as real (`formspree.io/f/PLACEHOLDER`),
or silently skipped unreachable sources while implying they were read.

**Mechanism:** three reinforcing layers. (a) Ask-before-inventing: a MANDATORY
named step — confirm real specifics exist, else STOP and ask the user up to 3
targeted questions; "one round of questions beats three rejected drafts"; if
the user says "just write it," proceed from documented facts only and tag
every dramatized line. (b) A small whitelisted set of loud placeholder markers
(`missing-photo`, `missing-asset`…) is the ONLY acceptable placeholder form;
the integrity check fails everything else placeholder-shaped. (c) Status
vocabulary: "couldn't check" is its own status, distinct from PASS and FAIL,
so an unrun check can never report as a passed one; "must go to a human" (FLAG)
is distinct from "auto-fixable" (FAIL) so automation never papers over what it
shouldn't touch.

**Rule:** every input gap gets an explicit branch that does one of exactly two
things — a bounded ask, or a labelled placeholder/flag — and never a
plausible invention. A system that fails loudly and specifically is easier to
trust and debug than one that always looks complete but is sometimes quietly
wrong.

## Pattern 8 — Closed-loop self-evolution with a promotion threshold

**Weakness:** learnings files existed but were append-only piles with live
contradictions, read by almost nothing. Lessons were paid for repeatedly.

**Mechanism:** four verbs, each owned by a numbered step in the workflow —
READ (memory loading is step 1, not an aspiration), CAPTURE (append the lesson
the round the correction happens: "an unbanked lesson is a defect"), RECONCILE
(a distilled Rules layer stays current on top; contradicted entries get marked
SUPERSEDED — never two live conflicting instructions), PROMOTE (a correction
recurring twice MUST be converted into a charter rule or an enforced check,
and marked `[promoted: yes]`). See `self-evolution-loop.md` for the wiring.

**Rule:** self-improvement must be a wired loop with owners, not a folder of
notes — and the promotion threshold is what turns "someone caught this once"
into "this can never happen again."

---

## Three cross-cutting laws

**1. Length degrades compliance — split by when, not what.** A 778-line skill
file was the biggest instruction-compliance load in one plugin: "checklists
that long get partially followed, causing quality drift." The fix: a ~180-line
core (context loading, the one overriding rule, the phase sequence, the hard
gates) + per-phase reference files loaded only when that phase runs — a pure
move, nothing deleted. A MUST-PASS gate buried at line 650 degrades like
everything around it; slimming the core is what makes the gates in it reliable.

**2. Cut by failure mode, not by looks.** After any "nothing was deleted"
refactor, run an independent fresh-eyes diff for dropped *meaning* — that pass
is exactly what caught the one real loss in the slimming above: advisory time
budgets ("faster usually means a phase got rushed"). They look like padding;
they are the only defense against rushing work that has no mechanical check.
Before cutting anything, name the failure it currently prevents and what still
prevents it after the cut. If nothing does, it stays.

**3. Fresh-eyes the rule system itself.** After building any
charter/gate/validator system, a separate fresh-context pass must hunt three
specific bugs: (a) enforcement that flags your own approved patterns — false
positives teach everyone to ignore the gate; (b) prose that overclaims what
the code enforces — drift between doc and checker corrodes trust in both;
(c) rules whose stated scope is broader than intended. Encode each fix as a
test so the exemption's rationale survives.

## Portability footer (include one in every charter)

Everything above is plain Markdown + Python stdlib and runs identically in any
AI tool. Where a step mentions subagents or fresh contexts, it also states the
manual fallback (a deliberate second pass) — **the fallback IS the contract;
richer tooling is an optimization.** One practical corollary: if the plugin's
source repo and its installed copy are separate clones, "the fix was merged"
and "the fix is live" are two different facts — keep a one-command sync script
and the instruction to run it in the top-level agent-facing file.
