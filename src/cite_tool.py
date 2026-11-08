"""check_citations: the Lab 4 citation check as a tool, behind src/cite_contracts.py.

It runs answer.check_citations() on text the model already wrote. It does not retrieve,
call a model, store anything, or show the answer. It takes no caller.
"""
from __future__ import annotations

from pydantic import BaseModel

from .answer import Reply
from .answer import check_citations as audit
from .cite_contracts import CheckCitations

SHOWN = "The citations match the retrieved sources. You may show this answer."
HELD = "Do not show this answer. Say that it is not in the company documents."


class CitationCheck(BaseModel):
    accepted: bool
    problem: str | None
    next_step: str


def check_citations(args: CheckCitations) -> CitationCheck:
    problem = audit(
        Reply(answer=args.answer, citations=list(args.citations), grounded=True),
        n_sources=args.n_sources,
    )
    if problem is None:
        return CitationCheck(accepted=True, problem=None, next_step=SHOWN)
    return CitationCheck(accepted=False, problem=problem, next_step=HELD)
