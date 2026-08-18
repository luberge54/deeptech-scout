"""Verify the local setup before running the pipeline.

Checks, in order:
  1. The .env file exists and ANTHROPIC_API_KEY is set.
  2. The key has the expected shape (never prints the key itself).
  3. A minimal live API call succeeds — this is what actually proves the key
     is valid and the account has credits.

Run with:  .venv\\Scripts\\python.exe src\\check_setup.py
"""

import os
import sys

import anthropic
from dotenv import load_dotenv

# The scoping doc (docs/00-scoping.md section 4d) assigns Sonnet to the
# collection steps. The check uses the same model so it exercises the real path.
CHECK_MODEL = "claude-sonnet-5"
CHECK_MAX_TOKENS = 16
EXPECTED_KEY_PREFIX = "sk-ant-"
PLACEHOLDER_FRAGMENT = "xxxx"


def read_api_key() -> str:
    """Load ANTHROPIC_API_KEY from .env and reject obviously unusable values.

    Returns the key. Exits with a readable message if anything is wrong.
    The key itself is never printed.
    """
    load_dotenv()
    key = os.getenv("ANTHROPIC_API_KEY", "").strip()

    if not key:
        sys.exit(
            "FAIL: ANTHROPIC_API_KEY is empty or missing.\n"
            "      Copy env.example to .env and paste your real key into it."
        )

    if PLACEHOLDER_FRAGMENT in key:
        sys.exit(
            "FAIL: .env still contains the placeholder value.\n"
            "      Replace sk-ant-xxxx... with the real key from console.anthropic.com."
        )

    if not key.startswith(EXPECTED_KEY_PREFIX):
        sys.exit(
            f"FAIL: the key does not start with '{EXPECTED_KEY_PREFIX}'.\n"
            "      Check you copied the whole value and nothing else."
        )

    # Plain ASCII output only: the Windows console default codepage mangles
    # characters like the em dash.
    print(f"OK  key found - starts with '{EXPECTED_KEY_PREFIX}', length {len(key)} characters")
    return key


def call_api(api_key: str) -> None:
    """Make the smallest useful request to confirm the key and credits work."""
    client = anthropic.Anthropic(api_key=api_key)

    try:
        response = client.messages.create(
            model=CHECK_MODEL,
            max_tokens=CHECK_MAX_TOKENS,
            messages=[{"role": "user", "content": "Reply with the single word: ready"}],
        )
    except anthropic.AuthenticationError:
        sys.exit(
            "FAIL: the API rejected the key (authentication error).\n"
            "      The key is malformed, revoked, or from a different account."
        )
    except anthropic.PermissionDeniedError:
        sys.exit(
            "FAIL: the key is valid but lacks permission for this model.\n"
            "      Check the key's scope in the console."
        )
    except anthropic.APIStatusError as error:
        sys.exit(
            f"FAIL: the API returned an error (HTTP {error.status_code}).\n"
            f"      {error.message}\n"
            "      If this mentions credit or billing, add credits in the console."
        )
    except anthropic.APIConnectionError:
        sys.exit("FAIL: could not reach the API. Check your internet connection.")

    reply = next((block.text for block in response.content if block.type == "text"), "")
    used = response.usage

    print(f"OK  live API call succeeded using {CHECK_MODEL}")
    print(f"    model replied: {reply.strip()!r}")
    print(f"    tokens used: {used.input_tokens} in / {used.output_tokens} out")


def main() -> None:
    print("Checking DeepTech Scout setup...\n")
    api_key = read_api_key()
    call_api(api_key)
    print("\nAll checks passed. Ready to build step 1.")


if __name__ == "__main__":
    main()
