# Packaging: shipping and exporting a behavior pack

## v1 is a repo skill — plugin packaging is deferred

The distillation workflow lives as plain-text repo files on purpose: inspectable,
diffable, portable across AI tools, and provable with the repo's own tests.
Deferral rule: no global plugin, marketplace listing, or Codex plugin packaging
until (a) at least one pack has passed its holdout evals and (b) the owner
approves the packaging work as its own feature. Packaging mechanics never come
before the workflow is proven useful.

## Where things live

| Artifact | Location |
|---|---|
| Workflow (source of truth) | `.agents/skills/fable-distiller/` |
| Claude Code discovery stub | `.claude/skills/fable-distiller/SKILL.md` |
| Starter evals + manual rubric | `evals/fable-distiller/` |
| Generated packs | user-chosen repo path, plain text, versioned in git |

## Exporting a pack to another tool

- **Claude-family tools**: install the compact variant as a skill/system prompt;
  keep the full manual as a repo doc the model can load on demand.
- **ChatGPT / GPT-class**: compact variant into Custom Instructions or a system
  prompt; examples-first variant works well as the first message of a project.
- **Codex / Cursor / other agents**: pack files in-repo + a pointer from
  `AGENTS.md`; these tools read repo markdown natively.
- **Open-source / local models**: examples-first variant, shortest form; expect
  scaffolding (external gates) to carry most of the weight.

Portability rule (Constitution VI): everything stays plain text, nothing depends
on one vendor's feature to function. Scaffolding pieces that ARE vendor-specific
(e.g. Claude Code hooks) must list a manual fallback next to them.

## Versioning and honesty

- Version packs like code: `pack-v1`, `pack-v2`, with a changelog line per
  refinement loop and the eval results that motivated it.
- A pack's README must state: what was extracted, from which sources, what is
  verified vs inferred vs guessed, and what remains unverified — a reviewer must
  be able to see what was proven without re-running anything.
- Never describe a pack as "a copy of Fable" (or any model). It is the model's
  observable working discipline, reconstructed as procedures — say exactly that.
