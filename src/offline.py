"""Offline stand-ins used when MENTOR_OFFLINE=1. They are not a model."""
from __future__ import annotations

import hashlib
import re
from types import SimpleNamespace

import numpy as np

MODEL = "offline/trigram-hash"
DIMS = 512
STOP = set(
    """a an and are as at be by can do does for from has have how i if in is it me my
of on or the there this to was what when where which who will with you your our we any about
after before into than that then them they these those up""".split()
)


def words(text: str) -> list[str]:
    return [word for word in re.findall(r"[a-z0-9]+", text.lower()) if word not in STOP]


def _vector(text: str) -> np.ndarray:
    vector = np.zeros(DIMS, dtype=np.float32)
    for word in words(text):
        padded = f" {word} "
        for index in range(len(padded) - 2):
            digest = int(hashlib.md5(padded[index : index + 3].encode()).hexdigest(), 16)
            vector[digest % DIMS] += 1.0
    norm = np.linalg.norm(vector)
    return vector / norm if norm else vector


def embed(texts: list[str], log) -> np.ndarray:
    tokens = sum(len(text.split()) for text in texts)
    log(
        SimpleNamespace(model=MODEL, usage=SimpleNamespace(prompt_tokens=tokens, completion_tokens=0)),
        latency_ms=0,
        kind="embed",
    )
    return np.stack([_vector(text) for text in texts])


_SOURCE = re.compile(r"^\[(\d+)\] (.*?)\n(.*?)(?=^\[\d+\] |\Z)", re.S | re.M)


def stems(text: str) -> set[str]:
    return {word[:4] for word in words(text)}


def complete_json(prompt: str) -> tuple[dict, SimpleNamespace]:
    head, question = prompt.split("QUESTION:", 1)
    query = stems(question)
    cited: list[int] = []
    parts: list[str] = []
    for number, header, body in _SOURCE.findall(head):
        overlap = len(query & stems(header + " " + body)) / max(1, len(query))
        if overlap >= 0.6 and len(cited) < 2:
            sentences = [sentence for sentence in re.split(r"(?<=[.!?])\s+", body.strip()) if sentence]
            ranked = sorted(sentences, key=lambda sentence: -len(query & stems(sentence)))[:2]
            cited.append(int(number))
            parts.extend(f"{sentence.rstrip('.')} [{number}]." for sentence in sentences if sentence in ranked)
    if cited:
        out = {"answer": " ".join(parts), "citations": cited, "grounded": True}
    else:
        out = {"answer": "The sources do not say.", "citations": [], "grounded": False}
    resp = SimpleNamespace(
        model=MODEL,
        usage=SimpleNamespace(prompt_tokens=len(prompt.split()), completion_tokens=len(out["answer"].split())),
    )
    return out, resp
