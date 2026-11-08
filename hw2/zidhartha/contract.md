# HW2 · Tool contract · `route_notice` · zidhartha

Code on `main`, from product pull request #18: [`src/notice_contracts.py`](https://github.com/zidhartha/AIPSD-F26-Lomi/blob/main/src/notice_contracts.py) (`RouteNotice`, `ReadField`), [`src/notice_tool.py`](https://github.com/zidhartha/AIPSD-F26-Lomi/blob/main/src/notice_tool.py) (`route_notice`), [`src/tools.py`](https://github.com/zidhartha/AIPSD-F26-Lomi/blob/main/src/tools.py) (`TOOLS` entry), [`src/mcp_notice.py`](https://github.com/zidhartha/AIPSD-F26-Lomi/blob/main/src/mcp_notice.py), [`evals/tools/zidhartha.yaml`](https://github.com/zidhartha/AIPSD-F26-Lomi/blob/main/evals/tools/zidhartha.yaml).

**In one sentence, for the model:** Route the four lines read from a printed company notice to accepted, confirm, review, or rejected, with the reasons and the next step. Reads only. It never fills a form.

It wraps `checks.decide()` from Lab 3 (`docs/confidence-policy.md`). The photo is read by `src/extract.py`; this tool only decides what happens to what was read.

| | |
|---|---|
| **Effect** | reads |
| **Undo** | nothing to undo: it stores nothing |
| **Idempotent?** | yes. The same four lines give the same route |
| **Offered to** | visitors and signed-in callers. It does not write |
| **Identity from** | not needed. `call_tool` may know who is signed in, and does not pass it into the tool |
| **Touches** | nothing outside the call: no file, no model, no network |
| **Must never** | fill a form, or turn a missing or low-confidence line into a value |

**Inputs.** `title`, `action`, `timing`, `contact`, each a `ReadField`. Unknown fields are refused on the call and inside every field.

| Argument | Type | Constraint | Description the model reads |
|---|---|---|---|
| `<field>.value` | string or null | 1 to 120 characters, pattern `^[A-Za-z0-9][A-Za-z0-9 .,'()?:-]{0,119}$` | One line of text as printed on the notice, at most 120 characters |
| `<field>.evidence` | string or null | same as `value` | the same |
| `<field>.confidence` | number | 0 to 1 | How sure the reader is about this line, 0 to 1 |

**Result.** `route` (`accepted`, `confirm`, `review`, or `rejected`), `reasons` (list of sentences), `hard` (fields that stay empty), `next_step` (what the model should do).

**Expected failures.** A valid notice never fails: `review` and `rejected` are results, and `next_step` says what to do.

| When | Message the model reads |
|---|---|
| a line is missing | route `review`, "Action: not found on the image", next step "Send this notice to a person. Leave the hard fields empty; do not guess them." |
| not a company notice | route `rejected`, next step "This is not a company notice. Do not store it or fill a form from it." |
| a confidence above 1 | invalid arguments: title.confidence: Input should be less than or equal to 1 |
| an instruction on a second line | invalid arguments: title.evidence: String should match pattern ... |
| a `user_id` is included | invalid arguments: user_id: Extra inputs are not permitted |

**Tests and golden cases**

| Case | Expect | Where |
|---|---|---|
| a valid call | route `accepted`, `hard` empty | `evals/tools/zidhartha.yaml` n1, `test_a_clean_notice_is_accepted` |
| invalid arguments | refused before `decide()` runs | b1, `test_invalid_arguments_never_reach_the_tool` |
| not offered to this caller | refused, nothing runs | `test_a_tool_that_was_not_offered_does_not_run` |
| identity in the arguments | refused | a2, `test_an_identity_field_is_refused` |
| adversarial: an instruction on a second line of evidence | refused before `decide()` runs | a1, `test_an_instruction_on_a_second_line_is_refused` |

Both doors: `tests/test_mcp_notice.py` checks the MCP schema matches the `TOOLS` schema and both return the same route.

**Why this function.** My first tool, `lookup_handbook` (pull request #13, closed), wrapped the same capability as `search_handbook`. `route_notice` is a different capstone function, and it lives in its own files. Decision record: `docs/decisions/0003-route-notice-own-files.md`.

**Log line.** `logs/tools.jsonl` records the tool, the arguments, ok or the error, a hash of the caller, and latency. It never records the raw caller id.
