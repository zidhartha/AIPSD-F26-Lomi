# 0002 · Offline refusal threshold 0.30, k stays 5

**Date:** 2026-10-20 · **Decided by:** Davit Jincharadze

**Context.** `evals/golden.yaml` was run twice with `MENTOR_OFFLINE=1`, because this machine has no `OPENROUTER_API_KEY`. The runs are `evals/results/2026-10-20-1646-offline-k5.json` and `evals/results/2026-10-20-1646-offline-k1.json`.

**What the runs said.** Both settings passed 3 of 5, pass rate 0.60, under the 0.70 gate. g1, g2, and g5 passed. g3 and g4 were retrieved (the refusal reason is `model: sources do not answer it`, not `below threshold`) and then declined by the offline extractor, which only copies a source when 60% of the question's stems overlap it. k=1 did not beat k=5.

**Decision.** Keep k = 5. Keep the live embedding threshold at cosine 0.25. Raise only the offline hash threshold to 0.30. At 0.25 the question "What is the guest cafeteria menu on Friday?" still reached the model: the best retrieved cosine was 0.27, from `handbook/leave-balance`. Unrelated English sits in that band for `offline/trigram-hash`.

**What we did not do.** g3 and g4 were not edited or deleted to make the offline run pass.

**Live run.** On 2026-10-20, with `openai/text-embedding-3-small` and `google/gemini-3.8-flash`, k = 5, `evals/results/2026-10-20-1734-live-k5.json` passed 5/5. k stayed 5. The cafeteria question was refused by the model (`model: sources do not answer it`), not by the score threshold.
