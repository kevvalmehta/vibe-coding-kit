# Upstream sources — the repos this kit borrowed ideas from

This is the watch-list for **`/upstream-check`**. Each row is a repo whose ideas were rebuilt natively
in this kit (we never install upstream code — Constitution VI portability). `/upstream-check` reads this
file, looks at what each repo changed **since the `synced-at` commit**, and reports — with pros, cons,
and a worth-it verdict — anything worth porting. You approve each port; nothing copies automatically.

**`synced-at` is the bookmark.** It records the exact commit of the upstream repo we last reviewed, so
the next check only looks at what's new since then. Rows start **UNPINNED**: the first `/upstream-check`
run records each repo's current commit, and every run after that diffs from there.

**Never invent a commit, a change, or a verdict.** If `gh`/network is unavailable, `/upstream-check`
says so and stops — it does not guess.

| # | Repo | What we borrowed | Native home in this kit | License | synced-at |
|---|------|------------------|--------------------------|---------|-----------|
| 1 | [github/spec-kit](https://github.com/github/spec-kit) | the whole planning workflow (`/speckit-*`) | `.specify/`, `.claude/skills/speckit-*` | MIT | UNPINNED |
| 2 | [Forward-Future/loop-library](https://github.com/Forward-Future/loop-library) | loop patterns + 4-part frame | `/loop-design` + `catalog.md` | MIT | UNPINNED |
| 3 | [obra/superpowers](https://github.com/obra/superpowers) | safe-build engine (TDD, worktrees, two-stage review) | installed plugin + our guardrails | check repo | UNPINNED |
| 4 | [mattpocock/skills](https://github.com/mattpocock/skills) | grill-me, grill-with-docs, zoom-out, prototype | `.claude/skills/{grill-me,grill-with-docs,zoom-out,prototype}` | MIT | UNPINNED |
| 5 | [TexasBedouin/vibe-check](https://github.com/TexasBedouin/vibe-check) | the pre-spec reality-check method | `/discover` | MIT | UNPINNED |
| 6 | [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | the "build smaller" ruleset | `/lean-review` + `/lean-debt` + constitution V | MIT | UNPINNED |
| 7 | [humanlayer/12-factor-agents](https://github.com/humanlayer/12-factor-agents) | principles for AI-inside apps | `docs/ai-feature-checklist.md` | CC BY-SA | UNPINNED |
| 8 | [idosal/git-mcp](https://github.com/idosal/git-mcp) | the GitMCP grounding connector | `.mcp.json` + AGENTS.md notes | check repo | UNPINNED |
| 9 | [safishamsi/graphify](https://github.com/safishamsi/graphify) | optional impact-map connector | AGENTS.md notes | check repo | UNPINNED |

**Not tracked:** RTK — evaluated and parked (didn't run on Windows); we never borrowed from it, so it's
not on the watch-list. Add a row here if that ever changes.

## How a row gets updated
1. `/upstream-check` reports what's new since `synced-at` for a repo, with a worth-it verdict.
2. If you approve a port, the kit's `/safe-change` builds it natively (tests first, isolated, reviewed).
3. `/upstream-check` then updates that row's `synced-at` to the commit it just reviewed — so the next
   run starts fresh from there. (Licences noted "check repo" get confirmed at first real review.)
