# Pattern Journal · [Your name]

*One entry per teaching week, 2 to 3 sentences. Graded inside HW1 (W1-4), HW2 (W5-7), and the Repository Review (W10-14). Honest beats polished.*

Format per entry:
**W# · [Pattern name]** · Where I applied it · What I delegated to AI · How I verified it

---

**W1 · Context as Budget** ·

**W2 · Spec Before Code** · I wrote the first-slice criteria in `docs/spec.md` before `src/ask.py`: a question returns the handbook passage and its filename, or the fixed refusal, and an empty question is an error. I delegated the implementation. The plan wanted a model to paraphrase the passage. That was wrong for this slice, because the spec says the answer is the passage and CI has no API key. I verified it by reading `tests/test_ask.py` first, then running `python -m pytest -q tests` (7 passed) and the three commands in `evals/golden.md`. Next time I want the "no model" line approved before any file is written. It was confirmed after the code existed.

**W3 · Uncertainty-Aware UX** ·

**W4 · Grounded Generation** ·
