"""The tool contract for lookup_handbook. Both doors read this file.

  * src/tools.py builds the function-calling schema from HandbookLookup
  * src/mcp_server.py builds the MCP tool from the same type aliases

Rules:
  * extra="forbid": an argument we did not ask for is an error, never ignored
  * the question is a short plain sentence, never a path
  * max_chars is bounded
  * nothing here names who is calling
"""
from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

Question = Annotated[
    str,
    Field(
        min_length=8,
        max_length=120,
        pattern=r"^[A-Za-z0-9][A-Za-z0-9 ?,'-]{7,119}$",
        description="A handbook question in plain words, 8 to 120 characters",
    ),
]
MaxChars = Annotated[
    int,
    Field(ge=80, le=800, description="How much of the passage to return, 80 to 800 characters"),
]


class Contract(BaseModel):
    model_config = ConfigDict(extra="forbid")


class HandbookLookup(Contract):
    """The handbook passage for one question, with the document name. Reads only."""

    question: Question
    max_chars: MaxChars = 400
