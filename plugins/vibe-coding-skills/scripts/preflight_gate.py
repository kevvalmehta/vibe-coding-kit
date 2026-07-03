#!/usr/bin/env python3
"""Pre-flight security gate: three deterministic burn-vector checks, no LLM.

Solo-founder projects burn in production on a small set of mechanical mistakes: a
hardcoded secret gets committed, a database table ships without Row-Level Security, an
API route has no rate limit. This gate catches all three with plain regex/parsing — no
model in the loop, so it can't be talked out of a finding.

Three checks:
  - secrets:    regex sweep of git-tracked text files for hardcoded keys/tokens/PEM.
  - rls:        every CREATE TABLE in migration SQL has a matching ENABLE ROW LEVEL SECURITY.
  - rate_limit: if API routes exist, at least one recognized limiter is present.

Checks that don't apply (no migrations, no API routes) report SKIP, not FAIL. Unlike the
session hooks, this is a GATE: it fails LOUD (exit non-zero) on any FAIL. It still refuses
to crash — unreadable files are skipped, not fatal.

Usage:
  python scripts/preflight_gate.py          # human-readable table, exit 1 on any FAIL
  python scripts/preflight_gate.py --json    # {"checks":[...],"ok":bool} for CI
"""

import json
import re
import subprocess
import sys
from pathlib import Path

# --- secret patterns (name -> compiled regex) --------------------------------
SECRET_PATTERNS = {
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "Google API key": re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b"),
    "OpenAI/Anthropic key": re.compile(r"\bsk-(?:ant-)?[0-9A-Za-z_\-]{16,}\b"),
    "GitHub token": re.compile(r"\bghp_[0-9A-Za-z]{36}\b"),
    "Private key (PEM)": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY-----"),
    "Generic secret assignment": re.compile(
        r"(?i)(?:api[_-]?key|secret|token|passwd|password)\s*[:=]\s*['\"][^'\"]{16,}['\"]"
    ),
}

# Files that legitimately carry example/placeholder secrets or are noise for this sweep.
_SKIP_BASENAMES = {
    ".env.example",
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "poetry.lock",
    "Pipfile.lock",
    "composer.lock",
    "Cargo.lock",
    "go.sum",
}

# Path fragments (posix-style) whose files are skipped in the secret sweep.
_SKIP_PATH_FRAGMENTS = ("tests/fixtures", "test/fixtures")

# Extensions we treat as text worth scanning. Anything else is assumed binary/irrelevant.
_TEXT_SUFFIXES = {
    ".py", ".js", ".jsx", ".ts", ".tsx", ".json", ".yaml", ".yml", ".toml", ".ini",
    ".cfg", ".env", ".sh", ".bash", ".ps1", ".sql", ".md", ".txt", ".go", ".rb", ".rs",
    ".java", ".php", ".c", ".cpp", ".h", ".cs", ".html", ".css", ".xml", ".conf",
}

# API-route signals: any of these existing means the project exposes routes.
_API_ROUTE_GLOBS = (
    "app/api/**/route.js", "app/api/**/route.ts", "app/api/**/route.jsx", "app/api/**/route.tsx",
    "pages/api/**/*.js", "pages/api/**/*.ts",
    "src/app/api/**/route.js", "src/app/api/**/route.ts",
    "src/pages/api/**/*.js", "src/pages/api/**/*.ts",
)

# Signals that a rate limiter is wired in somewhere.
_RATE_LIMIT_SIGNALS = re.compile(
    r"@limiter|slowapi|express-rate-limit|rate[_-]?limit|Ratelimit|upstash|"
    r"flask[_-]?limiter|django-ratelimit",
    re.IGNORECASE,
)


def _git_tracked_files(root: Path):
    """Git-tracked paths (relative Path objects), or None if root is not a git repo."""
    try:
        result = subprocess.run(
            ["git", "ls-files", "-z"],
            cwd=str(root),
            capture_output=True,
            text=True,
            timeout=15,
        )
    except Exception:
        return None
    if result.returncode != 0:
        return None
    return [Path(p) for p in result.stdout.split("\0") if p]


def _is_scannable(rel: Path) -> bool:
    posix = rel.as_posix()
    if rel.name in _SKIP_BASENAMES:
        return False
    if any(frag in posix for frag in _SKIP_PATH_FRAGMENTS):
        return False
    return rel.suffix.lower() in _TEXT_SUFFIXES


def find_secrets(root: Path):
    """Return a list of 'name: file (pattern)' hits for hardcoded secrets in tracked files."""
    tracked = _git_tracked_files(root)
    if tracked is None:
        return []
    hits = []
    for rel in tracked:
        if not _is_scannable(rel):
            continue
        abs_path = root / rel
        try:
            text = abs_path.read_text(encoding="utf-8", errors="strict")
        except Exception:
            continue  # unreadable / binary — skip, never crash
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                hits.append(f"{rel.as_posix()} ({label})")
    return hits


def _migration_sql_files(root: Path):
    files = set()
    for pattern in ("**/migrations/**/*.sql", "supabase/migrations/**/*.sql"):
        for p in root.glob(pattern):
            if p.is_file():
                files.add(p)
    return sorted(files)


_CREATE_TABLE_RE = re.compile(
    r"create\s+table\s+(?:if\s+not\s+exists\s+)?[\"'`]?([\w.]+)[\"'`]?", re.IGNORECASE
)
_ENABLE_RLS_RE = re.compile(
    r"alter\s+table\s+(?:only\s+)?[\"'`]?([\w.]+)[\"'`]?\s+enable\s+row\s+level\s+security",
    re.IGNORECASE,
)


def _table_leaf(name: str) -> str:
    """Bare table name without a schema qualifier ('public.users' -> 'users')."""
    return name.rsplit(".", 1)[-1].lower()


def check_rls(root: Path):
    """Return (applies, missing_tables). applies=False means SKIP (no migration SQL)."""
    files = _migration_sql_files(root)
    if not files:
        return False, []
    created, rls_enabled = set(), set()
    for p in files:
        try:
            text = p.read_text(encoding="utf-8", errors="strict")
        except Exception:
            continue  # unreadable — skip, never crash
        for m in _CREATE_TABLE_RE.finditer(text):
            created.add(_table_leaf(m.group(1)))
        for m in _ENABLE_RLS_RE.finditer(text):
            rls_enabled.add(_table_leaf(m.group(1)))
    missing = sorted(created - rls_enabled)
    return True, missing


def _has_api_routes(root: Path) -> bool:
    for pattern in _API_ROUTE_GLOBS:
        for p in root.glob(pattern):
            if p.is_file():
                return True
    return False


def check_rate_limit(root: Path):
    """Return (applies, found). applies=False means SKIP (no API routes detected)."""
    if not _has_api_routes(root):
        return False, False
    tracked = _git_tracked_files(root)
    candidates = tracked if tracked is not None else [
        p.relative_to(root) for p in root.rglob("*") if p.is_file()
    ]
    for rel in candidates:
        if not _is_scannable(rel) and rel.name not in ("package.json", "requirements.txt"):
            continue
        try:
            text = (root / rel).read_text(encoding="utf-8", errors="strict")
        except Exception:
            continue
        if _RATE_LIMIT_SIGNALS.search(text):
            return True, True
    return True, False


FIX_LINES = {
    "secrets": (
        "Remove the hardcoded secret and load it from an environment variable instead "
        "(store the real value in .env, which is never committed). Rotate any key that "
        "was already committed."
    ),
    "rls": (
        "Add 'ALTER TABLE <name> ENABLE ROW LEVEL SECURITY;' (plus access policies) for "
        "each listed table in your migrations, so users can only read their own rows."
    ),
    "rate_limit": (
        "Add a rate limiter to your API (e.g. express-rate-limit for Node, slowapi for "
        "FastAPI) so one visitor can't hammer your endpoints and run up your bill."
    ),
}


def run_checks(root: Path):
    """Run all three checks. Return the list of {name, status, details} dicts."""
    checks = []

    secret_hits = find_secrets(root)
    if secret_hits:
        checks.append({
            "name": "secrets",
            "status": "FAIL",
            "details": "Possible hardcoded secrets: " + "; ".join(secret_hits),
        })
    else:
        checks.append({
            "name": "secrets",
            "status": "PASS",
            "details": "No hardcoded secrets found in tracked text files.",
        })

    rls_applies, rls_missing = check_rls(root)
    if not rls_applies:
        checks.append({
            "name": "rls",
            "status": "SKIP",
            "details": "No migration SQL found — Row-Level Security check does not apply.",
        })
    elif rls_missing:
        checks.append({
            "name": "rls",
            "status": "FAIL",
            "details": "Tables with CREATE TABLE but no ENABLE ROW LEVEL SECURITY: "
                       + ", ".join(rls_missing),
        })
    else:
        checks.append({
            "name": "rls",
            "status": "PASS",
            "details": "Every created table enables Row-Level Security.",
        })

    rl_applies, rl_found = check_rate_limit(root)
    if not rl_applies:
        checks.append({
            "name": "rate_limit",
            "status": "SKIP",
            "details": "No API routes detected — rate-limit check does not apply.",
        })
    elif rl_found:
        checks.append({
            "name": "rate_limit",
            "status": "PASS",
            "details": "A rate-limit mechanism is present.",
        })
    else:
        checks.append({
            "name": "rate_limit",
            "status": "FAIL",
            "details": "API routes exist but no rate-limit mechanism was found.",
        })

    return checks


def render_table(checks) -> str:
    lines = ["Pre-flight security gate", "=" * 24]
    for c in checks:
        lines.append(f"[{c['status']:<4}] {c['name']:<12} {c['details']}")
    fails = [c for c in checks if c["status"] == "FAIL"]
    if fails:
        lines.append("")
        lines.append("How to fix:")
        for c in fails:
            lines.append(f"  - {c['name']}: {FIX_LINES.get(c['name'], '')}")
        lines.append("")
        lines.append("RESULT: FAIL — fix the above before deploying.")
    else:
        lines.append("")
        lines.append("RESULT: PASS")
    return "\n".join(lines)


def process(root: Path):
    """Return (checks, ok). ok is True only when no check FAILs."""
    checks = run_checks(root)
    ok = not any(c["status"] == "FAIL" for c in checks)
    return checks, ok


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    as_json = "--json" in argv
    root = Path.cwd()
    checks, ok = process(root)
    if as_json:
        print(json.dumps({"checks": checks, "ok": ok}))
    else:
        print(render_table(checks))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
