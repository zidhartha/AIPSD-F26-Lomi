# Delegation log · AI Mentor

One entry per delegation that mattered. Two minutes each. Lives at `docs/delegation-log.md`. HW1 asks for half a page of these.

### Entry 1 · Lab 4 pipeline and Design Review
- **Task:** spec acceptance criteria 1 to 3 (grounded answer, refusal below threshold, refusal on a citation that was not retrieved), the Lab 3 photo path, the Lab 4 golden set, and a first draft of every section of `docs/DESIGN-REVIEW.md`, the decision records 0001 and 0002, and the README.
- **Delegated to:** Cursor agent (Claude), rung 3. Context: `docs/spec.md`, `AGENTS.md`, `docs/TEAM-REPO.md`, the Design Review brief and the CampusPulse example. Driver: Elene27.
- **Plan check:** standard library only (no new dependency, so nothing to ask first); fictional seed corpus; no key in the repo; tests never call the model.
- **Came back wrong:** the first refusal threshold (2.0) was a guess, and would have sent "Does Brightpath pay for a gym membership?" (score 2.25) to the model. Golden g3 ("work from Spain for a whole month") is refused, because keyword retrieval does not know Spain is "another country". Kept as an honest failure, not replaced by an easier question.
- **Caught by:** printing best-chunk scores for on-topic and off-topic questions before fixing the number (decision 0002), then the offline golden run.
- **Decision:** threshold 3.5; g3 stays in the set and is diagnosed in the Design Review, section 4.
- **AGENTS.md change:** the run line now points at `python -m src.ask`, with `--offline` when no key is set.
- **Cost:** one session; no model spend (offline runs only until the live run).
