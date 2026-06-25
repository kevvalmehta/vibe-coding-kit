"""Guard test for the Conductor (`/start`) skill + its SessionStart greeting hook.

Spec: specs/009-conductor/spec.md  ·  Plan: specs/009-conductor/plan.md

Written FIRST (TDD). Pure filesystem/stdlib reads — no network/model. Guards that the SKILL.md states
every required behavior + is registered, and that the greeting hook fires once per project.
"""
import importlib.util
import io
import json
from pathlib import Path

from _kitpaths import scripts_dir, skills_dir

ROOT = Path(__file__).resolve().parent.parent
SKILL = skills_dir(ROOT) / "start" / "SKILL.md"
STAGE_MAP = skills_dir(ROOT) / "start" / "references" / "stage-resource-map.md"


def _skill() -> str:
    return SKILL.read_text(encoding="utf-8").lower()


# ---------- the skill ----------

def test_T1_skill_exists_with_frontmatter():
    assert SKILL.exists(), "start/SKILL.md missing"
    text = SKILL.read_text(encoding="utf-8")
    assert "name: start" in text, "frontmatter missing 'name: start'"
    assert "description:" in text, "frontmatter missing description"


def test_T2_proactive_and_invokable():
    t = _skill()
    assert "start" in t and ("greet" in t or "greeting" in t), "missing greeting"
    assert "capabilities" in t or "what i can" in t or "what it can" in t, "missing capabilities/limits"


def test_T3_drives_existing_skills_not_a_new_pipeline():
    t = _skill()
    assert "idea-to-app" in t, "must drive idea-to-app (not a new pipeline)"
    assert "guide" in t, "must use guide's routing"
    assert "not a new pipeline" in t or "not reimplement" in t or "drive" in t, "must say it drives, not duplicates"


def test_T4_weaves_the_stage_resources():
    t = _skill()
    for needle in ("discover", "grill-me", "research-scout", "loop-design", "verify", "security-review", "git-safety"):
        assert needle in t, f"SKILL.md does not weave in: {needle}"
    assert "stack" in t, "missing the light stack suggestion"


def test_T5_checkpoints_bypass_and_safety_wall():
    t = _skill()
    assert "checkpoint" in t or "stop for" in t or "your ok" in t, "missing per-stage checkpoints"
    assert "just run it" in t or "bypass" in t, "missing the opt-in bypass"
    assert "never" in t and ("push" in t and "merge" in t and "deploy" in t), "missing the never push/merge/deploy wall"


def test_T6_stage_resource_map_exists():
    assert STAGE_MAP.exists(), "references/stage-resource-map.md missing"
    t = STAGE_MAP.read_text(encoding="utf-8").lower()
    for needle in ("discover", "research-scout", "loop-design", "recommender", "gitmcp", "cookbook", "agent-architect"):
        assert needle in t, f"stage-resource-map missing: {needle}"


def test_T7_registered_everywhere():
    assert "start" in (ROOT / "SKILL-MAP.md").read_text(encoding="utf-8"), "not in SKILL-MAP.md"
    # AGENTS.md + README mention the Conductor explicitly
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8").lower()
    assert "conductor" in agents and "/start" in agents, "AGENTS.md does not register the Conductor /start"
    assert "conductor" in (ROOT / "README.md").read_text(encoding="utf-8").lower(), "README missing Conductor"


# ---------- the SessionStart greeting hook ----------

_spec = importlib.util.spec_from_file_location("conductor_greeting", scripts_dir(ROOT) / "conductor_greeting.py")
conductor_greeting = importlib.util.module_from_spec(_spec)
if _spec.loader and (scripts_dir(ROOT) / "conductor_greeting.py").exists():
    _spec.loader.exec_module(conductor_greeting)


def test_T8_hook_fires_once_for_fresh_project(tmp_path, monkeypatch):
    (tmp_path / ".git").mkdir()
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps({"cwd": str(tmp_path)})))
    cap = io.StringIO()
    monkeypatch.setattr("sys.stdout", cap)
    assert conductor_greeting.main() == 0
    out = cap.getvalue()
    assert "conductor" in out.lower() and "start" in out.lower(), "hook did not emit the greeting"
    assert (tmp_path / ".claude" / ".conductor-greeted").exists(), "marker not written"


def test_T9_hook_silent_after_marker(tmp_path, monkeypatch):
    (tmp_path / ".git").mkdir()
    conductor_greeting.mark_done(tmp_path)
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps({"cwd": str(tmp_path)})))
    cap = io.StringIO()
    monkeypatch.setattr("sys.stdout", cap)
    assert conductor_greeting.main() == 0
    assert cap.getvalue() == "", "hook should stay quiet after the marker exists"


def test_T10_hook_survives_garbage_stdin(monkeypatch):
    monkeypatch.setattr("sys.stdin", io.StringIO("not json"))
    assert conductor_greeting.main() == 0
