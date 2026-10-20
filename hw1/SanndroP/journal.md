# Pattern Journal · SanndroP · Weeks 1 to 4

*One entry per week: the pattern, one place I saw or used it, one thing I would do differently.*

## Week 1 · 2026-09-22 · Context as Budget

**Where I used it:** my HW1 folder is `hw1/SanndroP`, and the only files the feature needs are this spec and `office_hours.json`. **What I noticed:** the other `hw1/` folders already hold a scholarship lookup, a prerequisite check, and a club-events list. That is the wrong context for my feature. The useful part is the folder shape, not their content. **Do differently:** name my GitHub username and the one folder the agent may write, in the first message, before it goes looking for a model.

## Week 2 · 2026-09-29 · Spec Before Code

**Where I used it:** `spec.md` was written before `hours.py`. Criteria 3 and 4 both mean "no hours to show," and they are not the same result: Giorgi Kapanadze exits 0 with an empty list, and Mariam Gelashvili exits 1 with `on_leave`. **What I noticed:** if I start from the happy path, both of those become an error, which is what the first code did. **Do differently:** write the exit code next to every "no" before asking for any file.

## Week 3 · 2026-10-06 · Uncertainty-Aware UX

**Where I used it:** `"Nino"` stays `instructor_not_found`. The program does not offer Nino Beridze as a guess. **What I noticed:** a suggestion would look helpful and could send a student to the wrong room, the same way a confident answer with no evidence looks done. **Do differently:** leave partial names in "out of scope" unless the spec says how many suggestions and in what order.

## Week 4 · 2026-10-20 · Grounded Generation

**Where I used it:** the three rows in `golden.md`. Each one has the command, the expected JSON, and the stdout from a real run, including the exit 1 for leave. **What I noticed:** Thursday-before-Tuesday was still valid JSON. The calendar-order test is what showed it was the wrong answer. A row with no actual output would have hidden that. **Do differently:** paste the output before marking pass, and keep the order assertion even after the happy path looks right.
