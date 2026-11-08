"""Answer from retrieved handbook chunks, cite them, or refuse before the model."""
from __future__ import annotations

import json
import os
import re
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from pydantic import BaseModel, ConfigDict

from .index import Index, load
from .llm import complete_json, embed_model_name
from .retrieve import Hit, hybrid

DEFAULT_MIN_SCORE = {"openai/text-embedding-3-small": 0.25, "offline/trigram-hash": 0.30}
ANSWER_LOG = Path(os.environ.get("MENTOR_ANSWER_LOG", "logs/answers.jsonl"))
REFUSAL = "That is not in the company documents."


def min_score() -> float:
    override = os.environ.get("MENTOR_MIN_SCORE")
    if override:
        return float(override)
    return DEFAULT_MIN_SCORE.get(embed_model_name(), 0.25)


class Reply(BaseModel):
    model_config = ConfigDict(extra="forbid")
    answer: str
    citations: list[int]
    grounded: bool


PROMPT = """Answer the QUESTION using only the SOURCES.
End every sentence with the number of the source it came from, like [2].
If the sources do not answer the question, set grounded to false
and say what is missing. Never use outside knowledge.

SOURCES:
{sources}

QUESTION: {question}"""


@dataclass
class Answer:
    status: str
    text: str
    sources: list[dict] = field(default_factory=list)
    reason: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


def format_sources(hits: list[Hit]) -> str:
    return "\n\n".join(
        f"[{number}] {hit.chunk.title} · {hit.chunk.section}\n{hit.chunk.text}"
        for number, hit in enumerate(hits, start=1)
    )


def check_citations(reply: Reply, n_sources: int) -> str | None:
    markers = {int(match) for match in re.findall(r"\[(\d+)\]", reply.answer)}
    if not reply.citations or not markers:
        return "answer has no citations"
    unknown = (markers | set(reply.citations)) - set(range(1, n_sources + 1))
    if unknown:
        return f"cites sources that were never retrieved: {sorted(unknown)}"
    if markers != set(reply.citations):
        return "citation list and [n] markers disagree"
    sentences = [sentence for sentence in re.split(r"(?<=[.!?])\s+(?=[A-Z])", reply.answer.strip()) if sentence]
    uncited = [sentence for sentence in sentences if not re.search(r"\[\d+\]", sentence)]
    if uncited:
        return f"uncited sentence: {uncited[0][:60]!r}"
    return None


def refuse(reason: str) -> Answer:
    return Answer("refused", REFUSAL, reason=reason)


def cite(hits: list[Hit], citations: list[int]) -> list[dict]:
    return [
        {
            "n": number,
            "chunk_id": hits[number - 1].chunk.id,
            "doc_id": hits[number - 1].chunk.doc_id,
            "title": hits[number - 1].chunk.title,
            "section": hits[number - 1].chunk.section,
        }
        for number in sorted(set(citations))
        if 1 <= number <= len(hits)
    ]


def answer(index: Index, question: str, k: int = 5, retrieve=hybrid, llm=complete_json, check: bool = True) -> Answer:
    hits = retrieve(index, question, k=k)

    def done(result: Answer) -> Answer:
        return _log(question, k, hits, result)

    best = max((hit.score for hit in hits), default=0.0)
    if best < min_score():
        return done(refuse(f"best match {best:.2f} below threshold"))
    raw = llm(PROMPT.format(sources=format_sources(hits), question=question), schema=Reply.model_json_schema())
    reply = Reply.model_validate(raw)
    if not reply.grounded:
        return done(refuse("model: sources do not answer it"))
    problem = check_citations(reply, n_sources=len(hits)) if check else None
    if problem:
        return done(refuse(problem))
    return done(Answer("answered", reply.answer, cite(hits, reply.citations)))


def _log(question: str, k: int, hits: list[Hit], result: Answer) -> Answer:
    line = {
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "question": question,
        "status": result.status,
        "reason": result.reason,
        "k": k,
        "best_score": round(max((hit.score for hit in hits), default=0.0), 3),
        "retrieved": [hit.chunk.id for hit in hits],
        "cited": [source["chunk_id"] for source in result.sources],
    }
    ANSWER_LOG.parent.mkdir(parents=True, exist_ok=True)
    with ANSWER_LOG.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(line) + "\n")
    return result


if __name__ == "__main__":
    print(json.dumps(answer(load(), " ".join(sys.argv[1:])).to_dict(), indent=2))
