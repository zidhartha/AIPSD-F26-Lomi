"""The one place a model is called, per AGENTS.md. Imported lazily by src/act.py, so
tests and CI never import it and never need a key.

complete_tools() sends messages plus tool schemas to the model and returns the reply in a
small fixed shape: {content, tool_calls, reasoning_details}. The key comes from the
environment (OPENROUTER_API_KEY), never from code. Every call appends one line to
logs/usage.jsonl: model, tokens in, tokens out, cost, latency.
"""
from __future__ import annotations

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

USAGE_LOG = Path(os.environ.get("AIMENTOR_USAGE_LOG", "logs/usage.jsonl"))
MODEL = os.environ.get("MODEL", "google/gemini-3.8-flash")


def ms_since(t0: float) -> float:
    return round((time.perf_counter() - t0) * 1000, 1)


def complete_tools(messages: list[dict], tools: list[dict]) -> dict:
    """Call the model once with tools. Returns {content, tool_calls, reasoning_details}."""
    from openai import OpenAI  # imported here so importing this module never needs the package

    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        raise RuntimeError("OPENROUTER_API_KEY is not set. Tests and CI must not reach this path.")

    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=key)
    t0 = time.perf_counter()
    resp = client.chat.completions.create(model=MODEL, messages=messages, tools=tools)
    choice = resp.choices[0].message
    calls = [{"id": c.id, "name": c.function.name, "arguments": c.function.arguments}
             for c in (choice.tool_calls or [])]
    _log_usage(resp, ms_since(t0))
    return {"content": choice.content, "tool_calls": calls,
            "reasoning_details": getattr(choice, "reasoning_details", None)}


def _log_usage(resp, latency_ms: float) -> None:
    u = getattr(resp, "usage", None)
    line = {"ts": datetime.now(timezone.utc).isoformat(timespec="seconds"), "model": MODEL,
            "tokens_in": getattr(u, "prompt_tokens", None), "tokens_out": getattr(u, "completion_tokens", None),
            "cost": getattr(u, "cost", None), "latency_ms": latency_ms}
    USAGE_LOG.parent.mkdir(parents=True, exist_ok=True)
    with USAGE_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(line) + "\n")
