"""AI Mentor as an MCP server: the same tool, the second door, usable by any MCP host.

Run it over stdio (what Cursor, Claude Code and VS Code launch):
    python -m src.mcp_server

The schema of the tool comes from the type hints, which come from src/contracts.py, the
same single source of truth the function-calling door reads. The tool is read-only and
takes no identity, so there is nothing for the host to sign in. `mcp` is only needed to
run this file; tests and CI never import it.
"""
from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from . import tools
from .contracts import Query, SearchHandbook, TopK

mcp = FastMCP("ai-mentor")


@mcp.tool(description=SearchHandbook.__doc__)
def search_handbook(query: Query, top_k: TopK = 3) -> tools.SearchResult:
    """Validate through the same contract the function-calling door uses, then run."""
    try:
        return tools.search_handbook(SearchHandbook(query=query, top_k=top_k))
    except tools.ToolFailure as e:
        # Expected failures reach the host as a readable error, never a stack trace.
        raise ValueError(str(e)) from e


if __name__ == "__main__":
    mcp.run()
