# HW2 · Tool contract · `check_citations` · SanndroP

Code in product pull request #21 (commit `9a121ee`): [`src/cite_contracts.py`](https://github.com/zidhartha/AIPSD-F26-Lomi/blob/9a121ee94f94e19cf82966cd563bd79ea96e6858/src/cite_contracts.py) (`CheckCitations`, `AnswerText`, `Citations`), [`src/cite_tool.py`](https://github.com/zidhartha/AIPSD-F26-Lomi/blob/9a121ee94f94e19cf82966cd563bd79ea96e6858/src/cite_tool.py) (`check_citations`), [`src/tools.py`](https://github.com/zidhartha/AIPSD-F26-Lomi/blob/9a121ee94f94e19cf82966cd563bd79ea96e6858/src/tools.py) (`TOOLS` entry), [`src/mcp_cite.py`](https://github.com/zidhartha/AIPSD-F26-Lomi/blob/9a121ee94f94e19cf82966cd563bd79ea96e6858/src/mcp_cite.py), [`evals/tools/SanndroP.yaml`](https://github.com/zidhartha/AIPSD-F26-Lomi/blob/9a121ee94f94e19cf82966cd563bd79ea96e6858/evals/tools/SanndroP.yaml).

**In one sentence, for the model:** Check that every `[n]` in a proposed handbook answer points at a source that was retrieved, and that every sentence has one. Reads only. It never stores the answer.

It wraps `answer.check_citations()` from Lab 4 (`docs/retrieval-spec.md`). Retrieval is `search_handbook`. This tool only decides whether the answer that came back may be shown.

| | |
|---|---|
| **Effect** | reads |
| **Undo** | nothing to undo: it stores nothing |
| **Idempotent?** | yes. The same answer and the same source count give the same verdict |
| **Offered to** | visitors and signed-in callers. It does not write |
| **Identity from** | not needed. `call_tool` may know who is signed in, and does not pass it into the tool |
| **Touches** | nothing outside the call: no file, no model, no network |
| **Must never** | show an answer whose markers do not match the retrieved sources, or treat a second line of instructions as answer text |

**Inputs.** `answer`, `citations`, `n_sources`. Unknown fields are refused.

| Argument | Type | Constraint | Description the model reads |
|---|---|---|---|
| `answer` | string | 1 to 240 characters, pattern `^[A-Za-z0-9][A-Za-z0-9 .,'()?:;\-\[\]]{0,239}$` | One paragraph of the proposed answer, with `[n]` markers. No line breaks |
| `citations` | list of integers | each item 1 to 5, at most 5 items | The source numbers the answer claims to use |
| `n_sources` | integer | 1 to 5 | How many sources were retrieved for this answer |

**Result.** `accepted` (bool), `problem` (sentence or null), `next_step` (what the model should do).

**Expected failures.** A citation problem is a result, not an error: `accepted` is false and `next_step` says not to show the answer.

| When | Message the model reads |
|---|---|
| no `[n]` markers | `accepted` false, problem "answer has no citations", next step "Do not show this answer. Say that it is not in the company documents." |
| a marker past the retrieved sources | `accepted` false, problem "cites sources that were never retrieved: [4]" |
| `n_sources` is 0 | invalid arguments: n_sources: Input should be greater than or equal to 1 |
| an instruction on a second line | invalid arguments: answer: String should match pattern ... |
| a `user_id` is included | invalid arguments: user_id: Extra inputs are not permitted |

**Tests and golden cases**

| Case | Expect | Where |
|---|---|---|
| a valid call | `accepted` true, `problem` null | `evals/tools/SanndroP.yaml` n1, `test_a_cited_sentence_is_accepted` |
| invalid arguments | refused before `check_citations()` runs | b1, `test_invalid_arguments_never_reach_the_tool` |
| not offered to this caller | refused, nothing runs | `test_a_tool_that_was_not_offered_does_not_run` |
| identity in the arguments | refused | a2, `test_an_identity_field_is_refused` |
| adversarial: an instruction on a second line | refused before the check runs | a1, `test_an_instruction_on_a_second_line_is_refused` |

Both doors: `tests/test_mcp_cite.py` checks the MCP schema matches the `TOOLS` schema and both return the same verdict.

**Why this function.** `search_handbook` already retrieves passages. `route_notice` already routes a notice. `check_citations` is the Lab 4 check that an answer's `[n]` markers were actually retrieved, and it calls no model, so CI needs no key. It lives in its own files. Decision record: `docs/decisions/0004-check-citations-own-files.md` (in pull request #21).

**Log line.** `logs/tools.jsonl` records the tool, the arguments, ok or the error, a hash of the caller, and latency. It never records the raw caller id. `test_one_log_line_per_call_and_no_raw_caller` checks that `s123` is not in the line.
