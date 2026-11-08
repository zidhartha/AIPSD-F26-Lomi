"""Tool contracts for AI Mentor: what each tool accepts, as types the code can check.

This file is the single source of truth for tool inputs. Both doors read it:
  * src/tools.py builds the function-calling schema the model sees (from the Args model)
  * src/mcp_server.py builds the MCP tool from the same type aliases
If the two doors ever describe a tool differently, that is a bug: they share these types.

Rules that hold for every contract (the HW2 locks):
  * extra="forbid": an argument we did not ask for is an error, never ignored
  * every string that reaches a lookup has a pattern (or a fixed set of values)
  * every number has bounds
  * nothing here names WHO is calling, or a document path. The query is words, not a file.
"""
from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

# A plain-language question. Letters, digits, spaces and light punctuation only:
# no slash, backslash, newline or markup, so a file path or an injected block of
# instructions cannot be smuggled in through the query string. \w is Unicode-aware,
# so a question in Georgian or another language still matches (spec: answer in the
# language of the question).
Query = Annotated[
    str,
    Field(
        pattern=r"^[\w ?.,'!()\-:]{3,200}$",
        description="A question in plain words, 3 to 200 characters. No slashes or markup.",
    ),
]

# How many passages to return. Bounded so a huge value cannot be used to pull the
# whole corpus back through one call.
TopK = Annotated[int, Field(ge=1, le=5, description="How many passages to return, 1 to 5")]


class Contract(BaseModel):
    model_config = ConfigDict(extra="forbid")


class SearchHandbook(Contract):
    """Search the company handbook and return the passages that best match a question, each with its source document, so an answer can be grounded. Reads only."""

    query: Query
    top_k: TopK = 3
