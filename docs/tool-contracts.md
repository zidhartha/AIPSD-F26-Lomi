# Tool contracts · Lomi

*The AI Mentor tools, their contracts, and who owns each. Each HW2 member wraps a different capstone function (HW2 brief: "Each member wraps a different function").*

The contract for every tool lives in `src/contracts.py`; the function and registry entry in `src/tools.py`; the MCP registration in `src/mcp_server.py`; and the golden set in `evals/tools/<username>.yaml`, run in CI by `tests/test_tool_golden.py`.

## Owners

| Tool | Function | Effect | Owner | Golden set |
|---|---|---|---|---|
| `search_handbook` | retrieve the passages that best match a question, with their source | reads | Irakligig | `evals/tools/Irakligig.yaml` |
| `route_notice` | route the lines read from a notice photo with `checks.decide()` (Lab 3): accepted, confirm, review, or rejected. Contract in `src/notice_contracts.py`, function in `src/notice_tool.py`, MCP in `src/mcp_notice.py` | reads | zidhartha | `evals/tools/zidhartha.yaml` |
| _(next member)_ | _(a different capstone function)_ | | | |

A tool that deletes, pays, or sends to other people needs the instructor's agreement by email before it is built.
