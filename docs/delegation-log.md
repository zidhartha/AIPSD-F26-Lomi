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

### Entry 2 · Notice photo
- **Task:** Lab 3. A photographed company notice returns value, evidence, and confidence, then `decide()` routes it.
- **Delegated to:** Cursor agent, with `docs/multimodal-spec.md`, `AGENTS.md`, and the Lab 3 poster-extraction example.
- **Plan check:** The plan was to trust the model's confidence and store the fields. Rejected. The policy says a missing line is a hard flag and is shown empty.
- **Came back wrong:** The first live call returned HTTP 402. The request reserved 65536 output tokens, more than the credit balance could cover. Nothing was generated. `max_tokens=1024` in `src/llm.py` is what made the next call fit.
- **Caught by:** the 402 from `python -m src.extract tests/images/clean.jpg`, then the rerun. `tests/test_checks.py` already had the degraded case as a hand-written extraction.
- **Live check, 2026-10-20:** `tests/images/clean.jpg` returned title, action, timing, and contact, each with evidence. `tests/images/degraded.jpg` routed to `review`, hard field `action`, reason "Action: not found on the image".
- **Cost:** two calls in `logs/usage.jsonl`: $0.002447 and $0.002702. No credits were purchased.

### Entry 3 · Grounded answer
- **Task:** Lab 4. Retrieve handbook chunks, cite them, or refuse before the model. Golden set of five.
- **Delegated to:** Cursor agent, with `docs/retrieval-spec.md`, `AGENTS.md`, and the Lab 4 campuspulse-rag example.
- **Plan check:** The plan used the example's 0.25 threshold for every embedder. That was wrong for the offline hash.
- **Came back wrong:** "What is the guest cafeteria menu on Friday?" scored 0.27 and the test reached the model. The first golden run was 3/5.
- **Caught by:** `tests/test_answer.py` failing on the no-model refusal, then `python -m evals.run_golden` at k=5 and k=1.
- **Decision:** Offline threshold 0.30. k stays 5. g3 and g4 were not weakened. The committed result stays 3/5 until a live run. `docs/decisions/0002-k-and-threshold.md`.
- **Cost:** $0. The usage log is the offline stand-in.
