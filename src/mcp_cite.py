"""check_citations as an MCP server, on MCP SDK 2.x (MCPServer).

    python -m src.mcp_cite

The schema comes from src/cite_contracts.py, the same types the function-calling door
validates against. There is no caller field for the model to fill.
"""
from __future__ import annotations

import sys

from mcp.server import MCPServer
from mcp.types import ToolAnnotations

from . import cite_tool
from .cite_contracts import AnswerText, CheckCitations, Citations, SourceCount

mcp = MCPServer(
    "ai-mentor-citations",
    instructions="Check the [n] markers on a handbook answer. Reads only. Never stores the answer.",
)
READS = ToolAnnotations(read_only_hint=True, destructive_hint=False, idempotent_hint=True, open_world_hint=False)


@mcp.tool(annotations=READS, description=CheckCitations.__doc__)
def check_citations(
    answer: AnswerText,
    citations: Citations,
    n_sources: SourceCount,
) -> cite_tool.CitationCheck:
    return cite_tool.check_citations(
        CheckCitations(answer=answer, citations=citations, n_sources=n_sources)
    )


if __name__ == "__main__":
    if "--http" in sys.argv:
        mcp.run("streamable-http", host="127.0.0.1", port=8000)
    else:
        mcp.run()
