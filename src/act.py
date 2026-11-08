"""The three gates in front of every tool call. No model, no key.

call_tool() never raises. A refusal is a dict the model can read, plus one line in the tool log.
The caller's identity is not an argument and is not written to the log.
"""
from __future__ import annotations

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

from pydantic import ValidationError

from .tools import Tool, ToolFailure

MAX_ROUNDS = 3


def brief(err: ValidationError) -> str:
    """Which field, and what was wrong. No stack trace."""
    return "; ".join(
        f"{'.'.join(map(str, item['loc'])) or 'arguments'}: {item['msg']}" for item in err.errors()
    )


def call_tool(call: dict, allowed: dict[str, Tool], caller: str | None) -> dict:
    started = time.perf_counter()
    tool = allowed.get(call["name"])
    if tool is None:
        return _log(call, started, error=f"no tool named {call['name']!r} is available")
    try:
        args = tool.args.model_validate_json(call["arguments"] or "{}")
    except ValidationError as err:
        return _log(call, started, error=f"invalid arguments: {brief(err)}")
    try:
        out = tool.run(args)
    except ToolFailure as err:
        return _log(call, started, error=str(err))
    return _log(call, started, result=out.model_dump(mode="json"))


def _log(call: dict, started: float, result: dict | None = None, error: str | None = None) -> dict:
    line = {
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "tool": call["name"],
        "arguments": call["arguments"],
        "ok": error is None,
        "error": error,
        "latency_ms": round((time.perf_counter() - started) * 1000),
    }
    path = Path(os.environ.get("MENTOR_TOOL_LOG", "logs/tools.jsonl"))
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(line) + "\n")
    return {**line, "result": result}


__all__ = ["MAX_ROUNDS", "brief", "call_tool"]
