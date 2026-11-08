# 0003 · route_notice wraps decide(), in its own files

**Status:** accepted · 2026-11-08 · Davit Jincharadze

## Context

HW2 asks each member to wrap a different capstone function. `search_handbook` already covers handbook retrieval. My first tool, `lookup_handbook`, returned the best passage for a question, which is the same capability.

## Decision

The tool is `route_notice`. It takes the four lines a model read from a notice photo, each with value, evidence, and confidence, and returns the route from `checks.decide()`: accepted, confirm, review, or rejected, with the reasons, the hard fields, and the next step. It reads only and takes no caller.

The contract is in `src/notice_contracts.py`, the function in `src/notice_tool.py`, and the MCP registration in `src/mcp_notice.py`, on MCP SDK 2.x. The shared `src/tools.py` gets one import and one `TOOLS` entry. `src/contracts.py`, `src/act.py`, and `src/mcp_server.py` are not changed.

## Alternatives

- **Keep `lookup_handbook`.** Rejected: same function as `search_handbook`, and it conflicts with the five shared tool files.
- **Wrap `extract()`, the photo reader.** Rejected: it calls a model, so its golden cases could not run in CI without a key.
- **Register in `src/mcp_server.py`.** Rejected for this pull request. That file imports `FastMCP`, which MCP SDK 2.x no longer has, so registering there would mean changing another member's file.

## Consequences

- The model can ask for a route but never for a write. A low-confidence or missing line still cannot be prefilled: `decide()` names it, and the reply says to leave it empty.
- Each string is one short line with a pattern, so instructions on a second line are refused before `decide()` runs. Golden case `a1` keeps that in place.
- There are two MCP servers until the team merges them.
