"""lookup_handbook: one read of the company handbook, behind the contract in src/contracts.py.

The question is never used as a file path. The tool reads only the markdown already in
data/corpus, and it returns a document id, not a path. It does not take a caller.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from pydantic import BaseModel

from .ask import tokens
from .contracts import Contract, HandbookLookup

CORPUS = Path(__file__).resolve().parents[1] / "data" / "corpus"
THRESHOLD = 0.5
REFUSAL = (
    "That is not in the company documents. "
    "Ask about a rule that is written in the handbook."
)


class ToolFailure(Exception):
    """An expected failure. The message goes back to the model and says what to do next."""


class Passage(BaseModel):
    doc: str
    title: str
    passage: str


def load_docs(root: Path = CORPUS) -> list[dict]:
    docs = []
    for file in sorted(root.rglob("*.md")):
        text = file.read_text(encoding="utf-8")
        title = next(
            (line.lstrip("#").strip() for line in text.splitlines() if line.startswith("#")),
            file.stem,
        )
        docs.append({"id": file.relative_to(root).with_suffix("").as_posix(), "title": title, "text": text})
    return docs


def rank(question: str, docs: list[dict] | None = None) -> list[dict]:
    query = tokens(question)
    if not query:
        return []
    found = []
    for doc in load_docs() if docs is None else docs:
        words = set(tokens(doc["text"]))
        score = len(set(query) & words) / len(set(query))
        found.append({**doc, "score": score})
    found.sort(key=lambda hit: (-hit["score"], hit["id"]))
    return found


def lookup_handbook(args: HandbookLookup) -> Passage:
    hits = rank(args.question)
    if not hits or hits[0]["score"] < THRESHOLD:
        raise ToolFailure(REFUSAL)
    top = hits[0]
    return Passage(doc=top["id"], title=top["title"], passage=top["text"][: args.max_chars])


@dataclass(frozen=True)
class Tool:
    name: str
    args: type[Contract]
    run: Callable[..., BaseModel]
    writes: bool = False

    def schema(self) -> dict:
        return {"type": "function", "function": {
            "name": self.name,
            "description": (self.args.__doc__ or "").strip(),
            "parameters": self.args.model_json_schema(),
        }}


TOOLS = {t.name: t for t in [
    Tool("lookup_handbook", HandbookLookup, lookup_handbook),
]}


def tools_for(caller: str | None) -> dict[str, Tool]:
    """A caller who is not signed in is offered read tools only. This tool never writes."""
    return {name: tool for name, tool in TOOLS.items() if caller or not tool.writes}
