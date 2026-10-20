# AGENTS.md · AI Mentor
A mentor that answers a new employee's questions from their company's own documents, or refuses. Spec: docs/spec.md

## Commands
install:  pip install -r requirements.txt
run:      python -m src.ask "How do I request time off?"   (add --offline when no key is set)
eval:     python -m evals.run   (--offline for the stand-in model; saves evals/results/)
test:     python -m pytest -q tests

## Conventions
- Model: env `OPENROUTER_API_KEY` and `MODEL`. Default `MODEL` is `google/gemini-3.8-flash`. Never hard-code a key.
- Every model call goes through `src/llm.py` and appends one line to `logs/usage.jsonl`: model, tokens in, tokens out, cost, latency.
- Dates are ISO. Answer in the language of the question. Quote money and durations as the source document writes them.
- Success shape: `{answer, citations, grounded}`. Refusal is `grounded: false` plus the fixed refusal sentence, not an exception. Request errors are `{error, detail}`.
- Every new feature ships with a test that would fail if the feature broke, and a golden question once the answer path exists.

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
