"""Guard test for the vendored ponytail adoption (VCK mirror of PCK #63).

Ponytail (DietrichGebert/ponytail, MIT) is vendored verbatim and wired as three hooks:
SessionStart (activate + inject rules), UserPromptSubmit (track /ponytail mode), SubagentStart
(inject rules into subagents, which also carries the rules into a delegated Codex helper).

These assertions lock in that wiring so a future edit cannot SILENTLY:
  - drop one of the three hooks    -> ponytail stops loading its rules, no error shown;
  - corrupt the hooks config       -> the kit's OWN safety hooks (TDD-guard etc.) die with it;
  - lose the MIT LICENSE           -> attribution is the single condition the license imposes;
  - move/rename the ruleset        -> ponytail's loader silently serves its stale inline copy.

Layout-aware (like _kitpaths): resolves ponytail + the hooks config under BOTH the dev-repo
layout (vendor/ponytail, .claude/settings.json) and the published plugin layout
(plugins/<plugin>/vendor/ponytail, plugins/<plugin>/hooks/hooks.json), so this one file runs
green in either repo. Pure filesystem + JSON reads: no network, no node, no model calls.
Paths anchored only on vendor/, plugins/, and .claude/settings.json — none banned by
tests/test_no_hardcoded_kit_paths.py (which guards scripts/ and .claude/skills/).
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

HOOK_FILES = [
    "ponytail-activate.js",
    "ponytail-config.js",
    "ponytail-instructions.js",
    "ponytail-mode-tracker.js",
    "ponytail-runtime.js",
    "ponytail-subagent.js",
    "ponytail-statusline.sh",
    "ponytail-statusline.ps1",
]


def _vendor_dir() -> Path:
    dev = ROOT / "vendor" / "ponytail"
    if dev.is_dir():
        return dev
    for c in sorted(ROOT.glob("plugins/*/vendor/ponytail")):
        if c.is_dir():
            return c
    return dev  # keep failure messages sensible if neither exists


def _hooks_config() -> Path:
    # A repo may have BOTH a root .claude/settings.json (VCK's is hooks-less) and a plugin
    # hooks.json — so pick the first candidate that actually carries a "hooks" key, preferring
    # the plugin layout. PCK (dev repo) has no plugins/ dir, so it falls through to settings.json.
    candidates = list(sorted(ROOT.glob("plugins/*/hooks/hooks.json"))) + [ROOT / ".claude" / "settings.json"]
    for c in candidates:
        if c.is_file():
            try:
                if "hooks" in json.loads(c.read_text(encoding="utf-8")):
                    return c
            except (json.JSONDecodeError, OSError):
                continue
    return ROOT / ".claude" / "settings.json"  # sensible default for the failure message


VENDOR = _vendor_dir()
CONFIG = _hooks_config()


def _hooks() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))["hooks"]


def _commands(event: str) -> list[str]:
    return [h["command"] for group in _hooks().get(event, []) for h in group["hooks"]]


def test_vendored_runtime_files_present():
    """A missing runtime file means the corresponding hook throws at session start."""
    missing = [f for f in HOOK_FILES if not (VENDOR / "hooks" / f).is_file()]
    assert missing == [], f"missing vendored ponytail files: {missing}"


def test_ruleset_at_loaders_expected_path_with_ladder():
    """ponytail-instructions.js reads ../skills/ponytail/SKILL.md; move it and ponytail silently
    falls back to its stale inline ruleset. Lock the path AND a decision-ladder marker."""
    skill = VENDOR / "skills" / "ponytail" / "SKILL.md"
    assert skill.is_file(), "ruleset markdown missing at the path ponytail's loader expects"
    assert "Does this need to exist at all" in skill.read_text(encoding="utf-8"), (
        "ruleset lost its lazy decision-ladder"
    )


def test_mit_license_vendored_for_attribution():
    """MIT's one obligation is keeping the notice with the copy. Drop it -> out of compliance."""
    lic = VENDOR / "LICENSE"
    assert lic.is_file(), "vendored LICENSE missing (MIT attribution requirement)"
    text = lic.read_text(encoding="utf-8")
    assert "MIT License" in text and "DietrichGebert" in text


def test_hooks_config_is_valid_json():
    """Highest-stakes assertion: broken JSON here disables the kit's own safety hooks, not just
    ponytail's. If this fails, every PreToolUse guard is silently gone too."""
    json.loads(CONFIG.read_text(encoding="utf-8"))


def test_three_ponytail_hooks_are_wired():
    """The three events that make ponytail load its rules must each point at a vendored script."""
    assert any("ponytail-activate.js" in c for c in _commands("SessionStart")), (
        "SessionStart activate hook missing — rules won't load on session start"
    )
    assert any("ponytail-mode-tracker.js" in c for c in _commands("UserPromptSubmit")), (
        "UserPromptSubmit tracker hook missing — /ponytail lite|full|ultra won't switch"
    )
    assert any("ponytail-subagent.js" in c for c in _commands("SubagentStart")), (
        "SubagentStart hook missing — subagents (incl. a Codex helper) run ponytail-unaware"
    )


def test_existing_safety_hooks_survived():
    """Regression canary: adopting ponytail must not have dropped the kit's own guards."""
    pre = [h["command"] for group in _hooks()["PreToolUse"] for h in group["hooks"]]
    assert any("tdd_guard.py" in c for c in pre), "TDD-guard hook was lost"
    assert any("destructive_action_gate.py" in c for c in pre), "destructive-action gate was lost"
