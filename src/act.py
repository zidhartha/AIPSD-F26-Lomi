"""Function calling: the model asks for a tool, our code decides whether it runs.

The loop:
  1. send the question plus the schemas of the tools THIS caller may use
  2. no tool call in the reply -> that is the answer
  3. each tool call goes through call_tool(): offered? valid? then run, identity from us
  4. results (or errors) go back to the model as tool messages; repeat, at most MAX_ROUNDS times

call_tool() never raises. Whatever happens becomes a dict the model can read and one line in
logs/tools.jsonl: the log-entry half of the Evidence Rule for every call.
"""
from __future__ import annotations

import json
import os
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from pydantic import ValidationError

from .tools import Tool, ToolFailure, student_key, tools_for

MAX_ROUNDS = 3              # a budget: three model turns, then we stop and say so
TOOL_LOG = Path(os.environ.get("AIMENTOR_TOOL_LOG", "logs/tools.jsonl"))

SYSTEM = """You are AI Mentor. Answer a new employee's question only from the company handbook.
Call search_handbook whenever a question needs a fact from the documents. Never invent a policy.
If search_handbook returns no passage, say the handbook does not cover it; do not guess."""


def ms_since(t0: float) -> float:
    return round((time.perf_counter() - t0) * 1000, 1)


@dataclass
class Reply:
    status: str                                       # "answered" or "stopped"
    text: str
    calls: list[dict] = field(default_factory=list)   # one entry per tool call, as logged

    def to_dict(self) -> dict:
        return asdict(self)


def brief(e: ValidationError) -> str:
    """A validation error the model can act on: which field, what was wrong. No stack trace."""
    return "; ".join(f"{'.'.join(map(str, x['loc'])) or 'arguments'}: {x['msg']}" for x in e.errors())


def call_tool(call: dict, allowed: dict[str, Tool], student: str | None) -> dict:
    t0 = time.perf_counter()
    tool = allowed.get(call["name"])
    if tool is None:                                                     # 1 · not offered to this caller
        return _log(call, student, t0, error=f"no tool named {call['name']!r} is available")
    try:
        args = tool.args.model_validate_json(call["arguments"] or "{}")  # 2 · the contract, checked
    except ValidationError as e:
        return _log(call, student, t0, error=f"invalid arguments: {brief(e)}")
    try:
        out = tool.run(args, student=student) if tool.writes else tool.run(args)   # 3 · identity from us
    except ToolFailure as e:                                             # expected: no passage, etc.
        return _log(call, student, t0, error=str(e))
    return _log(call, student, t0, result=out.model_dump(mode="json"))  # 4 · the result, as data


def act(question: str, student: str | None = None, llm=None) -> Reply:
    """The full loop. Imports the model client lazily, so tests and CI never need a key."""
    if llm is None:
        from .llm import complete_tools
        llm = complete_tools
    allowed = tools_for(student)
    messages = [{"role": "system", "content": SYSTEM},
                {"role": "user", "content": question}]
    calls: list[dict] = []
    for _ in range(MAX_ROUNDS):
        msg = llm(messages, [t.schema() for t in allowed.values()])
        if not msg["tool_calls"]:
            return Reply("answered", msg["content"] or "", calls)
        messages.append(_as_assistant(msg))
        for call in msg["tool_calls"]:
            outcome = call_tool(call, allowed, student)
            calls.append(outcome)
            messages.append({"role": "tool", "tool_call_id": call["id"],
                             "content": json.dumps(outcome.get("result") or {"error": outcome["error"]})})
    return Reply("stopped", f"I couldn't finish that in {MAX_ROUNDS} steps. Nothing was changed.", calls)


def _as_assistant(msg: dict) -> dict:
    return {"role": "assistant", "content": msg["content"],
            "tool_calls": [{"id": c["id"], "type": "function",
                            "function": {"name": c["name"], "arguments": c["arguments"]}}
                           for c in msg["tool_calls"]]}


def _log(call: dict, student: str | None, t0: float, result: dict | None = None,
         error: str | None = None) -> dict:
    line = {"ts": datetime.now(timezone.utc).isoformat(timespec="seconds"), "tool": call["name"],
            "arguments": call["arguments"], "ok": error is None, "error": error,
            "student": student_key(student) if student else None, "latency_ms": ms_since(t0)}
    TOOL_LOG.parent.mkdir(parents=True, exist_ok=True)
    with TOOL_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(line) + "\n")
    return {**line, "result": result}
