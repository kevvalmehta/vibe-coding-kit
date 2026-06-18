# Awesome-Claude-Code — shortlist for your two projects

Hand-picked from the 174-entry catalog ([THE_RESOURCES_TABLE.csv](https://github.com/hesreallyhim/awesome-claude-code/blob/main/THE_RESOURCES_TABLE.csv)).
Workflow: find something here → scan it with SkillSpector before installing.

---

## For the Coding Spec Kit (plan → TDD → review → ship)

| Tool | What it does (plain) | Why it fits you |
|---|---|---|
| [Superpowers](https://github.com/obra/superpowers) | The TDD / plan / review skill bundle you already use. | Confirms your choice — it's the catalog's headline pick for the full build cycle. |
| [TDD Guard](https://github.com/nizos/tdd-guard) | A guard that watches edits and **blocks** any change that breaks the test-first rule. | Mechanically enforces your Hard Rule #2 ("TDD always"). |
| [Trail of Bits Security Skills](https://github.com/trailofbits/skills) | A dozen professional security-audit skills (Semgrep, CodeQL, fix verification). | You already run Semgrep — this is the pro-grade version of your Hard Rule #4 ("security first"). |
| [Plannotator](https://github.com/backnotprop/plannotator) | A little UI to read, mark up, and approve the AI's plan **before** it builds. | Direct fit for "plan before code" — you eyeball the plan and annotate it first. |
| [RIPER Workflow](https://github.com/tony/claude-code-riper-5) | Forces distinct phases: Research → Innovate → Plan → Execute → Review. | Same philosophy as your speckit flow; worth a look for ideas to borrow. |
| [parry](https://github.com/vaporif/parry) | Scans for prompt-injection / secret-leak attempts as the AI works. | Backs your security-first stance; pairs with SkillSpector (early-stage, so just a look). |

## For the Second Brain (notes → wiki → decide)

| Tool | What it does (plain) | Why it fits you |
|---|---|---|
| [agnix](https://github.com/agent-sh/agnix) | A linter that checks `CLAUDE.md`, `AGENTS.md`, `SKILL.md` files for mistakes, with auto-fixes. | You keep CLAUDE.md and AGENTS.md in sync by hand and have many skill files — this catches drift automatically. **Useful for both projects.** |
| [Claude Scientific Skills](https://github.com/K-Dense-AI/claude-scientific-skills) | Ready-made skills for research, analysis, finance, and writing. | Maps onto your `finance` and research domains. |
| [Context Engineering Kit](https://github.com/NeoLabHQ/context-engineering-kit) | Techniques to feed the AI the right context using fewer tokens. | Directly supports your "read in priority order, stop early, minimize tokens" rule. |
| [claude-code-tools](https://github.com/pchalasani/claude-code-tools) | Keeps context across sessions; fast full-text search over past sessions; hand-off between Claude and other AIs. | Reinforces your `hot.md` / memory-snapshot continuity and your cross-LLM portability goal. |
| [Compound Engineering Plugin](https://github.com/EveryInc/compound-engineering-plugin) | A discipline for turning past mistakes into reusable lessons. | Mirrors your `learnings.md` / self-evolution loop. |
| [Claude Session Restore](https://github.com/ZENG3LD/claude-session-restore) | Rebuilds context from earlier sessions using session files + git history. | Another angle on your "catch up fast" read-priority flow. |

---

## Worth knowing (not now)
- [Claude CodePro](https://github.com/maxritter/claude-codepro) and [claudekit](https://github.com/carlrannaberg/claudekit) — heavyweight all-in-one kits that bundle spec-driven workflow + TDD + memory. Closest things to what you're hand-building; useful as reference or a fallback, but overlapping and heavy.
- [Encyclopedia of Agentic Coding Patterns](https://aipatternbook.com) — 190+ patterns for AI-assisted dev; a reading reference, not a tool.

> Catalog caveat: the repo's browsable front page is mid-rebuild, so this CSV is the real source for now.
