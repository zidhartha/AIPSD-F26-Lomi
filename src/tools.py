"""AI Mentor's tools: the code that acts, behind the contracts in src/contracts.py.

For HW2 there is one tool: `search_handbook`. It reads the company's documents in
data/corpus/ and returns the passages that best match a question. It is the retrieval
step the capstone's grounded answer is built on (docs/spec.md, "Core feature"): the
model only ever sees the chunks this tool returns, never the whole corpus.

Least privilege, decided by what this tool is NOT allowed to do:
  * it only reads .md files under one directory; it writes nothing
  * it takes no identity: the handbook is the same for everyone, so there is no
    student, user or account field anywhere
  * the query is words, not a path, so it cannot be steered to read another file

A failure we expected (no passage matches) raises ToolFailure with a message written
for the model to read and act on. Anything else is a bug and is allowed to crash.
"""
from __future__ import annotations

import hashlib
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from pydantic import BaseModel

from .contracts import Contract, SearchHandbook
from .notice_tool import RouteNotice, route_notice

CORPUS = Path(os.environ.get("AIMENTOR_CORPUS", Path(__file__).resolve().parents[1] / "data" / "corpus"))

# Words so common they say nothing about which document answers a question.
STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being", "do", "does",
    "did", "i", "you", "he", "she", "it", "we", "they", "me", "my", "your", "our",
    "how", "what", "when", "where", "who", "whom", "which", "why", "to", "of", "in",
    "on", "for", "and", "or", "but", "with", "at", "by", "as", "from", "into", "about",
    "this", "that", "these", "those", "there", "here", "then", "than", "so", "if",
    "can", "could", "should", "would", "will", "shall", "may", "might", "must", "have",
    "has", "had", "get", "got", "need", "want", "please", "am", "'s",
}


class ToolFailure(Exception):
    """An expected failure. The message goes back to the model, so make it say what to do next."""


def student_key(student: str) -> str:
    """Hash an identity before it ever reaches a log. Unused by search_handbook (it takes
    no identity), but the frame logs through it so a future write tool cannot log a raw id."""
    return hashlib.sha256(student.encode()).hexdigest()[:12]


# ---------------------------------------------------------------- results

class Passage(BaseModel):
    doc: str          # the source document, e.g. "time-off.md"
    score: int        # how many query terms (with repeats) this passage contains
    text: str         # the passage, so the answer can quote and cite it


class SearchResult(BaseModel):
    query: str
    grounded: bool            # True when at least one passage matched
    count: int                # how many passages are returned
    top_doc: str | None       # the source of the best passage, for a quick citation check
    hits: list[Passage]


# ---------------------------------------------------------------- search_handbook

def _tokens(text: str) -> list[str]:
    return re.findall(r"\w+", text.lower())


def _passages() -> list[tuple[str, str]]:
    """Every paragraph in the corpus, as (document name, text). Reads only; sorted for determinism."""
    out: list[tuple[str, str]] = []
    for path in sorted(CORPUS.glob("*.md")):
        for block in re.split(r"\n\s*\n", path.read_text(encoding="utf-8")):
            block = block.strip()
            if block and not block.startswith("#"):
                out.append((path.name, block))
    return out


def search_handbook(args: SearchHandbook) -> SearchResult:
    terms = {t for t in _tokens(args.query) if t not in STOPWORDS and len(t) > 1}
    scored = []
    for doc, text in _passages():
        counts = _tokens(text)
        score = sum(counts.count(t) for t in terms)
        if score > 0:
            scored.append((score, doc, text))
    # Highest score first; ties break by document name then text, so results never reorder.
    scored.sort(key=lambda s: (-s[0], s[1], s[2]))
    hits = scored[: args.top_k]
    if not hits:
        raise ToolFailure(
            "No handbook passage answers that question. Tell the user the handbook does "
            "not cover it and suggest they rephrase or ask a human; do not invent a rule."
        )
    passages = [Passage(doc=d, score=s, text=t) for s, d, t in hits]
    return SearchResult(
        query=args.query,
        grounded=True,
        count=len(passages),
        top_doc=passages[0].doc,
        hits=passages,
    )


# ---------------------------------------------------------------- the registry

@dataclass(frozen=True)
class Tool:
    name: str
    args: type[Contract]
    run: Callable[..., BaseModel]
    writes: bool = False                  # True: changes the world, needs an identity from us

    def schema(self) -> dict:
        """What the model sees: name, description and JSON Schema, all from the contract."""
        return {"type": "function", "function": {
            "name": self.name,
            "description": (self.args.__doc__ or "").strip(),
            "parameters": self.args.model_json_schema(),
        }}


TOOLS = {t.name: t for t in [
    Tool("search_handbook", SearchHandbook, search_handbook),
    Tool("route_notice", RouteNotice, route_notice),
]}


def tools_for(student: str | None) -> dict[str, Tool]:
    """Least privilege by construction. search_handbook reads only, so it is offered to
    everyone, visitors included. A future write tool would be hidden from a visitor here."""
    return {n: t for n, t in TOOLS.items() if student or not t.writes}
