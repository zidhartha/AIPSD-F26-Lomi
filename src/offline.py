"""Offline stand-in for the chat model: no network, no key, no cost.

It answers with the full text of source [1] and cites [1], so an offline run measures
retrieval, refusal and citation checks, not the wording of a real answer.
"""
import json
import re
from pathlib import Path

from src import llm

MODEL = "offline-stand-in"
LOG_PATH = Path(__file__).resolve().parents[1] / "logs" / "usage-offline.jsonl"


def transport(body):
    prompt = body["messages"][-1]["content"]
    first = re.search(r"^\[1\] \([^)]*\) [^:]*: (.*)$", prompt, re.MULTILINE)
    reply = {"answer": first.group(1), "citations": [1], "grounded": True} if first else {
        "answer": "", "citations": [], "grounded": False}
    text = json.dumps(reply)
    chars_in = sum(len(m["content"]) for m in body["messages"])
    return {
        "model": MODEL,
        "choices": [{"message": {"content": text}}],
        "usage": {"prompt_tokens": chars_in // 4, "completion_tokens": len(text) // 4, "cost": 0.0},
    }


def chat(messages, *, feature, **kwargs):
    return llm.chat(messages, feature=feature, model=MODEL, transport=transport, log_path=LOG_PATH)
