# Pattern Journal · [Your name]

*One entry per teaching week, 2 to 3 sentences. Graded inside HW1 (W1-4), HW2 (W5-7), and the Repository Review (W10-14). Honest beats polished.*

Format per entry:
**W# · [Pattern name]** · Where I applied it · What I delegated to AI · How I verified it

---

**W1 · Context as Budget** ·

**W2 · Spec Before Code** · I wrote the first-slice criteria in `docs/spec.md` before `src/ask.py`: a question returns the handbook passage and its filename, or the fixed refusal, and an empty question is an error. I delegated the implementation. The plan wanted a model to paraphrase the passage. That was wrong for this slice, because the spec says the answer is the passage and CI has no API key. I verified it by reading `tests/test_ask.py` first, then running `python -m pytest -q tests` (7 passed) and the three commands in `evals/golden.md`. Next time I want the "no model" line approved before any file is written. It was confirmed after the code existed.

**W3 · Uncertainty-Aware UX** · I used it on the notice photo. A covered action line is a hard flag, so `decide()` sends that card to review and does not prefill the action. I delegated the extraction shape. The first live call was rejected with HTTP 402 because it reserved 65536 tokens; capping `max_tokens` at 1024 is what let it run. I then ran both cards: the clean one came back with evidence on every field, and the degraded one routed to review with the action empty. The hand-written check for a value with no evidence is still `tests/test_checks.py`.

**W4 · Grounded Generation** · I used it on the handbook answer. A cafeteria question has to refuse before any model call. The offline hash scored it at 0.27, so the first test still called the model. I raised only that hash's threshold to 0.30 and left the five golden questions as they were. The committed run is 3/5, and it is offline. I would export the key and run `python -m evals.run_golden` before treating 0.60 as the product's pass rate.
