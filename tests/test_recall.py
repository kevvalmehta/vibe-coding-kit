"""Tests for scripts/recall.py -- the transcript + memory keyword recall tool ("goldfish" fix).

WHY these matter, one per real failure mode:
  1. It must find a fact saved in the memory markdown (the easy case).
  2. It must find a fact that lives ONLY in a raw session transcript, never saved as a memory --
     that is the WHOLE point, because "no search over transcripts" is exactly what made recall feel
     like a goldfish. A test that only checked memory files would pass even if transcript search was
     broken, so this is the load-bearing one.
  3. It must NOT match tool-result noise or injected <system-reminder> text -- otherwise recall
     surfaces machine chatter instead of what you actually said.

Pure filesystem: seeds a fake ~/.claude via CLAUDE_CONFIG_DIR + a temp cwd. No network, no model.
Locates scripts/ via _kitpaths so it runs in BOTH the dev repo and the published plugin repo.
"""

import sys
from pathlib import Path

from _kitpaths import scripts_dir

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(scripts_dir(ROOT)))


def _recall():
    """Import the module under test at call time, so a missing scripts/recall.py surfaces as a
    test FAILURE (red), not a collection error -- clean TDD bootstrap for a brand-new module."""
    import recall

    return recall


def _seed(home: Path) -> None:
    proj = home / "projects" / "C--demo"
    (proj / "memory").mkdir(parents=True)
    (proj / "memory" / "MEMORY.md").write_text(
        "- ponytail statusline was skipped (ExecutionPolicy concern)\n", encoding="utf-8"
    )
    # One transcript: a real user line, a tool_result (noise), and an injected reminder.
    # Only the first is real text the user typed; the other two must be ignored.
    lines = [
        '{"type":"user","message":{"content":[{"type":"text","text":"lets adopt supabase for auth"}]},"timestamp":"2026-07-01T10:00:00Z"}',
        '{"type":"user","message":{"content":[{"type":"tool_result","text":"supabase internal noise"}]}}',
        '{"type":"assistant","message":{"content":[{"type":"text","text":"<system-reminder>supabase reminder junk</system-reminder> ok"}]}}',
    ]
    (proj / "sess.jsonl").write_text("\n".join(lines), encoding="utf-8")


def test_project_slug_mirrors_claude_naming():
    recall = _recall()
    assert recall.project_slug(Path("C:/Projects/My App")) == "C--Projects-My-App"


def test_finds_fact_in_saved_memory(tmp_path, monkeypatch):
    recall = _recall()
    _seed(tmp_path)
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(tmp_path))
    monkeypatch.chdir(tmp_path)  # keep cwd-based dirs empty so only seeded data is searched
    hits = recall.search(["ponytail", "statusline"], all_projects=True)
    assert any(kind == "memory" and "statusline" in snip.lower() for kind, _d, _loc, snip in hits)


def test_finds_fact_only_in_transcript(tmp_path, monkeypatch):
    """The load-bearing case: 'supabase auth' lives ONLY in the raw transcript, never in a memory."""
    recall = _recall()
    _seed(tmp_path)
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(tmp_path))
    monkeypatch.chdir(tmp_path)
    hits = recall.search(["supabase", "auth"], all_projects=True)
    assert any(kind in ("user", "assistant") for kind, _d, _loc, _s in hits), (
        "transcript recall missed a real user line that was never saved as a memory"
    )


def test_ignores_tool_noise_and_injected_reminders(tmp_path, monkeypatch):
    recall = _recall()
    _seed(tmp_path)
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(tmp_path))
    monkeypatch.chdir(tmp_path)
    hits = recall.search(["supabase"], all_projects=True)
    blob = " ".join(snip for _k, _d, _loc, snip in hits).lower()
    assert "noise" not in blob, "matched tool_result noise instead of real text"
    assert "junk" not in blob, "matched injected <system-reminder> text instead of real text"


def test_prints_unicode_on_cp1252_stream_without_crashing(tmp_path, monkeypatch):
    """Regression: transcripts contain emoji/smart-quotes, and printing them to a Windows cp1252
    console crashed with UnicodeEncodeError. main() must reconfigure stdout to survive. We force a
    cp1252 stream so this actually FAILS if that fix is removed (a green-on-Linux-only test would be
    worthless per constitution Quality Gate 9)."""
    import io
    import sys as _sys

    recall = _recall()
    proj = tmp_path / "projects" / "C--u"
    proj.mkdir(parents=True)
    (proj / "s.jsonl").write_text(
        '{"type":"user","message":{"content":[{"type":"text","text":"ship it \U0001f680 rocket"}]}}',
        encoding="utf-8",
    )
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(tmp_path))
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(_sys, "stdout", io.TextIOWrapper(io.BytesIO(), encoding="cp1252"))
    assert recall.main(["--all", "ship"]) == 0  # must not raise UnicodeEncodeError
