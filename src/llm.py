"""The only file that talks to a model.

A notice photo goes out with a JSON schema. Every call appends one usage line.
max_tokens is capped so a request cannot reserve the model's full output budget.
"""
from __future__ import annotations

import base64
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

from openai import OpenAI

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
LOG_PATH = Path(os.environ.get("MENTOR_USAGE_LOG", "logs/usage.jsonl"))
CHAT_MODEL = os.environ.get("MODEL", "google/gemini-3.8-flash")

# USD per million tokens (input, output). Promo price checked 13 October 2026.
PRICES = {
    "google/gemini-3.8-flash": (0.75, 3.75),
}

_client: OpenAI | None = None


def get_client() -> OpenAI:
    global _client
    if _client is None:
        key = os.environ.get("OPENROUTER_API_KEY")
        if not key:
            raise RuntimeError("OPENROUTER_API_KEY is not set; copy .env.example to .env")
        _client = OpenAI(base_url=OPENROUTER_BASE_URL, api_key=key)
    return _client


class _LazyClient:
    def __getattr__(self, name):
        return getattr(get_client(), name)


client = _LazyClient()


def data_url(image: bytes) -> str:
    return "data:image/jpeg;base64," + base64.b64encode(image).decode("ascii")


def cost_usd(model: str, tokens_in: int, tokens_out: int) -> float:
    price_in, price_out = PRICES.get(model, (0.0, 0.0))
    return round((tokens_in * price_in + tokens_out * price_out) / 1_000_000, 6)


def log_usage(resp, latency_ms: int = 0, kind: str = "chat") -> dict:
    usage = getattr(resp, "usage", None)
    tokens_in = getattr(usage, "prompt_tokens", 0) or 0
    tokens_out = getattr(usage, "completion_tokens", 0) or 0
    model = getattr(resp, "model", None) or CHAT_MODEL
    line = {
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "kind": kind,
        "model": model,
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "cost_usd": cost_usd(model, tokens_in, tokens_out),
        "latency_ms": latency_ms,
    }
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(line) + "\n")
    return line


def complete_json(prompt: str, image: bytes | None = None, schema: dict | None = None) -> dict:
    content: list[dict] = [{"type": "text", "text": prompt}]
    if image is not None:
        content.append({"type": "image_url", "image_url": {"url": data_url(image)}})
    started = time.perf_counter()
    resp = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[{"role": "user", "content": content}],
        response_format={
            "type": "json_schema",
            "json_schema": {"name": "reply", "schema": schema or {}, "strict": True},
        },
        temperature=0,
        max_tokens=1024,
    )
    log_usage(resp, latency_ms=int((time.perf_counter() - started) * 1000))
    return json.loads(resp.choices[0].message.content)
