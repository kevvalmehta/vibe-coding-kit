#!/usr/bin/env python3
"""PostToolUse hook (Edit|Write|MultiEdit): flag imports that don't exist here.

Invented APIs usually enter a project as an import of a package the model hallucinated
(or never installed). This hook checks every import in the just-edited file:

- Python: OK if stdlib, installed in this environment (find_spec), or a local module
  (repo root, src/, app/, or a sibling of the edited file).
- JS/TS: OK if relative, a node builtin, declared in package.json, or in node_modules.

Anything else is fed straight back to the model: verify against real docs (GitMCP) or
install it — while fixing course is still cheap. Feedback only; the edit already
happened and is not rolled back. Always exits 0; errors are swallowed.
"""

import ast
import json
import re
import sys
from pathlib import Path

PY_EXTS = {".py"}
JS_EXTS = {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"}

NODE_BUILTINS = {
    "assert", "buffer", "child_process", "cluster", "console", "constants", "crypto",
    "dgram", "dns", "domain", "events", "fs", "http", "http2", "https", "inspector",
    "module", "net", "os", "path", "perf_hooks", "process", "punycode", "querystring",
    "readline", "repl", "stream", "string_decoder", "timers", "tls", "trace_events",
    "tty", "url", "util", "v8", "vm", "worker_threads", "zlib",
}

LOCAL_ROOTS = ("", "src", "app", "lib", "scripts", "tests")

JS_IMPORT_RE = re.compile(
    r"""(?:import\s+(?:[\w{}\s,*$]+\s+from\s+)?|require\s*\(\s*|import\s*\(\s*|export\s+[\w{}\s,*]+\s+from\s+)
        ['"](?P<spec>[^'"]+)['"]""",
    re.VERBOSE,
)


def _py_top_modules(source: str) -> set:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return set()
    mods = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            mods.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            mods.add(node.module.split(".")[0])
    return mods


def _py_exists(mod: str, root: Path, file_dir: Path) -> bool:
    if mod in getattr(sys, "stdlib_module_names", set()):
        return True
    for base in [file_dir] + [root / r if r else root for r in LOCAL_ROOTS]:
        if (base / f"{mod}.py").is_file() or (base / mod / "__init__.py").is_file() or (base / mod).is_dir():
            return True
    try:
        import importlib.util

        if importlib.util.find_spec(mod) is not None:
            return True
    except Exception:
        pass
    return False


def _js_bare_packages(source: str) -> set:
    pkgs = set()
    for m in JS_IMPORT_RE.finditer(source):
        spec = m.group("spec")
        if spec.startswith((".", "/", "~", "@/")) or spec.startswith("node:"):
            continue
        parts = spec.split("/")
        pkgs.add("/".join(parts[:2]) if spec.startswith("@") and len(parts) >= 2 else parts[0])
    return pkgs


def _js_declared(root: Path) -> set:
    declared = set()
    pkg_json = root / "package.json"
    if pkg_json.is_file():
        try:
            data = json.loads(pkg_json.read_text(encoding="utf-8"))
            for key in ("dependencies", "devDependencies", "peerDependencies"):
                declared.update((data.get(key) or {}).keys())
        except Exception:
            pass
    return declared


def _js_exists(pkg: str, root: Path, declared: set) -> bool:
    if pkg in NODE_BUILTINS or pkg in declared:
        return True
    return (root / "node_modules" / pkg).is_dir()


def missing_imports(file_path: Path, root: Path) -> list:
    """Sorted list of imports in file_path that resolve nowhere in this project."""
    ext = file_path.suffix.lower()
    try:
        source = file_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    if ext in PY_EXTS:
        return sorted(
            m for m in _py_top_modules(source) if not _py_exists(m, root, file_path.parent)
        )
    if ext in JS_EXTS:
        declared = _js_declared(root)
        return sorted(p for p in _js_bare_packages(source) if not _js_exists(p, root, declared))
    return []


def process(data: dict):
    """Return a feedback dict for the model, or None to stay silent."""
    if data.get("tool_name") not in ("Edit", "Write", "MultiEdit"):
        return None
    file_path = Path(data.get("tool_input", {}).get("file_path") or "")
    if file_path.suffix.lower() not in PY_EXTS | JS_EXTS or not file_path.is_file():
        return None
    root = Path(data.get("cwd") or Path.cwd())
    missing = missing_imports(file_path, root)
    if not missing:
        return None
    return {
        "decision": "block",
        "reason": (
            f"Import reality check: {file_path.name} imports "
            f"{', '.join(missing)} — not stdlib/builtin, not installed, not declared, and "
            "not a local module. This is how invented APIs land. Verify the real package "
            "name against live docs (GitMCP) and install it, or fix the import. If it IS "
            "correct (different environment/monorepo path), say so and continue."
        ),
    }


def main() -> int:
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
        out = process(data)
        if out:
            print(json.dumps(out))
    except Exception:
        pass  # a hook must never break a session
    return 0


if __name__ == "__main__":
    sys.exit(main())
