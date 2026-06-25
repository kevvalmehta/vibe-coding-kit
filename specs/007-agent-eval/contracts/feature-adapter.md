# Contract: feature adapter

The one seam between the generic runner and a specific project's AI feature. Lives at
`evals/<feature>/feature_adapter.py`. Scaffolded as a stub; owner/AI fills it in.

## Required function

```python
def run_feature(input_text: str) -> str:
    """
    Send input_text to the project's real AI feature and return its text output.
    Raise on failure (do not return a fake/empty string) — the runner treats a raised
    error as a fail-loud condition, never a silent pass.
    """
```

## Rules

- MUST return the feature's actual output as a string. For features that return structured data,
  return the part being evaluated (e.g. the reply text), serialized to string.
- MUST raise on error (network, auth, etc.) rather than swallow it — the runner converts that into
  an exit-2 "eval broke" result, not a pass.
- SHOULD be cheap to call repeatedly; the runner may call it many times.
- MUST read any secrets (API keys) from environment variables, never hardcoded (Principle IV).

## Stub shipped by the skill

```python
def run_feature(input_text: str) -> str:
    # TODO: call your real AI feature here and return its text output.
    # Example: from app.support import draft_reply; return draft_reply(input_text)
    raise NotImplementedError("Fill in run_feature() to call your AI feature.")
```

The stub raises by design, so an unfilled adapter fails loudly instead of silently "passing."
