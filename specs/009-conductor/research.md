# Phase 0 Research: `/start` (the Conductor)

Dogfooded `/research-scout` to research how to build an orchestrator/mentor before designing it.

## Sources
- **Anthropic — Building Effective Agents** (primary): https://www.anthropic.com/research/building-effective-agents
- Co-designing conversational agents — review (ScienceDirect, peer-reviewed): https://www.sciencedirect.com/science/article/pii/S0142694X23000716
- How to Onboard Users to Conversational Agent Interactions (framework study): https://www.researchgate.net/publication/392399156
- Conversational AI for information elicitation (arXiv): https://arxiv.org/pdf/2506.11610
- Choosing a tech stack in 2026 (blog-tier, cross-checked across several): https://tbugaevsky.medium.com/how-to-choose-a-tech-stack-in-2026-what-the-evidence-says-3e9c32741340

## Findings → decisions
- **Orchestrator + routing; simple composable patterns beat frameworks** (Building Effective Agents).
  → Conductor is a router/orchestrator SKILL.md that DRIVES existing skills (idea-to-app, guide) — not
  a new engine, not a duplicate pipeline (FR-004). *(authoritative, high confidence)*
- **Good onboarding states capabilities/limits, asks dynamic questions (not static forms), keeps the
  user able to redirect; depth→ease, breadth→trust.** → FR-003 greeting + dynamic elicitation; FR-008
  checkpoints/control. *(peer-reviewed, high confidence)*
- **Stack: start from problem/users/features; "boring, proven tech"; match project type.** → FR-010
  light stack suggestion using kit defaults + project-type nudge. *(blog-tier, medium confidence,
  consistent across sources)*

## Why a procedure skill (+ one small hook), not a Python tool
The runtime is the AI following the procedure and routing to other skills — no deterministic algorithm
to encode (contrast `/agent-eval`). So: a portable SKILL.md + references + a single SessionStart
greeting hook (deterministic, stdlib, mirrors `recommender_nudge.py`), guarded by guard tests.
Principle V (no YAGNI runner).
