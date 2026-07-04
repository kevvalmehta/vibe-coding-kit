# tests/test_feedback_loop_hardening.py
"""Guard for spec 019 (feedback-loop hardening): the five loop-discipline rules must
exist with their load-bearing phrases intact — eval answer-key blinding, the
constraint-needs-an-instrument rule, /ship's hypothesis log + forced new hypothesis on
stall, the Scar Log graduation path, and scaffold's structured-logs advice. Drop one
and the loop degrades to exactly the failure it was built to prevent (memorized evals,
vibe constraints, same-knob-harder stalls, prose-only lessons, illegible apps)."""
from pathlib import Path

from _kitpaths import skills_dir

ROOT = Path(__file__).resolve().parent.parent


def read(path):
    return path.read_text(encoding="utf-8").lower()


def test_agent_eval_blinds_the_answer_key():
    low = read(skills_dir(ROOT) / "agent-eval" / "SKILL.md")
    assert "blind" in low  # the rule is named
    assert "never read the expected answers" in low or "must not read the expected answers" in low
    # what the iterating agent IS allowed to see
    assert "categor" in low  # score + failed-case categories
    assert "memoriz" in low  # the failure this prevents


def test_goal_requires_an_instrument_per_constraint():
    low = read(skills_dir(ROOT) / "goal" / "SKILL.md")
    assert "instrument" in low
    assert "vibe" in low  # "a constraint without an instrument is a vibe"
    assert "wall-clock" in low or "wall clock" in low  # agents have no time sense
    assert "target mode" in low  # optional descend-to-a-bar mode


def test_ship_logs_hypotheses_and_forces_entropy_on_stall():
    low = read(skills_dir(ROOT) / "ship" / "SKILL.md")
    assert "hypothesis" in low
    assert "expected failure" in low  # log: hypothesis -> expected failure -> diagnostic
    assert "different hypothesis" in low  # stall -> genuinely new idea required
    assert "harder" in low  # "same idea, harder" is the banned move


def test_lessons_have_a_graduation_path():
    low = read(ROOT / ".specify/memory/lessons.md")
    assert "graduate" in low
    assert "hook" in low or "lint" in low or "ci check" in low
    assert "100%" in low or "every time" in low  # checks fire always; prose relies on memory


def test_scaffold_advises_structured_logs():
    low = read(skills_dir(ROOT) / "scaffold" / "SKILL.md")
    assert "structured log" in low
