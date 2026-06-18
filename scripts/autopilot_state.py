"""Autopilot deterministic state helper.

Answers one question with no model involvement: "which planning step are we on?"
Derives the answer from existing artifacts (the feature's specs/<id>/ directory),
so resume is reliable and testable. See
specs/001-autopilot-orchestrator/contracts/autopilot-skill-contract.md.
"""

from __future__ import annotations

import json
from pathlib import Path

STEP_ORDER: list[str] = ["specify", "clarify", "plan", "tasks", "pre-pr-checks"]

# Marker the skill writes into HANDOFF.md so a cold reader/this helper can find its section.
HANDOFF_MARKER = "<!-- AUTOPILOT-STATE -->"


def _has_open_clarification(spec_text: str) -> bool:
    return "[NEEDS CLARIFICATION" in spec_text


def _step_done(step: str, feature_dir: Path | None) -> bool:
    """Whether a step's artifact exists. Pure filesystem check, no ordering."""
    if feature_dir is None or not feature_dir.exists():
        return False
    spec = feature_dir / "spec.md"
    if step == "specify":
        return spec.is_file()
    if step == "clarify":
        # Clarify is "done" once a spec exists with no open clarification markers
        # (the kit auto-skips clarify in that case).
        if not spec.is_file():
            return False
        return not _has_open_clarification(spec.read_text(encoding="utf-8"))
    if step == "plan":
        return (feature_dir / "plan.md").is_file()
    if step == "tasks":
        return (feature_dir / "tasks.md").is_file()
    if step == "pre-pr-checks":
        # Terminal step — never auto-complete from a file artifact.
        return False
    return False


def get_current_step(
    feature_dir: str | None,
    handoff_text: str | None = None,
) -> dict:
    """Return the current/next planning step derived from artifacts.

    feature_dir: path to specs/<id>/ (or None / missing -> not started).
    handoff_text: optional HANDOFF.md contents; informational only — the
        filesystem is authoritative. A missing Autopilot marker adds a warning.
    """
    fd = Path(feature_dir) if feature_dir else None
    warnings: list[str] = []

    done = {step: _step_done(step, fd) for step in STEP_ORDER}
    completed = [step for step in STEP_ORDER if done[step]]

    # current = first step not yet done.
    current = next((step for step in STEP_ORDER if not done[step]), STEP_ORDER[-1])
    cur_idx = STEP_ORDER.index(current)

    # Out-of-order detection: a later step is done while current (earlier) is not.
    later_done = [step for step in completed if STEP_ORDER.index(step) > cur_idx]
    if later_done:
        warnings.append(
            f"prerequisite gap: {later_done} present but '{current}' is incomplete "
            "(out of order) — not skipping; resolve the earlier step first"
        )

    if handoff_text is not None and HANDOFF_MARKER not in handoff_text:
        warnings.append(
            "HANDOFF.md has no Autopilot marker section; using filesystem to resume"
        )

    nxt = STEP_ORDER[cur_idx + 1] if cur_idx + 1 < len(STEP_ORDER) else None

    return {
        "feature_dir": str(fd) if fd else None,
        "completed": completed,
        "current": current,
        "next": nxt,
        "warnings": warnings,
    }


def _resolve_active_feature_dir(repo_root: Path) -> str | None:
    fj = repo_root / ".specify" / "feature.json"
    if not fj.is_file():
        return None
    try:
        data = json.loads(fj.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    rel = data.get("feature_directory")
    return str(repo_root / rel) if rel else None


def main() -> None:
    """CLI: print the current step as JSON for the active feature."""
    repo_root = Path(__file__).resolve().parent.parent
    feature_dir = _resolve_active_feature_dir(repo_root)
    handoff = repo_root / "HANDOFF.md"
    handoff_text = handoff.read_text(encoding="utf-8") if handoff.is_file() else None
    print(json.dumps(get_current_step(feature_dir, handoff_text), indent=2))


if __name__ == "__main__":
    main()
