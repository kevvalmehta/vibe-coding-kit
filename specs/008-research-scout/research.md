# Phase 0 Research: `/research-scout`

We ate our own dog food — researched *how to build a research agent* before speccing one. Cited
sources and the design decisions they drove.

## Sources

- **Anthropic — How we built our multi-agent research system** (primary): https://www.anthropic.com/engineering/multi-agent-research-system
- Prompting Guide — Context Engineering / Deep Research deep dive: https://www.promptingguide.ai/agents/context-engineering-deep-dive
- How OpenAI's Deep Research works (PromptLayer): https://blog.promptlayer.com/how-deep-research-works/
- Inference-Time Scaling of Verification (arXiv 2026): https://arxiv.org/pdf/2601.15808
- VoltAgent — awesome-ai-agent-papers (curated repo): https://github.com/VoltAgent/awesome-ai-agent-papers

## Findings → decisions

- **Match effort to the question; embed scaling rules.** Anthropic's agent once spawned 50 subagents
  for a trivial query. → FR-005/006: quick default, depth tiers, hard ceiling, effort heads-up.
- **Decompose into focused, non-overlapping subtasks; brief precisely.** Vague "research X" fails. →
  FR-010 method (decompose → parallel search → triage → synthesize).
- **Separate citation pass.** A dedicated step checks each claim against its source ("do claims match
  sources, do cited sources match claims"). → FR-002/010: cite everything, separate citation pass,
  never fabricate.
- **Source quality matters; agents drift to SEO junk.** Prefer primary/authoritative. → FR-008 source
  tiers; Reddit/forums = anecdote, cross-checked.
- **Explicit STOP + budget** or it loops forever on nonexistent sources. → FR-006/010 STOP rule +
  ceiling (echoes loop-design's STOP frame + agent-eval's cost cap).
- **Multi-agent ≈ 15× token cost.** → lean by default; deep fan-out only on request; advise cost/benefit
  (FR-007).
- **Treat retrieved content carefully.** → FR-009 fetched text is DATA, not instructions (injection-safe).

## Why it's a procedure skill, not a Python tool

The runtime is the AI following the procedure with web search + GitMCP + optional helper subagents —
there is no deterministic algorithm to encode in a runner (contrast `/agent-eval`, which has real
scoring logic). So, like `/discover` and `agent-architect`, it ships as a portable `SKILL.md` + small
reference files, guarded by a content/registration guard test. Simpler, and Principle V (no YAGNI runner).
