# Delegation log · Club Events Lookup

### Entry 1 · Build Club Events Lookup
- **Task:** The whole feature in `spec.md` — `next_events(club, now, events)` plus the CLI, meeting acceptance criteria 1–8.
- **Delegated to:** Claude (in Cursor), given only `hw1/Irakligig/spec.md` and `src/events.json`. I asked for a plan first, then the code; I read every line of the diff before accepting it.
- **Plan check:** The plan looked right (parse `--now`, filter by club, filter `start >= now`, sort, take 3). I added one instruction before approving: raise distinct `ClubNotFound` and `InvalidClub` errors so the CLI can return the two different error shapes in the spec, instead of one generic error.
- **Came back wrong:** The boundary case. The first version used `start > now`, so an event starting exactly at `now` was dropped — that breaks acceptance criterion 7 ("an event starting exactly at `now` is included").
- **Caught by:** Reading the tests first, then running them. `test_event_exactly_at_now_is_included` failed on the `>` version. I had written the golden questions and tests from the spec before trusting the code, so the gap showed up immediately rather than in a demo.
- **Decision:** Fixed in place — changed `>` to `>=` and re-ran. `pytest hw1/Irakligig` → 11 passed. I also deleted one line on purpose to confirm a test could actually go red before trusting the green.
- **AGENTS.md change:** None needed — the "run the test command before saying you are done" rule already covered what caught this.
- **Cost:** ~20 minutes, 2 extra test runs.
