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
- **Decision:** Offline threshold 0.30. Live threshold stays 0.25. k stays 5. g3 and g4 were not weakened. The live run on 2026-10-20 passed 5/5: `evals/results/2026-10-20-1734-live-k5.json`. The cafeteria refusal in that run called the model.
- **Cost:** five live answer calls, about $0.005 together, plus an embedding of the corpus well under $0.0001. The two notice photos were separate.

### Entry 4 · Notice route tool (HW2, zidhartha)
- **Task:** Issue #17. Wrap one capstone function as a tool with a contract, both doors, and golden cases in CI.
- **Delegated to:** Cursor agent, with the Lab 5 tool example, `AGENTS.md`, and `docs/tool-contracts.md`.
- **Plan check:** The first plan wrapped a handbook lookup. Rejected after the fact, see below. The second plan wraps `checks.decide()` from Lab 3, which calls no model, so the golden file runs in CI with no key.
- **Came back wrong:** The first version, `lookup_handbook` in pull request #13, returned the best handbook passage for a question. That is the same capability as `search_handbook`, which merged first, and it rewrote the five shared tool files. The brief says no two members wrap the same function.
- **Caught by:** the owners table in `docs/tool-contracts.md`, and five add/add merge conflicts against `main`. Pull request #13 was closed without merging.
- **Decision:** `route_notice` lives in its own files. The only change to the shared tool files is one import and one entry in `TOOLS`. `python -m pytest -q tests`: 67 passed, including Irakli's cases.
- **AGENTS.md change:** two Never lines: no identity field in a tool's arguments, and no tool that deletes or sends without asking first.
- **Cost:** no model call, so $0.

### Entry 5 · Citation check tool (HW2, SanndroP)
- **Task:** Wrap one capstone function that is not `search_handbook` or `route_notice`.
- **Delegated to:** Cursor agent, with the `route_notice` file layout, `AGENTS.md`, and `docs/tool-contracts.md`.
- **Plan check:** A second retrieval tool was rejected before any file was written. `answer.check_citations()` calls no model, so the golden file can run in CI with no key.
- **Came back wrong:** The MCP parameter for `citations` was a bare list. The function-calling schema also had `maxItems: 5` and the field description. The two doors did not match.
- **Caught by:** `tests/test_mcp_cite.py::test_both_doors_describe_the_arguments_identically`. The list is now one `Citations` type used by both doors.
- **Decision:** `check_citations` lives in its own files. The only edit in `src/tools.py` is one import and one `TOOLS` entry. `python -m pytest -q tests` passed, including the other members' cases.
- **Cost:** no model call, so $0.
