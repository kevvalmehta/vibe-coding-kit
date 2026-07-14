# ponytail (vendored, verbatim)

**Source:** https://github.com/DietrichGebert/ponytail — version **4.8.4**
**License:** MIT (see `LICENSE` in this folder — the one condition is keeping that notice).
**What it is:** the "lazy senior developer" code-minimalism discipline — before writing code,
climb a ladder (does this need to exist? stdlib? native platform feature? one line?) and take the
first rung that holds. The full ruleset is `skills/ponytail/SKILL.md`.

## Why the code is vendored, not installed as a plugin

- This environment has no `/plugin` marketplace, so the normal install path does not run here.
- Vendoring keeps the exact bytes that were security-reviewed under version control, instead of
  auto-pulling a future (unreviewed) release.
- It honors the kit's rules: no untrusted install, one source of truth, LLM-portable
  (plain files, documented in `AGENTS.md` + `SKILL-MAP.md`).

## What was changed vs. upstream

**The code files: nothing — verbatim.** The `hooks/*.js`, `hooks/*.sh|ps1`, and
`skills/ponytail/SKILL.md` are byte-for-byte from upstream 4.8.4.

The **wiring** is the kit's, not upstream's: instead of a plugin manifest, the three hooks are
registered by hand in `.claude/settings.json`:

| Event | Script | Job |
|---|---|---|
| SessionStart | `hooks/ponytail-activate.js` | write the on/off flag, inject the ruleset |
| UserPromptSubmit | `hooks/ponytail-mode-tracker.js` | react to `/ponytail lite\|full\|ultra` |
| SubagentStart | `hooks/ponytail-subagent.js` | inject the ruleset into subagents (incl. a Codex helper) |

The `[PONYTAIL]` statusline (`hooks/ponytail-statusline.ps1` / `.sh`) is optional and is wired
separately, because it runs PowerShell with `-ExecutionPolicy Bypass` and needs explicit approval.

## Security review (static, at adoption time)

Every file above was read line-by-line and pattern-scanned. Findings: no outbound network (the
only `connect` is local stdio), no shell/`exec`, no `eval`, no secret/credential access, no
install-time (`postinstall`) scripts, no obfuscation. File writes are limited to ponytail's own
on/off flag and config. Re-review on any version bump before updating these files.

## Updating

Do not auto-update. To move to a new upstream version: re-download these exact files, re-run the
static review, run `tests/test_ponytail_adoption.py`, and bump the version noted above.
