"""The one bridge between the eval runner and YOUR AI feature.

Fill in run_feature() so it calls your real AI feature and returns its text output.
The runner calls this once per eval case.

Rules:
- Return the feature's actual output as a string.
- RAISE on error (network, auth, etc.) — do NOT return a fake/empty string. The runner treats a
  raised error as "the eval broke" (never a silent pass).
- Read any API keys from environment variables, never hardcode them.
"""


def run_feature(input_text: str) -> str:
    # TODO: call your real AI feature here and return its text output.
    # Example:
    #   from app.support import draft_reply
    #   return draft_reply(input_text)
    raise NotImplementedError(
        "Fill in run_feature() in feature_adapter.py to call your AI feature."
    )
