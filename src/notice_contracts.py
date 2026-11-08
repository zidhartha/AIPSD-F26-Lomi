"""The tool contract for route_notice. Both doors read this file.

  * src/tools.py registers RouteNotice in TOOLS (the function-calling door)
  * src/mcp_notice.py builds the MCP tool from the same ReadField type

Rules:
  * extra="forbid" on the call and on every field: an argument we did not ask for is an error
  * every string is one short line of notice text: a pattern and at most 120 characters,
    so no newline, slash, or markup can carry instructions into the route
  * confidence is bounded 0 to 1
  * nothing here names who is calling
"""
from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

NoticeText = Annotated[
    str,
    Field(
        min_length=1,
        max_length=120,
        pattern=r"^[A-Za-z0-9][A-Za-z0-9 .,'()?:-]{0,119}$",
        description="One line of text as printed on the notice, at most 120 characters",
    ),
]
Confidence = Annotated[
    float,
    Field(ge=0.0, le=1.0, description="How sure the reader is about this line, 0 to 1"),
]


class ReadField(BaseModel):
    """One line read from the notice. value and evidence are null when the line could not be read."""

    model_config = ConfigDict(extra="forbid")

    value: NoticeText | None
    evidence: NoticeText | None
    confidence: Confidence


class RouteNotice(BaseModel):
    """Route the four lines read from a printed company notice to accepted, confirm, review, or rejected, with the reasons and the next step. Reads only. It never fills a form."""

    model_config = ConfigDict(extra="forbid")

    title: ReadField
    action: ReadField
    timing: ReadField
    contact: ReadField
