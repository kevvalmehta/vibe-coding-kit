"""Guard test for the availability-prober (Conductor v6).

Spec: specs/012-availability-prober/spec.md  ·  Plan: specs/012-availability-prober/plan.md

Written FIRST (TDD). Pure filesystem/stdlib — no network/model. Guards that the prober parses the real
config shapes, surfaces the Conductor's optional resources, is defensive (never raises), and states the
"configured != live" caveat.
"""
import importlib.util
import io
import json
from pathlib import Path

from _kitpaths import scripts_dir

ROOT = Path(__file__).resolve().parent.parent
PROBE = scripts_dir(ROOT) / "availability_probe.py"

_spec = importlib.util.spec_from_file_location("availability_probe", PROBE)
availability_probe = importlib.util.module_from_spec(_spec)
if _spec.loader and PROBE.exists():
    _spec.loader.exec_module(availability_probe)


def _write(tmp_path, mcp=None, settings=None, local=None):
    if mcp is not None:
        (tmp_path / ".mcp.json").write_text(json.dumps(mcp), encoding="utf-8")
    if settings is not None:
        (tmp_path / ".claude").mkdir(exist_ok=True)
        (tmp_path / ".claude" / "settings.json").write_text(json.dumps(settings), encoding="utf-8")
    if local is not None:
        (tmp_path / ".claude").mkdir(exist_ok=True)
        (tmp_path / ".claude" / "settings.local.json").write_text(json.dumps(local), encoding="utf-8")


def test_T1_script_exists():
    assert PROBE.exists(), "scripts/availability_probe.py missing"


def test_T2_parses_mcp_servers(tmp_path):
    _write(tmp_path, mcp={"mcpServers": {"gitmcp": {"type": "http"}, "cookbook": {"type": "http"}}})
    r = availability_probe.probe(tmp_path)
    assert "gitmcp" in r["mcp_servers"] and "cookbook" in r["mcp_servers"]


def test_T3_parses_enabled_plugins(tmp_path):
    _write(tmp_path, settings={"enabledPlugins": {"claude-code-setup@claude-plugins-official": True}})
    r = availability_probe.probe(tmp_path)
    assert any("claude-code-setup" in k for k in r["plugins"]), "recommender plugin not parsed"


def test_T4_surfaces_conductor_resources(tmp_path):
    _write(
        tmp_path,
        mcp={"mcpServers": {"gitmcp": {}, "cookbook": {}}},
        settings={"enabledPlugins": {"claude-code-setup@claude-plugins-official": True}},
    )
    res = availability_probe.probe(tmp_path)["conductor_resources"]
    assert res["gitmcp"] is True and res["cookbook"] is True and res["recommender"] is True


def test_T5_local_settings_override(tmp_path):
    _write(
        tmp_path,
        settings={"enabledPlugins": {"claude-code-setup@claude-plugins-official": False}},
        local={"enabledPlugins": {"claude-code-setup@claude-plugins-official": True}},
    )
    # local wins → recommender enabled
    assert availability_probe.probe(tmp_path)["conductor_resources"]["recommender"] is True


def test_T6_plugin_false_is_disabled(tmp_path):
    _write(tmp_path, settings={"enabledPlugins": {"claude-code-setup@claude-plugins-official": False}})
    assert availability_probe.probe(tmp_path)["conductor_resources"]["recommender"] is False


def test_T7_missing_files_do_not_raise(tmp_path):
    r = availability_probe.probe(tmp_path)  # empty dir, nothing present
    assert r["conductor_resources"]["gitmcp"] is False
    assert r["mcp_servers"] == [], "mcp_servers must always be a list"


def test_T8_garbage_json_does_not_raise(tmp_path):
    (tmp_path / ".mcp.json").write_text("{not valid json", encoding="utf-8")
    (tmp_path / ".claude").mkdir()
    (tmp_path / ".claude" / "settings.json").write_text("also broken", encoding="utf-8")
    r = availability_probe.probe(tmp_path)  # must not raise
    assert r["conductor_resources"]["gitmcp"] is False


def test_T9_main_exits_zero_and_prints_caveat(tmp_path, monkeypatch):
    _write(tmp_path, mcp={"mcpServers": {"gitmcp": {}}})
    monkeypatch.chdir(tmp_path)
    cap = io.StringIO()
    monkeypatch.setattr("sys.stdout", cap)
    code = availability_probe.main([str(tmp_path)])
    assert code == 0
    out = cap.getvalue().lower()
    assert "configured" in out and "live" in out, "summary must state the configured-vs-live caveat"


def test_T10_emits_json(tmp_path, monkeypatch):
    _write(tmp_path, mcp={"mcpServers": {"gitmcp": {}}})
    cap = io.StringIO()
    monkeypatch.setattr("sys.stdout", cap)
    availability_probe.main([str(tmp_path)])
    out = cap.getvalue()
    # both the machine-readable JSON AND the plain-English summary must be printed
    assert "conductor_resources" in out, "must emit machine-readable JSON"
    assert "configured" in out.lower(), "must also print the plain-English summary"
