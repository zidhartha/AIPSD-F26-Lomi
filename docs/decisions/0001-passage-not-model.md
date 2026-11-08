# 0001 · First slice returns the passage, not a model answer

**Date:** Week 2 · **Decided by:** Davit Jincharadze

**Context.** The product answers from company documents. A model call needs a key, and Lab 2's first slice has to pass in CI with no key.

**Decision.** `ask()` returns the retrieved passage and its filename, or the fixed refusal. It does not call a model.

**Alternatives.** Call `google/gemini-3.8-flash` on every question. That matches the later product and fails CI without a key. We also considered keyword search that always returns the closest document. That would invent an answer for "office dog."

**Consequences.** The employee sees the handbook paragraph, which is easier to check and less pleasant to read. A later slice can paraphrase the same passage. The refusal sentence stays fixed.
