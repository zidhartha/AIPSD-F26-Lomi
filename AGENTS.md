# AGENTS.md · AI Mentor
A mentor that answers a new employee's questions from their company's own documents, or refuses. Spec: docs/spec.md

## Commands
install:  pip install -r requirements.txt
run:      python -m src.ask "How do I request time off?"
notice:   python -m src.extract tests/images/clean.jpg
answer:   python -m src.index
          python -m src.answer "How do I request time off?"
test:     python -m pytest -q tests

## Conventions
- Model: env `OPENROUTER_API_KEY` and `MODEL`. Default `MODEL` is `google/gemini-3.8-flash`. Embeddings: `EMBED_MODEL`, default `openai/text-embedding-3-small`. Never hard-code a key.
- Every model call goes through `src/llm.py` and appends one line to `logs/usage.jsonl`: model, tokens in, tokens out, cost, latency.
- Downscale a notice photo to 1024 px on the longest side before sending it. Evidence is nullable. Never guess a field.
- Never prefill a low-confidence or missing value into a form. `decide()` leaves hard fields empty.
- Every grounded answer cites a retrieved source as `[n]`, or refuses. Refuse before the model when the best score is under the threshold.
- Never weaken or delete a golden question to make it pass.
- Dates are ISO. Quote money and durations as the source document writes them.
- Success shape: `{answer, citations, grounded}`. Refusal text is `That is not in the company documents.` Request errors are `{error, detail}`.

## Always
- Run the test command before saying you are done, and paste the result

## Ask first
- Adding a dependency
- Changing a public response shape
- Editing CI configuration

## Never
- Read or write .env, or print a key
- Delete, skip, or weaken a test to make it pass
- Invent a company rule that was not in the retrieved documents

<!-- Keep it under about 40 lines. It is loaded into every agent session: every line costs budget every time. -->
