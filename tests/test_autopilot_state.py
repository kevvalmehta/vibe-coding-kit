"""Tests for the Autopilot deterministic state helper.

Contract: specs/001-autopilot-orchestrator/contracts/autopilot-skill-contract.md
These are written FIRST (TDD) and must fail before scripts/autopilot_state.py exists.
"""

import sys
from pathlib import Path

import pytest

from _kitpaths import scripts_dir

# Make the scripts dir importable (root `scripts/` or plugin `plugins/<plugin>/scripts/`).
sys.path.insert(0, str(scripts_dir(Path(__file__).resolve().parent.parent)))

import autopilot_state as st  # noqa: E402


def _write(feature_dir: Path, name: str, text: str = "x") -> None:
    (feature_dir / name).write_text(text, encoding="utf-8")


def test_step_order_is_fixed():
    assert st.STEP_ORDER == ["specify", "clarify", "plan", "tasks", "pre-pr-checks"]


def test_missing_feature_dir_starts_at_specify():
    result = st.get_current_step(None)
    assert result["current"] == "specify"
    assert result["completed"] == []
    assert result["next"] == "clarify"


def test_empty_feature_dir_starts_at_specify(tmp_path):
    result = st.get_current_step(str(tmp_path))
    assert result["current"] == "specify"
    assert result["completed"] == []


def test_spec_and_plan_present_no_tasks_is_at_tasks(tmp_path):
    _write(tmp_path, "spec.md", "# spec\nno markers here\n")
    _write(tmp_path, "plan.md")
    result = st.get_current_step(str(tmp_path))
    assert result["current"] == "tasks"
    assert "specify" in result["completed"]
    assert "clarify" in result["completed"]
    assert "plan" in result["completed"]
    assert result["next"] == "pre-pr-checks"


def test_spec_without_markers_counts_clarify_complete(tmp_path):
    _write(tmp_path, "spec.md", "# spec\nall resolved, no clarification needed\n")
    result = st.get_current_step(str(tmp_path))
    assert "clarify" in result["completed"]
    assert result["current"] == "plan"


def test_spec_with_open_clarification_marker_is_at_clarify(tmp_path):
    _write(tmp_path, "spec.md", "# spec\n- FR-006 [NEEDS CLARIFICATION: which auth?]\n")
    result = st.get_current_step(str(tmp_path))
    assert result["current"] == "clarify"
    assert "specify" in result["completed"]
    assert "clarify" not in result["completed"]


def test_prerequisite_gap_returns_earliest_gap_with_warning(tmp_path):
    # plan.md exists but spec.md is missing -> out of order.
    _write(tmp_path, "plan.md")
    result = st.get_current_step(str(tmp_path))
    assert result["current"] == "specify"
    assert result["warnings"], "expected a warning about the prerequisite gap"


def test_tasks_present_ends_at_pre_pr_checks(tmp_path):
    _write(tmp_path, "spec.md", "# spec\nno markers\n")
    _write(tmp_path, "plan.md")
    _write(tmp_path, "tasks.md")
    result = st.get_current_step(str(tmp_path))
    assert result["current"] == "pre-pr-checks"
    assert result["next"] is None


def test_malformed_handoff_text_adds_warning_filesystem_still_authoritative(tmp_path):
    _write(tmp_path, "spec.md", "# spec\nno markers\n")
    result = st.get_current_step(str(tmp_path), handoff_text="garbage with no marker")
    # filesystem says clarify done, current = plan; handoff note is informational only
    assert result["current"] == "plan"
    assert any("handoff" in w.lower() for w in result["warnings"])


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
