# tests/test_preflight_gate.py
"""The pre-flight gate mechanizes the three solo-founder burn vectors deterministically:
a hardcoded secret, a table without Row-Level Security, or an API route with no rate
limit must FAIL loud (non-zero exit) — not be talked out of by a model. Checks that don't
apply SKIP; only a real FAIL fails the gate."""
import importlib.util
import subprocess
from pathlib import Path

from _kitpaths import scripts_dir

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location(
    "preflight_gate", scripts_dir(ROOT) / "preflight_gate.py"
)
pg = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pg)


def make_repo(tmp_path):
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.email", "t@t"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=tmp_path, check=True)
    return tmp_path


def commit_all(tmp_path):
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-qm", "snapshot"], cwd=tmp_path, check=True)


def status_of(checks, name):
    return next(c["status"] for c in checks if c["name"] == name)


# Built at runtime so the literal never appears in this file — otherwise the gate
# (correctly) flags its own test suite when scanning the kit repo. AWS's documented
# example key, split: "AKIA" + "IOSFODNN7EXAMPLE".
FAKE_AWS_KEY = "AKIA" + "IOSFODNN7EXAMPLE"


def test_clean_repo_passes_with_skips(tmp_path):
    make_repo(tmp_path)
    (tmp_path / "hello.py").write_text("print('hi')\n", encoding="utf-8")
    commit_all(tmp_path)
    checks, ok = pg.process(tmp_path)
    assert ok is True
    assert status_of(checks, "secrets") == "PASS"
    assert status_of(checks, "rls") == "SKIP"
    assert status_of(checks, "rate_limit") == "SKIP"


def test_planted_aws_key_fails_secrets(tmp_path):
    make_repo(tmp_path)
    (tmp_path / "config.py").write_text(
        f"AWS_KEY = '{FAKE_AWS_KEY}'\n", encoding="utf-8"
    )
    commit_all(tmp_path)
    checks, ok = pg.process(tmp_path)
    assert ok is False
    assert status_of(checks, "secrets") == "FAIL"


def test_secrets_skip_env_example_and_fixtures(tmp_path):
    make_repo(tmp_path)
    (tmp_path / ".env.example").write_text(
        f"AWS_KEY={FAKE_AWS_KEY}\n", encoding="utf-8"
    )
    fixtures = tmp_path / "tests" / "fixtures"
    fixtures.mkdir(parents=True)
    (fixtures / "sample.txt").write_text(FAKE_AWS_KEY + "\n", encoding="utf-8")
    commit_all(tmp_path)
    checks, ok = pg.process(tmp_path)
    assert ok is True
    assert status_of(checks, "secrets") == "PASS"


def test_untracked_secret_is_ignored(tmp_path):
    make_repo(tmp_path)
    (tmp_path / "keep.py").write_text("print('hi')\n", encoding="utf-8")
    commit_all(tmp_path)
    # Not committed / not tracked -> the sweep does not see it.
    (tmp_path / "leak.py").write_text(f"KEY='{FAKE_AWS_KEY}'\n", encoding="utf-8")
    checks, ok = pg.process(tmp_path)
    assert ok is True
    assert status_of(checks, "secrets") == "PASS"


def test_migration_without_rls_fails_and_alter_passes(tmp_path):
    make_repo(tmp_path)
    mig = tmp_path / "migrations"
    mig.mkdir()
    sql = mig / "001_init.sql"
    sql.write_text("CREATE TABLE users (id int primary key);\n", encoding="utf-8")
    commit_all(tmp_path)
    checks, ok = pg.process(tmp_path)
    assert ok is False
    assert status_of(checks, "rls") == "FAIL"

    sql.write_text(
        "CREATE TABLE users (id int primary key);\n"
        "ALTER TABLE users ENABLE ROW LEVEL SECURITY;\n",
        encoding="utf-8",
    )
    commit_all(tmp_path)
    checks, ok = pg.process(tmp_path)
    assert ok is True
    assert status_of(checks, "rls") == "PASS"


def test_supabase_migrations_are_checked(tmp_path):
    make_repo(tmp_path)
    mig = tmp_path / "supabase" / "migrations"
    mig.mkdir(parents=True)
    (mig / "001.sql").write_text(
        "CREATE TABLE orders (id int);\n", encoding="utf-8"
    )
    commit_all(tmp_path)
    checks, ok = pg.process(tmp_path)
    assert status_of(checks, "rls") == "FAIL"


def test_api_route_without_limiter_fails_rate_limit(tmp_path):
    make_repo(tmp_path)
    route = tmp_path / "app" / "api" / "hello"
    route.mkdir(parents=True)
    (route / "route.ts").write_text(
        "export async function GET() { return new Response('hi'); }\n", encoding="utf-8"
    )
    (tmp_path / "package.json").write_text(
        '{"name":"x","dependencies":{"next":"14.0.0"}}\n', encoding="utf-8"
    )
    commit_all(tmp_path)
    checks, ok = pg.process(tmp_path)
    assert ok is False
    assert status_of(checks, "rate_limit") == "FAIL"


def test_api_route_with_limiter_passes(tmp_path):
    make_repo(tmp_path)
    route = tmp_path / "app" / "api" / "hello"
    route.mkdir(parents=True)
    (route / "route.ts").write_text(
        "export async function GET() { return new Response('hi'); }\n", encoding="utf-8"
    )
    (tmp_path / "package.json").write_text(
        '{"name":"x","dependencies":{"express-rate-limit":"7.0.0"}}\n', encoding="utf-8"
    )
    commit_all(tmp_path)
    checks, ok = pg.process(tmp_path)
    assert ok is True
    assert status_of(checks, "rate_limit") == "PASS"


def test_json_output_shape(tmp_path):
    make_repo(tmp_path)
    (tmp_path / "hello.py").write_text("print('hi')\n", encoding="utf-8")
    commit_all(tmp_path)
    result = subprocess.run(
        ["python", str(scripts_dir(ROOT) / "preflight_gate.py"), "--json"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    import json

    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert isinstance(payload["checks"], list)
    names = {c["name"] for c in payload["checks"]}
    assert names == {"secrets", "rls", "rate_limit"}
    for c in payload["checks"]:
        assert set(c) == {"name", "status", "details"}


def test_gate_exits_nonzero_on_fail(tmp_path):
    make_repo(tmp_path)
    (tmp_path / "config.py").write_text(
        f"AWS_KEY = '{FAKE_AWS_KEY}'\n", encoding="utf-8"
    )
    commit_all(tmp_path)
    result = subprocess.run(
        ["python", str(scripts_dir(ROOT) / "preflight_gate.py")],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    assert "FAIL" in result.stdout
