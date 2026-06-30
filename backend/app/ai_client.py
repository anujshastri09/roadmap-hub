import os
import json
import logging
from anthropic import Anthropic

logger = logging.getLogger("roadmap_hub.ai")

MODEL = "claude-sonnet-4-6"

_client = None


def get_client() -> Anthropic:
    """Lazily instantiate the Anthropic client so the app can still boot
    (and serve every non-AI endpoint) even if no API key is configured."""
    global _client
    if _client is None:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError(
                "ANTHROPIC_API_KEY is not set. Add it to your .env file to use AI features."
            )
        _client = Anthropic(api_key=api_key)
    return _client


def call_claude(system: str, user_message: str, max_tokens: int = 2000) -> str:
    """Single-turn completion call. Returns plain text."""
    client = get_client()
    response = client.messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user_message}],
    )
    return "".join(block.text for block in response.content if block.type == "text")


def call_claude_chat(system: str, history: list[dict], max_tokens: int = 1000) -> str:
    """Multi-turn completion. `history` is a list of {"role": "user"|"assistant", "content": str}."""
    client = get_client()
    response = client.messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        system=system,
        messages=history,
    )
    return "".join(block.text for block in response.content if block.type == "text")


def stream_claude_chat(system: str, history: list[dict], max_tokens: int = 1000):
    """Generator yielding text chunks as they arrive from Claude, for Server-Sent Events streaming.
    Used so the frontend can render the assistant's reply token-by-token instead of waiting
    for the full response."""
    client = get_client()
    with client.messages.stream(
        model=MODEL,
        max_tokens=max_tokens,
        system=system,
        messages=history,
    ) as stream:
        for text_chunk in stream.text_stream:
            yield text_chunk


def extract_json(raw_text: str) -> dict:
    """Claude sometimes wraps JSON in markdown fences despite instructions — strip them."""
    text = raw_text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse AI JSON response: {e}\nRaw: {raw_text[:500]}")
        raise
