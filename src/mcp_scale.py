"""scale_notice as an MCP server, on MCP SDK 2.x (MCPServer).

    python -m src.mcp_scale

The schema comes from src/scale_contracts.py, the same types the function-calling door
validates against. There is no caller field for the model to fill.
"""
from __future__ import annotations

import sys

from mcp.server import MCPServer
from mcp.types import ToolAnnotations

from . import scale_tool
from .scale_contracts import PhotoLabel, Pixel, ScaleNotice

mcp = MCPServer(
    "ai-mentor-scale",
    instructions="Give the size a notice photo will have after downscaling. Reads only. Never stores the photo.",
)
READS = ToolAnnotations(read_only_hint=True, destructive_hint=False, idempotent_hint=True, open_world_hint=False)


@mcp.tool(annotations=READS, description=ScaleNotice.__doc__)
def scale_notice(width: Pixel, height: Pixel, label: PhotoLabel) -> scale_tool.ScaleResult:
    return scale_tool.scale_notice(ScaleNotice(width=width, height=height, label=label))


if __name__ == "__main__":
    if "--http" in sys.argv:
        mcp.run("streamable-http", host="127.0.0.1", port=8000)
    else:
        mcp.run()
