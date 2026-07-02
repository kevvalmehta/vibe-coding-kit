# tests/test_destructive_action_gate.py
"""The destructive-action gate is the kit's blast-radius limiter: an agent must never
run a destructive database/filesystem command or edit a schema/migration file without
the owner explicitly approving — because unsupervised migrations and bulk deletes are
the top way agents corrupt production data."""
import importlib.util
from pathlib import Path

from _kitpaths import scripts_dir

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location(
    "destructive_action_gate", scripts_dir(ROOT) / "destructive_action_gate.py"
)
gate = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gate)


def bash(cmd, cwd="."):
    return gate.process({"tool_name": "Bash", "tool_input": {"command": cmd}, "cwd": cwd})


def edit(path, cwd="."):
    return gate.process({"tool_name": "Edit", "tool_input": {"file_path": path}, "cwd": cwd})


def is_ask(out):
    return out is not None and out["hookSpecificOutput"]["permissionDecision"] == "ask"


def test_destructive_bash_commands_are_gated():
    assert is_ask(bash("rm -rf build/"))
    assert is_ask(bash("rm -fr /tmp/x"))
    assert is_ask(bash('psql -c "DROP TABLE users"'))
    assert is_ask(bash("npx supabase db reset"))
    assert is_ask(bash("npx prisma migrate reset --force"))
    assert is_ask(bash('psql -c "TRUNCATE TABLE posts"'))
    assert is_ask(bash('psql -c "DELETE FROM streaks;"'))
    assert is_ask(bash("claude --dangerously-skip-permissions"))


def test_safe_bash_commands_pass_silently():
    assert bash("git status") is None
    assert bash("python -m pytest -q") is None
    assert bash("rm build.log") is None  # single file, no -rf
    assert bash('psql -c "DELETE FROM streaks WHERE user_id = 7;"') is None  # has WHERE
    assert bash("npx prisma migrate dev") is None  # forward migration, not reset


def test_schema_and_migration_edits_are_gated():
    assert is_ask(edit("supabase/migrations/0001_init.sql"))
    assert is_ask(edit("db/migrations/20260702_add_streaks.sql"))
    assert is_ask(edit("prisma/schema.prisma"))
    assert is_ask(edit("app/db/schema.sql"))


def test_ordinary_edits_and_reads_pass_silently():
    assert edit("app/components/Feed.tsx") is None
    assert edit("tests/test_streaks.py") is None
    assert gate.process({"tool_name": "Read", "tool_input": {"file_path": "supabase/migrations/0001_init.sql"}}) is None


def test_reason_is_plain_english():
    out = bash("npx supabase db reset")
    reason = out["hookSpecificOutput"]["permissionDecisionReason"]
    assert "database" in reason.lower()
    assert "approve" in reason.lower() or "sure" in reason.lower()


def test_opt_out_marker_disables(tmp_path):
    (tmp_path / ".no-destructive-gate").write_text("", encoding="utf-8")
    assert bash("rm -rf build/", cwd=str(tmp_path)) is None
    assert edit("prisma/schema.prisma", cwd=str(tmp_path)) is None
