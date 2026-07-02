# tests/test_done_claim_verifier.py
"""The done-claim verifier mechanizes Truth Over Confidence: an assistant turn may not
END on a strong completion claim ("tests pass", "pushed") unless the verifying command
actually ran in that turn. Claim without proof -> block; proof present -> silent."""
import importlib.util
import json
from pathlib import Path

from _kitpaths import scripts_dir

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location(
    "done_claim_verifier", scripts_dir(ROOT) / "done_claim_verifier.py"
)
dcv = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dcv)


def user_line(text):
    return json.dumps({"type": "user", "message": {"content": text}})


def tool_result_line():
    return json.dumps(
        {"type": "user", "message": {"content": [{"type": "tool_result", "content": "ok"}]}}
    )


def assistant_line(text=None, command=None):
    content = []
    if text:
        content.append({"type": "text", "text": text})
    if command:
        content.append({"type": "tool_use", "name": "Bash", "input": {"command": command}})
    return json.dumps({"type": "assistant", "message": {"content": content}})


def write_transcript(tmp_path, lines):
    p = tmp_path / "transcript.jsonl"
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return p


def hook_data(tmp_path, transcript, stop_hook_active=False):
    return {
        "cwd": str(tmp_path),
        "transcript_path": str(transcript),
        "session_id": "abc123",
        "stop_hook_active": stop_hook_active,
    }


def test_detects_test_pass_claims():
    assert "tests" in dcv.detect_claims("All 42 tests pass, we're good.")
    assert "tests" in dcv.detect_claims("The suite is green now.")
    assert "tests" not in dcv.detect_claims("I will now run the tests.")


def test_detects_push_and_commit_claims():
    assert "push" in dcv.detect_claims("Pushed to origin.")
    assert "commit" in dcv.detect_claims("Committed the fix.")


def test_plain_prose_has_no_claims():
    assert dcv.detect_claims("Here is my plan for the refactor.") == set()


def test_claim_without_evidence_blocks(tmp_path):
    t = write_transcript(
        tmp_path,
        [
            user_line("fix the bug"),
            assistant_line(text="Fixed. All tests pass."),
        ],
    )
    out = dcv.process(hook_data(tmp_path, t))
    assert out["decision"] == "block"
    assert "tests" in out["reason"].lower()


def test_claim_with_evidence_is_silent(tmp_path):
    t = write_transcript(
        tmp_path,
        [
            user_line("fix the bug"),
            assistant_line(text="Running tests.", command="python -m pytest -q"),
            tool_result_line(),
            assistant_line(text="All tests pass."),
        ],
    )
    assert dcv.process(hook_data(tmp_path, t)) is None


def test_only_current_turn_counts_as_evidence(tmp_path):
    # pytest ran in a PREVIOUS turn; the claim in this turn is still unproven.
    t = write_transcript(
        tmp_path,
        [
            user_line("run the tests"),
            assistant_line(text="Running.", command="python -m pytest -q"),
            tool_result_line(),
            user_line("now fix the bug"),
            assistant_line(text="Fixed. Tests pass."),
        ],
    )
    out = dcv.process(hook_data(tmp_path, t))
    assert out["decision"] == "block"


def test_tool_result_lines_do_not_reset_turn_boundary(tmp_path):
    # tool_result messages have type "user" but are NOT the user speaking.
    t = write_transcript(
        tmp_path,
        [
            user_line("fix and verify"),
            assistant_line(text="Running.", command="npm test"),
            tool_result_line(),
            assistant_line(text="Tests pass."),
        ],
    )
    assert dcv.process(hook_data(tmp_path, t)) is None


def test_stop_hook_active_is_noop(tmp_path):
    t = write_transcript(
        tmp_path,
        [user_line("go"), assistant_line(text="All tests pass.")],
    )
    assert dcv.process(hook_data(tmp_path, t, stop_hook_active=True)) is None


def test_opt_out_marker_disables(tmp_path):
    (tmp_path / ".no-claim-verify").write_text("off\n", encoding="utf-8")
    t = write_transcript(
        tmp_path,
        [user_line("go"), assistant_line(text="All tests pass.")],
    )
    assert dcv.process(hook_data(tmp_path, t)) is None


def test_push_claim_needs_git_push(tmp_path):
    t = write_transcript(
        tmp_path,
        [
            user_line("save my work"),
            assistant_line(text="Committing.", command="git commit -m x"),
            tool_result_line(),
            assistant_line(text="Committed and pushed."),
        ],
    )
    out = dcv.process(hook_data(tmp_path, t))
    assert out["decision"] == "block"
    assert "push" in out["reason"].lower()


def test_missing_transcript_is_silent(tmp_path):
    assert dcv.process(hook_data(tmp_path, tmp_path / "nope.jsonl")) is None
