# Golden questions · Handbook lookup

Run from the repo root. No API key. `python -m pytest -q tests` was 7 passed.

| # | Question | Expected | Actual | Pass? | How I ran it |
|---|---|---|---|---|---|
| 1 | How do I request time off? | `"grounded": true` and `"citations": ["time-off.md"]` | `{"answer": "# Time off\n\nTo request time off, file a request in the HR form at least 5 working days ahead. Your manager approves it. Sick time off can be filed the same day.\n", "citations": ["time-off.md"], "grounded": true}` | pass | `python -m src.ask "How do I request time off?"` |
| 2 | What is the office dog's name? | `"grounded": false` and the refusal sentence | `{"answer": "That is not in the company documents.", "citations": [], "grounded": false}` | pass | `python -m src.ask "What is the office dog's name?"` |
| 3 | (empty) | `{"error": "invalid_question", "detail": "Question is empty."}` | `{"error": "invalid_question", "detail": "Question is empty."}` | pass | `python -m src.ask` |
