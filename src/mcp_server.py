"""AI Mentor as an MCP server: the same handbook lookup, with the same contract.

    python -m src.mcp_server

The schema comes from the type aliases in src/contracts.py. The question is the only
argument. There is no caller field for the model to fill.
"""
from __future__ import annotations

import sys

from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from mcp.types import ToolAnnotations

from . import tools
from .contracts import HandbookLookup, MaxChars, Question

mcp = MCPServer(
    "ai-mentor",
    instructions="Look up one rule in the company handbook. Reads only. Never invent a rule.",
)
READS = ToolAnnotations(read_only_hint=True, destructive_hint=False, open_world_hint=False)


def _run(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except tools.ToolFailure as err:
        raise ToolError(str(err)) from err


@mcp.tool(annotations=READS, description=HandbookLookup.__doc__)
def lookup_handbook(question: Question, max_chars: MaxChars = 400) -> tools.Passage:
    return _run(tools.lookup_handbook, HandbookLookup(question=question, max_chars=max_chars))


if __name__ == "__main__":
    if "--http" in sys.argv:
        mcp.run("streamable-http", host="127.0.0.1", port=8000)
    else:
        mcp.run()
