# 0002 · Refuse below a BM25 score of 3.5 (the Lab 4 setting we tuned)

**Date:** Week 4 (2026-10-20) · **Decided by:** proposed by Elene27 with a Cursor agent, approved in the pull request review

**Context.** Spec acceptance criterion 2: below the threshold, refuse without calling the model. BM25 scores have no fixed scale, so the number has to come from our own corpus.

**Decision.** `THRESHOLD = 3.5` in `src/retrieve.py`, with k = 5.

**Evidence.** Best-chunk scores on the seed corpus, measured before choosing:

| Question | Best score | Should |
|---|---|---|
| How do I request time off? | 8.72 | answer |
| How many days of paid annual leave do I get? | 7.10 | answer |
| What is the limit for a client meal? | 7.52 | answer |
| sick 4 days, need doctor note?? | 9.94 | answer |
| Does Brightpath pay for a gym membership? | 2.25 | refuse |
| What is the dress code? | 2.21 | refuse |
| What is the parental leave policy? | 1.79 | refuse |
| Who is the CEO? | 0 (no hit) | refuse |

The first guess, 2.0, would have sent the gym and dress-code questions to the model. 3.5 sits between the highest off-topic score (2.25) and the lowest on-topic one (7.10).

**Alternatives.** 2.0 (lets off-topic questions through), 5.0 (closer to real answers, no gain on this corpus). Relying only on the model to refuse: costs a call and trusts the model with the one decision that must not fail.

**Consequences.** Off-topic questions cost $0. The threshold must be re-measured when the corpus changes; `tests/test_retrieve.py` fails if a known off-topic question rises above it or the time-off question falls below it.
