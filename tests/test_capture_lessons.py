"""Characterization + regression tests for scripts/capture-lessons.ps1 (the learning hook).

WHY: the hook once captured the SAME pasted message 14 times across 5 sessions, garbled
(em-dashes became "â€"") — see the 2026-07-16 queue-empty note in .specify/memory/lessons.md.
Root cause: the transcript and lessons.md were read with PowerShell 5.1's default ANSI
decoding instead of UTF-8, so any message containing a non-ASCII character (a) was
mojibake'd on capture and (b) never matched the exact-string dedup when a resumed session
(new session id -> high-water mark resets -> full transcript rescan) saw it again.

These tests run the REAL script via powershell.exe against a temp project and lock in:
  - opt-in: no lessons.md -> no-op, nothing created;
  - a correction-shaped user message becomes ONE "### candidate" entry;
  - re-running the same session never duplicates (high-water mark);
  - a NEW session rescanning the same non-ASCII message never duplicates (the 14x bug);
  - captured text keeps its real characters (no mojibake);
  - dedup still matches entries the OLD buggy version already wrote garbled;
  - the hook exits 0 even on garbage input (must never break a session).
"""

import json
import subprocess
from pathlib import Path

from _kitpaths import scripts_dir

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = scripts_dir(ROOT) / "capture-lessons.ps1"

SESSION_A = "aaaa1111-1111-1111-1111-111111111111"
SESSION_B = "bbbb2222-2222-2222-2222-222222222222"

CORRECTION_ASCII = "no, actually don't do that - always use the shared helper instead"
CORRECTION_UNICODE = "from now on — never touch the ✓ prod db — always ask first"


def transcript_line(text: str) -> str:
    # ensure_ascii=False: real transcripts hold raw UTF-8 bytes, not \uXXXX escapes —
    # that's exactly what the ANSI-read bug garbled.
    return json.dumps(
        {"type": "user", "message": {"content": [{"type": "text", "text": text}]}},
        ensure_ascii=False,
    )


def write_transcript(tmp_path: Path, texts: list[str], name: str) -> Path:
    p = tmp_path / name
    # UTF-8 without BOM, exactly how Claude Code writes transcripts.
    p.write_text("\n".join(transcript_line(t) for t in texts) + "\n", encoding="utf-8")
    return p


def make_project(tmp_path: Path, lessons_seed: str = "# Lessons\n") -> Path:
    mem = tmp_path / ".specify" / "memory"
    mem.mkdir(parents=True)
    (mem / "lessons.md").write_text(lessons_seed, encoding="utf-8")
    return mem / "lessons.md"


def run_hook(cwd: Path, transcript: Path, session_id: str = SESSION_A):
    payload = json.dumps(  # ensure_ascii keeps the piped stdin codepage-proof
        {"cwd": str(cwd), "transcript_path": str(transcript), "session_id": session_id}
    )
    return subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(SCRIPT)],
        input=payload,
        capture_output=True,
        text=True,
        timeout=90,
    )


def test_optin_noop_without_lessons_file(tmp_path):
    """No Scar Log -> the hook must do nothing and create nothing."""
    transcript = write_transcript(tmp_path, [CORRECTION_ASCII], "s1.jsonl")
    result = run_hook(tmp_path, transcript)
    assert result.returncode == 0
    assert not (tmp_path / ".specify").exists()


def test_correction_message_captured_once(tmp_path):
    """A correction-shaped message becomes exactly one candidate entry."""
    lessons = make_project(tmp_path)
    transcript = write_transcript(tmp_path, ["please build the page", CORRECTION_ASCII], "s1.jsonl")
    result = run_hook(tmp_path, transcript)
    assert result.returncode == 0
    content = lessons.read_text(encoding="utf-8")
    assert content.count("### candidate") == 1
    assert "always use the shared helper" in content


def test_same_session_rerun_does_not_duplicate(tmp_path):
    """The per-session high-water mark stops rescans within one session."""
    lessons = make_project(tmp_path)
    transcript = write_transcript(tmp_path, [CORRECTION_ASCII], "s1.jsonl")
    run_hook(tmp_path, transcript)
    run_hook(tmp_path, transcript)
    assert lessons.read_text(encoding="utf-8").count("### candidate") == 1


def test_new_session_rescan_does_not_duplicate_nonascii(tmp_path):
    """THE 14x BUG: a resumed session gets a new session id, so the whole transcript is
    rescanned and only the dedup-against-lessons.md backstop protects us. With non-ASCII
    text the old ANSI read garbled the comparison and the backstop never matched."""
    lessons = make_project(tmp_path)
    t1 = write_transcript(tmp_path, [CORRECTION_UNICODE], "s1.jsonl")
    run_hook(tmp_path, t1, SESSION_A)
    t2 = write_transcript(tmp_path, [CORRECTION_UNICODE, "thanks, looks good"], "s2.jsonl")
    run_hook(tmp_path, t2, SESSION_B)
    assert lessons.read_text(encoding="utf-8").count("### candidate") == 1


def test_captured_text_is_not_mojibake(tmp_path):
    """Em-dashes must survive capture as em-dashes, not as 'â€"'."""
    lessons = make_project(tmp_path)
    transcript = write_transcript(tmp_path, [CORRECTION_UNICODE], "s1.jsonl")
    run_hook(tmp_path, transcript)
    content = lessons.read_text(encoding="utf-8")
    assert content.count("### candidate") == 1
    assert "—" in content, "em-dash was not preserved"
    assert "â€" not in content, "captured text is mojibake (UTF-8 read as ANSI)"


def test_dedup_matches_entries_the_buggy_version_wrote(tmp_path):
    """lessons.md already holds garbled entries from the buggy version. A fresh, correctly
    decoded capture of the same message must still be recognized as a duplicate."""
    mojibake = CORRECTION_UNICODE.encode("utf-8").decode("cp1252")
    seed = (
        "# Lessons\n\n## Candidate lessons\n\n"
        "### candidate -- 2026-07-16 21:34 (session cf818f)\n"
        f'**Trigger phrase (you said):** "{mojibake}"\n'
        "**Action:** review, then promote to an L-# entry above, or delete.\n"
    )
    lessons = make_project(tmp_path, seed)
    transcript = write_transcript(tmp_path, [CORRECTION_UNICODE], "s1.jsonl")
    run_hook(tmp_path, transcript)
    assert lessons.read_text(encoding="utf-8").count("### candidate") == 1


def test_garbage_input_still_exits_zero(tmp_path):
    """Contract: the hook must NEVER break a session, whatever it is fed."""
    result = subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(SCRIPT)],
        input="this is not json {",
        capture_output=True,
        text=True,
        timeout=90,
    )
    assert result.returncode == 0
