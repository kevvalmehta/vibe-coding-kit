# Spec 016 — Opus Hardening Layer (enforcement over instruction)

## Why (plain English)

The owner wants to use Claude Opus 4.8 as the main build model. Opus hallucinates
(invented APIs, false "done/tests pass" claims, made-up facts) and drops instructions
in long sessions. A 2026-07-02 audit of both kits found the root cause: ~47 guardrails
exist but only ONE can physically stop the model in-session (TDD-Guard, off by default).
Everything else is prose the model can ignore.

**Principle:** you cannot instruct a model into reliability; you engineer the
environment so unreliable output gets caught before it lands. Hooks fire 100% of the
time; prose is probabilistic.

## What (Phase 1 — four hooks)

### FR-1 lessons_injector.py — close the learning loop (SessionStart)
- Reads `.specify/memory/lessons.md`; extracts ONLY confirmed `### L-#` (scar) and
  `### P-#` (pattern) entries — never auto-captured candidates, never the templates.
- Injects a compact digest (Rule + Self-check per entry) as session context.
- No lessons file or no confirmed entries → silent no-op. Never blocks a session (exit 0 always).
- Fixes: "Opus repeats corrected mistakes" — the capture hook wrote lessons; nothing read them back.

### FR-2 done_claim_verifier.py — no claim without proof (Stop, BLOCK mode)
- On Stop, scans the current turn's final assistant text for strong completion claims:
  tests pass/green, pushed, committed, build/lint passes, deployed.
- For each claim, looks for the matching verifying command actually run this turn
  (pytest/npm test/jest/vitest; git push; git commit; build/lint commands).
- Claim with no evidence → `{"decision": "block"}` with a plain reason: run the proving
  command or correct the claim. Respects `stop_hook_active` (no infinite loops).
- Opt-out marker: `.no-claim-verify` at repo root. Errors swallowed; exit 0 always.
- Mechanizes the owner's global "Truth Over Confidence" rule.

### FR-3 regrounding.py — kill mid-session drift (SessionStart: resume|compact)
- After context compression or session resume, injects ground truth: current branch,
  count + sample of modified files, last commit, pointer to HANDOFF.md.
- Tells the model: memory is not proof; re-verify state claims against this snapshot.
- Never blocks; exit 0 always.

### FR-4 import_reality_check.py — catch invented APIs at the door (PostToolUse: Edit|Write|MultiEdit)
- After an edit to .py/.js/.ts/.tsx/.jsx/.mjs/.cjs, extracts imported top-level modules.
- Python: OK if stdlib, installed (find_spec), or a local module/file. JS/TS: OK if
  relative import, in package.json deps, or in node_modules.
- Unknown import → feedback to the model: likely invented or not installed; verify
  against real docs (GitMCP) or install it. Advisory feedback, does not undo the edit.
- Errors swallowed; exit 0 always.

## Hard rules honored
- TDD (tests in `tests/`, suite green before done)
- A hook must NEVER break a session (same contract as existing hooks)
- Windows-safe (PowerShell 5.1 host, ASCII-safe output)
- LLM portability: registered in AGENTS.md + SKILL-MAP.md; mirrored to vibe-coding-kit

## Out of scope (later phases)
Phase 2: TDD-Guard default-on (opt-out), Semgrep blocking, wire orphaned gate scripts,
fix red inventory test. Phase 3: dependency vuln scanning, DB migration safety,
error monitoring, backups, load testing, accessibility.
