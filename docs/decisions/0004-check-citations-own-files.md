# 0004 · check_citations wraps answer.check_citations(), in its own files

**Status:** accepted · 2026-11-08 · Sandro Paikidze

## Context

HW2 asks each member to wrap a different capstone function. `search_handbook` already covers retrieval. `route_notice` already covers `checks.decide()`.

## Decision

The tool is `check_citations`. It takes a proposed answer, the source numbers it claims, and how many sources were retrieved, and returns the verdict from `answer.check_citations()`: accepted or not, the problem, and the next step. It reads only and takes no caller.

The contract is in `src/cite_contracts.py`, the function in `src/cite_tool.py`, and the MCP registration in `src/mcp_cite.py`, on MCP SDK 2.x. The shared `src/tools.py` gets one import and one `TOOLS` entry. `src/contracts.py`, `src/act.py`, `src/mcp_server.py`, and the notice files are not changed.

## Alternatives

- **Wrap retrieval again.** Rejected: that is `search_handbook`.
- **Wrap `decide()` again.** Rejected: that is `route_notice`.
- **Wrap `answer()`, the full grounded call.** Rejected: it calls a model, so the golden cases could not run in CI without a key.
- **Register in `src/mcp_server.py`.** Rejected. That file is Irakli's door for `search_handbook`. A second server keeps this pull request out of his file.

## Consequences

- The model can ask whether an answer's `[n]` markers are real. It cannot store the answer or name the caller.
- The answer is one paragraph of at most 240 characters with a pattern, so a second line of instructions is refused before `check_citations()` runs. Golden case `a1` keeps that in place.
- There is a third MCP server until the team merges them.
