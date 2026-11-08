"""route_notice as an MCP server, on MCP SDK 2.x (MCPServer).

    python -m src.mcp_notice

The schema comes from ReadField in src/notice_contracts.py, the same type the
function-calling door validates against. There is no caller field for the model to fill.
"""
from __future__ import annotations

import sys

from mcp.server import MCPServer
from mcp.types import ToolAnnotations

from . import notice_tool
from .notice_contracts import ReadField, RouteNotice

mcp = MCPServer(
    "ai-mentor-notice",
    instructions="Route the lines read from a company notice photo. Reads only. Never fills a form.",
)
READS = ToolAnnotations(read_only_hint=True, destructive_hint=False, idempotent_hint=True, open_world_hint=False)


@mcp.tool(annotations=READS, description=RouteNotice.__doc__)
def route_notice(title: ReadField, action: ReadField, timing: ReadField, contact: ReadField) -> notice_tool.NoticeRoute:
    return notice_tool.route_notice(RouteNotice(title=title, action=action, timing=timing, contact=contact))


if __name__ == "__main__":
    if "--http" in sys.argv:
        mcp.run("streamable-http", host="127.0.0.1", port=8000)
    else:
        mcp.run()
