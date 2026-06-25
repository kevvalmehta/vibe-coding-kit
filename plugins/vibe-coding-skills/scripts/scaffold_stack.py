#!/usr/bin/env python3
"""scaffold_stack.py — Conductor v7: minimal stack scaffolding (Option 1).

Creates a MINIMAL, runnable starter for a chosen stack so an empty folder becomes something that runs
locally — enough to start building, no more. The doer companion to `/stack` (which only recommends).

HARD GUARANTEES:
- NEVER overwrites an existing file — only creates what's missing; reports created vs skipped.
- NEVER pushes/merges/deploys — it only writes local starter files.
- Declines unknown / non-scaffoldable stacks instead of writing a wrong skeleton.

Spec: specs/013-stack-scaffold/spec.md
"""
import sys
from pathlib import Path

_GITIGNORE = """\
# secrets — never commit
.env
# python
__pycache__/
*.pyc
.venv/
venv/
# node
node_modules/
.next/
dist/
# os / editor
.DS_Store
.idea/
.vscode/
"""

_ENV_EXAMPLE = "# Copy this file to .env and fill in real values. Never commit .env.\n# EXAMPLE_KEY=your-value-here\n"


def _readme(title, run_lines, live_line):
    run = "\n".join(run_lines)
    return (
        f"# {title}\n\n"
        f"A minimal starter created by `/scaffold`. It runs as-is — start building from here.\n\n"
        f"## How to run it (on your computer)\n\n```\n{run}\n```\n\n"
        f"## How to put this live\n\n{live_line}\n\n"
        f"## Growing it\n\n"
        f"Ask the kit to add features one at a time — `/safe-change` for edits, `/start` or `/ship`\n"
        f"for bigger features. Each addition is built tests-first and won't break what already works.\n"
    )


# stack key -> list of (relative path, file content)
TEMPLATES = {
    "streamlit": [
        ("requirements.txt", "streamlit\n"),
        ("app.py", 'import streamlit as st\n\nst.title("My App")\nst.write("It works! Start building here.")\n'),
        (".gitignore", _GITIGNORE),
        (".env.example", _ENV_EXAMPLE),
        ("README.md", _readme(
            "My Streamlit App",
            ["pip install -r requirements.txt", "streamlit run app.py"],
            "Push this folder to GitHub, then connect it at https://streamlit.io/cloud "
            "(Streamlit Community Cloud — free). Not Vercel: Vercel can't host Streamlit.",
        )),
    ],
    "fastapi": [
        ("requirements.txt", "fastapi\nuvicorn[standard]\n"),
        ("main.py",
         'from fastapi import FastAPI\n\napp = FastAPI()\n\n\n@app.get("/")\n'
         'def read_root():\n    return {"status": "it works"}\n'),
        (".gitignore", _GITIGNORE),
        (".env.example", _ENV_EXAMPLE),
        ("README.md", _readme(
            "My API",
            ["pip install -r requirements.txt", "uvicorn main:app --reload"],
            "Deploy on an always-on container host like Render or Railway (~$7/mo). "
            "A serverless host like Vercel is usually the wrong fit for an always-on API.",
        )),
    ],
    "python-script": [
        ("requirements.txt", "# add your dependencies here, e.g. requests\n"),
        ("main.py",
         'def main():\n    print("It works! Put your automation here.")\n\n\n'
         'if __name__ == "__main__":\n    main()\n'),
        (".gitignore", _GITIGNORE),
        (".env.example", _ENV_EXAMPLE),
        ("README.md", _readme(
            "My Automation Script",
            ["pip install -r requirements.txt", "python main.py"],
            "For a scheduled job, run it on a timer with GitHub Actions (free for public repos). "
            "For long or guaranteed-timing jobs, use a worker host like Render Cron / Railway.",
        )),
    ],
    "nextjs": [
        (".gitignore", _GITIGNORE),
        (".env.example", _ENV_EXAMPLE),
        ("README.md", _readme(
            "My Web App (Next.js)",
            ["npx create-next-app@latest .", "npm run dev"],
            "Deploy on Vercel (made for Next.js): push to GitHub and import the repo at "
            "https://vercel.com. Use Supabase for the database.",
        )),
    ],
    "static-site": [
        (".gitignore", _GITIGNORE),
        (".env.example", _ENV_EXAMPLE),
        ("README.md", _readme(
            "My Marketing Site",
            ["npm create astro@latest .", "npm run dev"],
            "Deploy on a static host with a free CDN: Netlify, Cloudflare Pages, or Vercel. "
            "Push to GitHub and connect the repo.",
        )),
    ],
}


def list_stacks():
    """Return the supported stack keys."""
    return sorted(TEMPLATES.keys())


def scaffold(stack, target, force=False):
    """Create the minimal starter for `stack` into `target`. Never overwrites unless force=True.

    Returns {"created": [...], "skipped": [...], "unknown": bool}. For an unknown stack, writes nothing.
    """
    files = TEMPLATES.get(stack)
    if files is None:
        return {"created": [], "skipped": [], "unknown": True}

    target = Path(target)
    created, skipped = [], []
    for rel, content in files:
        path = target / rel
        if path.exists() and not force:
            skipped.append(str(path))
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        created.append(str(path))
    return {"created": created, "skipped": skipped, "unknown": False}


def main(argv=None):
    """CLI: scaffold_stack.py <stack> <target-dir>. Always exits 0 (defensive)."""
    argv = argv if argv is not None else sys.argv[1:]
    if len(argv) < 2:
        print("Usage: python scaffold_stack.py <stack> <target-dir>")
        print("Supported stacks: " + ", ".join(list_stacks()))
        return 0

    stack, target = argv[0], argv[1]
    try:
        result = scaffold(stack, target)
    except Exception as exc:  # defensive — a helper must never crash a session
        print(f"Could not scaffold (a write error occurred): {exc}")
        return 0

    if result["unknown"]:
        print(f"Can't scaffold '{stack}' — that is not a supported stack to scaffold.")
        print("Supported stacks: " + ", ".join(list_stacks()))
        print("For anything else (e.g. a no-code mobile builder), use that tool's own setup, or run /stack.")
        return 0

    print(f"Created {len(result['created'])} file(s) in {target}:")
    for p in result["created"]:
        print(f"  + {p}")
    if result["skipped"]:
        print(f"Skipped {len(result['skipped'])} existing file(s) (never overwritten):")
        for p in result["skipped"]:
            print(f"  = {p}")
    print("\nNext: open the new README.md — it tells you how to run it and how to put it live.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
