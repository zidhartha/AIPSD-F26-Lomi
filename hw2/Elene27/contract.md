# HW2 · Tool contract · `scale_notice` · Elene27

Code on branch `slice-hw2-Elene27` (commit `ea8de54`): [`src/scale_contracts.py`](https://github.com/zidhartha/AIPSD-F26-Lomi/blob/ea8de54/src/scale_contracts.py) (`ScaleNotice`, `Pixel`, `PhotoLabel`), [`src/scale_tool.py`](https://github.com/zidhartha/AIPSD-F26-Lomi/blob/ea8de54/src/scale_tool.py) (`scale_notice`), [`src/tools.py`](https://github.com/zidhartha/AIPSD-F26-Lomi/blob/ea8de54/src/tools.py) (`TOOLS` entry), [`src/mcp_scale.py`](https://github.com/zidhartha/AIPSD-F26-Lomi/blob/ea8de54/src/mcp_scale.py), [`evals/tools/Elene27.yaml`](https://github.com/zidhartha/AIPSD-F26-Lomi/blob/ea8de54/evals/tools/Elene27.yaml).

**In one sentence, for the model:** Give the size a notice photo will have after it is downscaled to 1024 pixels on the longest side. Reads only. It never sends the photo or stores it.

It wraps `images.downscale()` from Lab 3 (`docs/multimodal-spec.md`). The photo is measured first. This tool only says what size to send. The 1024-pixel cap and the JPEG quality of 85 stay inside the tool.

| | |
|---|---|
| **Effect** | reads |
| **Undo** | nothing to undo: it stores nothing |
| **Idempotent?** | yes. The same width and height give the same size |
| **Offered to** | visitors and signed-in callers. It does not write |
| **Identity from** | not needed. `call_tool` may know who is signed in, and does not pass it into the tool |
| **Touches** | nothing outside the call: no file, no model, no network |
| **Must never** | let the model choose the 1024-pixel cap, take a file path, or treat a second line of instructions as a caption |

**Inputs.** `width`, `height`, `label`. Unknown fields are refused.

| Argument | Type | Constraint | Description the model reads |
|---|---|---|---|
| `width` | integer | 1 to 4096 | One side of the photo in pixels, from 1 to 4096 |
| `height` | integer | 1 to 4096 | the same |
| `label` | string | 1 to 80 characters, pattern `^[A-Za-z0-9][A-Za-z0-9 .,'()?:-]{0,79}$` | One short line naming what the photo shows. No line breaks |

**Result.** `scaled` (bool), `width` and `height` (the size to send), `next_step` (what the model should do).

**Expected failures.** A photo that is already small enough is a result, not an error: `scaled` is false and `next_step` says it may be sent.

| When | Message the model reads |
|---|---|
| the longest side is above 1024 | `scaled` true, next step "Resize the photo so the longest side is 1024 pixels before you send it. Do not send the original." |
| the photo is already small enough | `scaled` false, next step "The photo is already within 1024 pixels on the longest side. You may send it." |
| `width` is 0 | invalid arguments: width: Input should be greater than or equal to 1 |
| an instruction on a second line | invalid arguments: label: String should match pattern ... |
| a `user_id` is included | invalid arguments: user_id: Extra inputs are not permitted |

**Tests and golden cases**

| Case | Expect | Where |
|---|---|---|
| a valid call | `scaled` true, width 1024, height 512 | `evals/tools/Elene27.yaml` n1, `test_a_wide_photo_is_scaled_to_1024` |
| invalid arguments | refused before `downscale()` runs | b1, `test_invalid_arguments_never_reach_the_tool` |
| not offered to this caller | refused, nothing runs | `test_a_tool_that_was_not_offered_does_not_run` |
| identity in the arguments | refused | a2, `test_an_identity_field_is_refused` |
| adversarial: an instruction on a second line | refused before `downscale()` runs | a1, `test_an_instruction_on_a_second_line_is_refused` |

Both doors: `tests/test_mcp_scale.py` checks the MCP schema matches the `TOOLS` schema and both return the same size.

**Why this function.** `search_handbook` already retrieves passages. `route_notice` already routes a notice. `check_citations` already checks `[n]` markers. `scale_notice` is the Lab 3 downscale, and it calls no model, so CI needs no key. It lives in its own files. Decision record: `docs/decisions/0005-scale-notice-own-files.md`.

**Log line.** `logs/tools.jsonl` records the tool, the arguments, ok or the error, a hash of the caller, and latency. It never records the raw caller id. `test_one_log_line_per_call_and_no_raw_caller` checks that `s123` is not in the line.
