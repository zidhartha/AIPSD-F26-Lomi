# 0005 · scale_notice wraps downscale(), in its own files

**Status:** accepted · 2026-11-08 · Elene Kipiani

## Context

HW2 asks each member to wrap a different capstone function. `search_handbook` already covers retrieval. `route_notice` already covers `checks.decide()`. `check_citations` already covers `answer.check_citations()`.

## Decision

The tool is `scale_notice`. It takes the measured width and height of a notice photo, plus one short label, and returns the size from `images.downscale()`: whether the photo was scaled, the width and height to send, and the next step. The longest side stays 1024 and the JPEG quality stays 85. It reads only and takes no caller.

The contract is in `src/scale_contracts.py`, the function in `src/scale_tool.py`, and the MCP registration in `src/mcp_scale.py`, on MCP SDK 2.x. The shared `src/tools.py` gets one import and one `TOOLS` entry. `src/contracts.py`, `src/act.py`, `src/mcp_server.py`, and the other members' tool files are not changed.

## Alternatives

- **Wrap retrieval again.** Rejected: that is `search_handbook`.
- **Wrap `decide()` again.** Rejected: that is `route_notice`.
- **Wrap `check_citations()` again.** Rejected: that is SanndroP's tool.
- **Wrap `extract()`, the photo reader.** Rejected: it calls a model, so the golden cases could not run in CI without a key.
- **Take a file path.** Rejected: the model would choose the path.
- **Register in `src/mcp_server.py`.** Rejected. That file is Irakli's door for `search_handbook`. A separate server keeps this pull request out of his file.

## Consequences

- The model can ask what size to send. It cannot choose the 1024-pixel cap, store the photo, or name the caller.
- The label is one line of at most 80 characters with a pattern, so a second line of instructions is refused before `downscale()` runs. Golden case `a1` keeps that in place.
- There is another MCP server until the team merges them.
