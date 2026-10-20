import json
import os
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_MODEL = "google/gemini-3.8-flash"
ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
LOG_PATH = Path(__file__).resolve().parents[1] / "logs" / "usage.jsonl"

# USD per million tokens (input, output); used only when the provider reports no cost.
PRICES = {"google/gemini-3.8-flash": (0.75, 3.75)}


class MissingKey(RuntimeError):
    pass


def model_name():
    return os.environ.get("MODEL") or DEFAULT_MODEL


def http_transport(body):
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        raise MissingKey("OPENROUTER_API_KEY is not set")
    request = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def price(model, tokens_in, tokens_out):
    if model not in PRICES:
        return None
    rate_in, rate_out = PRICES[model]
    return (tokens_in * rate_in + tokens_out * rate_out) / 1_000_000


def chat(messages, *, feature, model=None, json_mode=True, transport=http_transport, log_path=LOG_PATH):
    model = model or model_name()
    body = {"model": model, "messages": messages, "usage": {"include": True}}
    if json_mode:
        body["response_format"] = {"type": "json_object"}
    start = time.perf_counter()
    raw = transport(body)
    latency_ms = round((time.perf_counter() - start) * 1000)
    usage = raw.get("usage") or {}
    tokens_in = usage.get("prompt_tokens", 0)
    tokens_out = usage.get("completion_tokens", 0)
    cost, cost_source = usage.get("cost"), "provider"
    if cost is None:
        cost, cost_source = price(model, tokens_in, tokens_out), "price_table"
    line = {
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "feature": feature,
        "model": raw.get("model") or model,
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "cost_usd": cost,
        "cost_source": cost_source,
        "latency_ms": latency_ms,
    }
    log_path = Path(log_path)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as log:
        log.write(json.dumps(line) + "\n")
    return {"text": raw["choices"][0]["message"]["content"], **line}
