# 0001 · Keyword retrieval (BM25), not long context and not embeddings yet

**Date:** Week 4 (2026-10-20) · **Decided by:** proposed by Elene27 with a Cursor agent, approved in the pull request review

**Context.** The answer path needs passages to cite and a score to refuse on (spec, acceptance criteria 1 and 2). We could send the whole handbook in every prompt, embed chunks with a second model, or rank chunks by keywords.

**Decision.** Rank `## ` sections of `data/corpus/` with BM25 in plain Python (`src/retrieve.py`), send the top k = 5 to the model, and refuse below a score threshold before any model call.

**Alternatives.**
- *Long context.* The seed corpus is about 1,030 tokens, so it would fit, but a real handbook is about 180,000 tokens (spec napkin math): about $0.14 per question instead of under $0.001, and no per-chunk score to refuse on.
- *Embeddings.* Better at synonyms, but a second model call per question, a second vendor, and an index to rebuild. Not needed to prove the pipeline in Week 4.

**Consequences.** No extra dependency, no embedding cost, deterministic tests. It misses synonyms: golden g3 ("work from Spain for a month") does not match "another country … 20 working days" and is refused. We watch g3; if the Week 11 set has more misses like it, we add embeddings as a second ranker and record that decision.
