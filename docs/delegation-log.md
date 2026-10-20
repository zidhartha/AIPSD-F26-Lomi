# Delegation log · AI Mentor

### Entry 1 · Handbook lookup, no model
- **Task:** AC1, AC2, AC3 in docs/spec.md. First slice.
- **Delegated to:** Cursor agent, with docs/spec.md, AGENTS.md, and the Lab 2 rule that the first slice is the smallest end-to-end piece.
- **Plan check:** The plan was to call a model to paraphrase the passage. Rejected before any product code. Lab 2's own example leaves the model for the next slice, and CI has no API key.
- **Came back wrong:** The first draft called the optional `complete` hook on a successful lookup. That would fail the test that forbids a model call.
- **Caught by:** reading `tests/test_ask.py` before running it. The hook call was removed first.
- **Decision:** The slice returns the passage itself. The model hook is not called. `python -m pytest -q tests` then passed, 7 tests.
- **AGENTS.md change:** `run` is now `python -m src.ask "How do I request time off?"`.
- **Cost:** one failed test run, then a green run. No model calls, so $0.
