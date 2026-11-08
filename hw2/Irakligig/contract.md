# HW2 · Tool contract · `search_handbook` · Irakligig

*Code on `main`: `src/contracts.py` (`SearchHandbook`, `Query`, `TopK`), `src/tools.py` (`search_handbook`, registry entry), `src/mcp_server.py` (`search_handbook`), `evals/tools/Irakligig.yaml`. Product pull request: `slice-hw2-Irakligig` (prepared locally; not pushed).*

**In one sentence, for the model:** Search the company handbook and return the passages that best match a question, each with its source document, so an answer can be grounded. Reads only.

This is the retrieval step the AI Mentor capstone is built on (`docs/spec.md`, "Core feature"): the model only ever sees the chunks this tool returns, never the whole corpus. Wrapping it as a tool is what lets a model *ask for evidence* before it answers, and refuse when there is none.

| | |
|---|---|
| **Effect** | reads. It returns passages; it changes nothing |
| **Undo** | nothing to undo: no state changes |
| **Idempotent?** | yes — same corpus, same query, same result |
| **Offered to** | everyone, visitors included. It needs no identity, so offering it widely costs nothing |
| **Identity from** | not needed — the handbook is the same for every employee |
| **Touches** | `data/corpus/*.md`, read only. No network, no model, no key |
| **Must never** | read a file outside `data/corpus/`, or build a file path from the query string |

**Inputs**

| Argument | Type | Constraint | Description the model reads |
|---|---|---|---|
| `query` | string | pattern `^[\w ?.,'!()\-:]{3,200}$`; unknown fields refused | A question in plain words, 3 to 200 characters. No slashes or markup |
| `top_k` | integer | `1 ≤ top_k ≤ 5`, default 3 | How many passages to return, 1 to 5 |

The pattern allows letters (Unicode, so other languages work), digits, spaces and light punctuation only. It refuses a slash, a backslash, a newline or markup, so a file path or a block of injected instructions cannot ride in on the query string. `top_k` is bounded so one call cannot pull the whole corpus back.

**Result.** `query`, `grounded` (bool), `count` (int), `top_doc` (the source of the best passage, for a quick citation check), and `hits`: a list of `{doc, score, text}`.

**Expected failures**

| When | Message the model reads |
|---|---|
| no passage matches | No handbook passage answers that question. Tell the user the handbook does not cover it and suggest they rephrase or ask a human; do not invent a rule. |

The message leaks no path, no file name and no stack trace. It tells the model the one safe next step, which is the capstone's refusal rule (`docs/spec.md`, acceptance criterion 2).

**Why retrieval, and why words not a path.** The first shape I considered was a `read_document(path)` tool. It worked, but the model chooses the path, and nothing stops it choosing `../../.env`. `search_handbook` takes a *question*, never a location: the code decides which files exist and opens only `.md` files under one directory. Even a fully hijacked model can do only one small, read-only thing — get back handbook passages. Decision record: `docs/decisions/0001-search-handbook-reads-only.md`.

**The seven locks.** (1) contract in code: pattern on `query`, bounds on `top_k`, `extra="forbid"`. (2) no identity, account or path field. (3) offered to everyone because it only reads. (4) nothing destructive exists. (5) the one failure message says what to do next and leaks nothing. (6) `top_k` bounds one call; `MAX_ROUNDS` bounds the loop. (7) one log line per call in `logs/tools.jsonl`; the five golden cases test the bad calls, not just the good ones.

**Both doors, one contract.** `src/tools.py` (function calling) and `src/mcp_server.py` (MCP) both build from `SearchHandbook` in `src/contracts.py`. `tests/test_tools.py::test_schema_comes_from_the_contract_and_forbids_extra_fields` fails if the schema ever loses the pattern, the bounds, or `additionalProperties: false`.

**Where the five cases live.** `evals/tools/Irakligig.yaml`, run in CI by `tests/test_tool_golden.py`. Results and run links: `evidence.md`.

**Log line.** Timestamp, tool, arguments, ok or the error, latency. No caller is recorded: the tool never receives one.
