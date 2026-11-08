"""The tool contract for check_citations. Both doors read this file.

  * src/tools.py registers CheckCitations in TOOLS (the function-calling door)
  * src/mcp_cite.py builds the MCP tool from the same AnswerText and SourceCount types

Rules:
  * extra="forbid": an argument we did not ask for is an error
  * the answer is one short paragraph: a pattern and at most 240 characters,
    so a newline or a 400-character instruction cannot ride in with the [n] markers
  * every source number is an integer from 1 to 5, and so is n_sources
  * nothing here names who is calling
"""
from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

AnswerText = Annotated[
    str,
    Field(
        min_length=1,
        max_length=240,
        pattern=r"^[A-Za-z0-9][A-Za-z0-9 .,'()?:;\-\[\]]{0,239}$",
        description="One paragraph of the proposed answer, at most 240 characters, with [n] markers. No line breaks.",
    ),
]
SourceCount = Annotated[
    int,
    Field(ge=1, le=5, description="How many sources were retrieved for this answer, from 1 to 5"),
]
CitationN = Annotated[
    int,
    Field(ge=1, le=5, description="A source number that was retrieved, from 1 to 5"),
]
Citations = Annotated[
    list[CitationN],
    Field(max_length=5, description="The source numbers the answer claims to use, at most five"),
]


class CheckCitations(BaseModel):
    """Check that every [n] in a proposed handbook answer points at a source that was retrieved, and that every sentence has one. Reads only. It never stores the answer."""

    model_config = ConfigDict(extra="forbid")

    answer: AnswerText
    citations: Citations
    n_sources: SourceCount
