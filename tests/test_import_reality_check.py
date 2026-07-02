# tests/test_import_reality_check.py
"""The import reality check catches invented APIs at the door: right after an edit,
imports that are neither stdlib, installed, nor local get flagged back to the model —
before the invented package becomes a runtime failure the owner has to debug."""
import importlib.util
import json
from pathlib import Path

from _kitpaths import scripts_dir

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location(
    "import_reality_check", scripts_dir(ROOT) / "import_reality_check.py"
)
irc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(irc)


def test_python_stdlib_and_installed_ok(tmp_path):
    f = tmp_path / "app.py"
    f.write_text("import json\nimport pathlib\nimport pytest\n", encoding="utf-8")
    assert irc.missing_imports(f, tmp_path) == []


def test_python_invented_package_flagged(tmp_path):
    f = tmp_path / "app.py"
    f.write_text("import totally_invented_pkg_xyz\n", encoding="utf-8")
    assert irc.missing_imports(f, tmp_path) == ["totally_invented_pkg_xyz"]


def test_python_local_module_ok(tmp_path):
    (tmp_path / "helpers.py").write_text("x = 1\n", encoding="utf-8")
    f = tmp_path / "app.py"
    f.write_text("import helpers\n", encoding="utf-8")
    assert irc.missing_imports(f, tmp_path) == []


def test_python_local_sibling_of_edited_file_ok(tmp_path):
    sub = tmp_path / "app"
    sub.mkdir()
    (sub / "utils.py").write_text("x = 1\n", encoding="utf-8")
    f = sub / "main.py"
    f.write_text("import utils\n", encoding="utf-8")
    assert irc.missing_imports(f, tmp_path) == []


def test_python_syntax_error_is_silent(tmp_path):
    f = tmp_path / "app.py"
    f.write_text("def broken(:\n", encoding="utf-8")
    assert irc.missing_imports(f, tmp_path) == []


def test_js_relative_and_node_builtin_ok(tmp_path):
    f = tmp_path / "app.js"
    f.write_text(
        "import x from './local';\nimport fs from 'fs';\nimport p from 'node:path';\n",
        encoding="utf-8",
    )
    assert irc.missing_imports(f, tmp_path) == []


def test_js_declared_dependency_ok(tmp_path):
    (tmp_path / "package.json").write_text(
        json.dumps({"dependencies": {"react": "^18.0.0"}, "devDependencies": {"vitest": "^1.0.0"}}),
        encoding="utf-8",
    )
    f = tmp_path / "app.jsx"
    f.write_text("import React from 'react';\nimport { test } from 'vitest';\n", encoding="utf-8")
    assert irc.missing_imports(f, tmp_path) == []


def test_js_scoped_package_resolved_by_scope_name(tmp_path):
    (tmp_path / "package.json").write_text(
        json.dumps({"dependencies": {"@supabase/supabase-js": "^2.0.0"}}), encoding="utf-8"
    )
    f = tmp_path / "app.ts"
    f.write_text("import { createClient } from '@supabase/supabase-js';\n", encoding="utf-8")
    assert irc.missing_imports(f, tmp_path) == []


def test_js_invented_package_flagged(tmp_path):
    (tmp_path / "package.json").write_text(json.dumps({"dependencies": {}}), encoding="utf-8")
    f = tmp_path / "app.ts"
    f.write_text("import magic from 'totally-invented-lib-xyz';\n", encoding="utf-8")
    assert irc.missing_imports(f, tmp_path) == ["totally-invented-lib-xyz"]


def test_noncode_file_is_silent(tmp_path):
    f = tmp_path / "notes.md"
    f.write_text("import nothing\n", encoding="utf-8")
    data = {"tool_name": "Write", "tool_input": {"file_path": str(f)}, "cwd": str(tmp_path)}
    assert irc.process(data) is None


def test_process_flags_missing_with_feedback(tmp_path):
    f = tmp_path / "app.py"
    f.write_text("import totally_invented_pkg_xyz\n", encoding="utf-8")
    data = {"tool_name": "Edit", "tool_input": {"file_path": str(f)}, "cwd": str(tmp_path)}
    out = irc.process(data)
    assert out["decision"] == "block"
    assert "totally_invented_pkg_xyz" in out["reason"]
    assert "install" in out["reason"].lower() or "verify" in out["reason"].lower()
