"""route_notice: the Lab 3 notice route as a tool, behind the contract in src/notice_contracts.py.

It runs checks.decide() on lines that were already read from a photo. It does not read
the photo, call a model, store anything, or fill a form. It takes no caller.
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

from .checks import decide
from .extract import Extraction
from .notice_contracts import RouteNotice

NEXT_STEP = {
    "accepted": "Show the values to the employee. Nothing is saved until they do.",
    "confirm": "Ask the employee to confirm the flagged lines before anything is saved.",
    "review": "Send this notice to a person. Leave the hard fields empty; do not guess them.",
    "rejected": "This is not a company notice. Do not store it or fill a form from it.",
}


class NoticeRoute(BaseModel):
    route: Literal["accepted", "confirm", "review", "rejected"]
    reasons: list[str]
    hard: list[str]
    next_step: str


def route_notice(args: RouteNotice) -> NoticeRoute:
    decision = decide(Extraction.model_validate(args.model_dump()))
    return NoticeRoute(
        route=decision.route,
        reasons=decision.reasons(),
        hard=sorted(decision.hard),
        next_step=NEXT_STEP[decision.route],
    )
