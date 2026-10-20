# Confidence policy · photo of a policy page

Applies to `src/extract.py`. An admin photographs a printed policy page; the model returns `{title, text, confidence, problems}`. Code, not the model, decides what happens next (`decide()`).

| Route | When | What the admin sees | Reaches the corpus? |
|---|---|---|---|
| accept | confidence ≥ 0.90 and no problems | extracted text, ready to save | yes, after save |
| confirm | 0.60 ≤ confidence < 0.90, or only soft problems (`glare`, `partly_unreadable`) | extracted text prefilled, must confirm or edit | only after the admin confirms |
| review | confidence < 0.60, empty text, an unreadable reply, or any hard flag: `cut_off`, `blurry`, `handwriting`, `not_a_policy_page` | the problems only; text is **never prefilled** | only if a human types or uploads it |

Why: a policy page with a cut-off number ("24 days" read as "4 days") would become a confident wrong answer for every employee who asks. Retyping one page costs a human two minutes.

Tested in `tests/test_extract.py`: one test per route, and a test that the review route never returns the text.
