# tests/test_wargame.py
"""Guard for spec 030 (/wargame): the plan war-gaming coach must exist with its
load-bearing pieces intact — the binding WARGAME.md contract, the four lines per plan
step (expected observation / failure scenario / likely cause / countermove), decision
forks, abort conditions, the assumed-inputs vs recon-needed split with {Placeholder}
unknowns, and the named executor model line. Plus the two absorptions: the
"Fails when → then what" companion line in the tasks template and the {Variable}
unknowns notation in /pathfinder's Fog section. If a future edit drops one of these,
the skill degrades into generic "think about risks" advice — the thing it replaces."""
from pathlib import Path

from _kitpaths import skills_dir

ROOT = Path(__file__).resolve().parent.parent


def read(path):
    return path.read_text(encoding="utf-8")


def test_wargame_skill_exists_and_writes_the_contract():
    text = read(skills_dir(ROOT) / "wargame" / "SKILL.md")
    assert "WARGAME.md" in text  # the binding contract file, by name


def test_wargame_has_the_four_lines_per_step():
    low = read(skills_dir(ROOT) / "wargame" / "SKILL.md").lower()
    # per plan step: what success looks like, how it fails, why, and the countermove
    assert "expected observation" in low
    assert "failure scenario" in low
    assert "likely cause" in low or "likely failure cause" in low
    assert "countermove" in low


def test_wargame_has_forks_and_aborts():
    low = read(skills_dir(ROOT) / "wargame" / "SKILL.md").lower()
    assert "fork" in low  # "if you observe X → route A; if Y → route B"
    assert "route a" in low and "route b" in low
    assert "abort" in low  # conditions where the executor stops, never improvises


def test_wargame_splits_assumptions_and_marks_unknowns():
    text = read(skills_dir(ROOT) / "wargame" / "SKILL.md")
    low = text.lower()
    assert "assumed inputs" in low
    assert "recon needed" in low
    # unknowns the owner must fill are {PlaceholderName} variables, greppable later
    assert "{" in text and "}" in text
    assert "placeholder" in low


def test_wargame_names_the_executor_model():
    low = read(skills_dir(ROOT) / "wargame" / "SKILL.md").lower()
    # the contract names which (cheaper) model executes the battle plan faithfully
    assert "executor" in low
    assert "cheaper" in low


def test_wargame_is_read_only_and_never_ships():
    low = read(skills_dir(ROOT) / "wargame" / "SKILL.md").lower()
    assert "read-only" in low or "never edits code" in low
    for forbidden in ("push", "merge", "deploy"):
        assert forbidden in low  # the never-push/merge/deploy wall, stated


def test_wargame_template_reference_exists():
    tpl = skills_dir(ROOT) / "wargame" / "references" / "wargame-template.md"
    text = read(tpl)
    low = text.lower()
    for section in ("expected observation", "failure scenario", "countermove",
                    "decision forks", "abort", "assumed inputs", "recon needed",
                    "executor"):
        assert section in low, f"template missing section: {section}"


def test_tasks_template_has_fails_when_companion_line():
    # absorption 1: the "Done when" convention gains a "Fails when → then what" line
    low = read(ROOT / ".specify" / "templates" / "tasks-template.md").lower()
    assert "fails when" in low
    assert "then what" in low


def test_pathfinder_fog_mentions_variable_notation():
    # absorption 2: Fog entries can mark nameable-but-unanswered values as {Variable}
    text = read(skills_dir(ROOT) / "pathfinder" / "SKILL.md")
    assert "{" in text and "}" in text
    assert "unknown" in text.lower()


def test_wargame_registered_everywhere():
    # Principle VI: not done until registered for other AI tools too
    for rel in ("SKILL-MAP.md", "AGENTS.md", "README.md", "QUICKSTART.md"):
        assert "wargame" in read(ROOT / rel).lower(), f"wargame missing from {rel}"
