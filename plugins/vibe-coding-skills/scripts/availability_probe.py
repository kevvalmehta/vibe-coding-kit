#!/usr/bin/env python3
"""availability_probe.py — Conductor v6: portable on-disk availability check.

Reads `.mcp.json` (mcpServers) + `.claude/settings.json` (+ settings.local.json) (enabledPlugins) and
reports which MCP servers + plugins are CONFIGURED, surfacing the Conductor's optional resources
(gitmcp, cookbook, the claude-code-setup recommender).

IMPORTANT: this reports CONFIG INTENT (what's listed on disk), NOT live state (what's actually
responding this session). The in-session tool list (Conductor v2) reports live state; this is its
portable, cross-tool complement. Defensive by construction: missing/malformed files never raise.

Spec: specs/012-availability-prober/spec.md
"""
import json
import sys
from pathlib import Path

CAVEAT = "Note: 'configured' means listed in your config files — not the same as 'responding live' " \
    "right now. For live state, check the in-session tool list (Conductor v2)."

# substring that identifies the recommender plugin (key looks like "claude-code-setup@marketplace")
_RECOMMENDER_KEY = "claude-code-setup"


def _load_json(path):
    """Read + parse a JSON file. Return the object, or None on any error (never raises)."""
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception:
        return None


def _enabled_plugins(root):
    """Merge enabledPlugins from settings.json then settings.local.json (local wins). dict name->bool."""
    merged = {}
    for name in ("settings.json", "settings.local.json"):
        data = _load_json(Path(root) / ".claude" / name)
        if isinstance(data, dict):
            plugins = data.get("enabledPlugins")
            if isinstance(plugins, dict):
                merged.update(plugins)
    return merged


def probe(root="."):
    """Return {mcp_servers, plugins, conductor_resources} for the project rooted at `root`."""
    root = Path(root)

    mcp_servers = []
    mcp = _load_json(root / ".mcp.json")
    if isinstance(mcp, dict) and isinstance(mcp.get("mcpServers"), dict):
        mcp_servers = sorted(mcp["mcpServers"].keys())

    plugins = _enabled_plugins(root)

    recommender = any(
        _RECOMMENDER_KEY in str(key) and bool(value) for key, value in plugins.items()
    )

    return {
        "mcp_servers": mcp_servers,
        "plugins": plugins,
        "conductor_resources": {
            "gitmcp": "gitmcp" in mcp_servers,
            "cookbook": "cookbook" in mcp_servers,
            "recommender": recommender,
        },
    }


def _summary(result):
    res = result["conductor_resources"]
    parts = [f"{name}: {'configured' if ok else 'not configured'}" for name, ok in res.items()]
    return "Conductor resources — " + " · ".join(parts) + "\n" + CAVEAT


def main(argv=None):
    """Print a machine-readable JSON result + a plain-English summary + the caveat. Always exit 0."""
    argv = argv if argv is not None else sys.argv[1:]
    root = argv[0] if argv else "."
    try:
        result = probe(root)
    except Exception:
        # defensive backstop — a helper must never crash a session
        result = {"mcp_servers": [], "plugins": {}, "conductor_resources":
                  {"gitmcp": False, "cookbook": False, "recommender": False}}
    print(json.dumps(result, indent=2))
    print(_summary(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
