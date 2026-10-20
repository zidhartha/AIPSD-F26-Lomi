# Pattern Journal · Elene27 · Weeks 1 to 4

*One entry per week: the pattern, one place I saw or used it, one thing I would do differently.*

## Week 1 · 2026-09-22 · Context as Budget

**Where I saw it:** the prerequisite checker only needs `courses.json` and the spec. Giving the agent the whole team repo made it read my teammates' folders and treat them as mine. **What I noticed:** extra context is not free. It is room for the agent to act on the wrong thing. **Do differently:** list the exact folder the agent may write to in the first message.

## Week 2 · 2026-09-29 · Spec Before Code

**Where I used it:** I decided "cannot enroll" is a normal answer (exit 0) and wrote it into criterion 8 before any code existed. Without that line, it would have been natural to exit 1 when a student is missing a course. **What I noticed:** the hard part of the spec was not the happy path but the line between an answer and an error. **Do differently:** for every "no" the program can say, write down whether it is a result or a failure.

## Week 3 · 2026-10-06 · Uncertainty-Aware UX

**Where I used it:** `PHYS999` returns `course_not_found` and `CS 201` returns `invalid_code`, two different errors. The tool never guesses that `CS 201` meant `CS201`. **What I noticed:** a student who sees `can_enroll: true` will register, so a confident wrong answer is worse than a refusal. **Do differently:** keep chains of prerequisites out of scope until the catalogue says how deep they go, instead of quietly checking only one level and implying more.

## Week 4 · 2026-10-13 · Grounded Generation

**Where I used it:** every row in `golden.md` was pasted from a real run with its exit code, and the expected column was written first. **What I noticed:** the `missing` list is grounded in the catalogue order, not in whatever order the student typed, so the same question always gives the same answer. **Do differently:** record the data file's `updated` date next to the golden questions, so a later failure can be traced to new data instead of new code.
