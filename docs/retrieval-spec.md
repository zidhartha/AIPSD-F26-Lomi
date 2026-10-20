# Retrieval spec · AI Mentor

## 1 · What the documents are

| Folder in `data/corpus/` | What is in it | Who owns the real version | How often it changes | Documents |
|---|---|---|---|---|
| `./` (three files) | The Lab 2 seed rules: time off, laptop, code review | Spec keeper, until a real company replaces them | When a rule changes | 3 |
| `handbook/` | The rest of the same fictional company handbook | Spec keeper | When a rule changes | 12 |

Fifteen documents in total. They are fictional and shareable. Not in the corpus, on purpose: cafeteria menus, salaries, and personal records. Those questions are refusals.

`src/ask.py` still reads only the three files in the corpus root, so the Lab 2 passage lookup does not change. Retrieval for the grounded answer reads every markdown file under `data/corpus/`.

## 2 · Chunking

- Split on: `## ` headings. A file with no heading becomes one Overview chunk. That is how the three seed files are stored.
- Header glued to each chunk before embedding: `title · section`
- Maximum size: 1200 characters. Overlap: the last paragraph of the previous piece.

## 3 · Retrieval

- Embedding model: `openai/text-embedding-3-small` via OpenRouter, env `EMBED_MODEL`. Price $0.02 per million input tokens, checked on the course Lab 4 example, 13 October 2026.
- Offline tests and CI use `offline/trigram-hash` when `MENTOR_OFFLINE=1`. Those vectors are not comparable with the OpenAI ones. `src/index.py` refuses to load an index built by the other model.
- Retriever: hybrid, vector cosine plus BM25, merged with reciprocal rank fusion. k = 5.
- Refusal threshold: cosine 0.25 for `openai/text-embedding-3-small`. The offline hash uses 0.30, because unrelated English still scores about 0.27. Recorded in `docs/decisions/0002-k-and-threshold.md`.

## 4 · Answering

- Model: env `MODEL`, default `google/gemini-3.8-flash`.
- Reply shape: `{answer, citations, grounded}`, validated by `Reply` in `src/answer.py`. No confidence field.
- Every sentence cites a retrieved source as `[n]`. A citation that fails `check_citations()` is a refusal, never a warning.
- Refuse before calling the model when the best cosine score is under the threshold. The refusal sentence is `That is not in the company documents.`

## 5 · What the user sees

- A cited answer looks like: "File a request in the HR form at least 5 working days ahead [1]." The `[1]` opens `time-off`.
- A refusal says: "That is not in the company documents." Next step: ask a teammate, or rephrase from a handbook title.

## 6 · Acceptance criteria

- AC1 "How do I request time off?" returns `answered`, citing `time-off`.
- AC2 "What is the guest cafeteria menu on Friday?" returns `refused` without a model call.
- AC3 A reply citing source `[7]` when fewer sources were retrieved is refused.
- AC4 Every answer and every refusal writes one line to `logs/answers.jsonl` with the reason.
- AC5 `evals/golden.yaml` passes at 0.70 or above on a live run. An offline run measures retrieval and the citation checks only.
