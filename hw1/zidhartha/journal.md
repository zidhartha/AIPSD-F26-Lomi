# Pattern Journal · zidhartha · Weeks 1 to 4

*One entry per week: the pattern, one place I used it, one thing I would do differently.*

## Week 1 · Context as Budget

**Where I used it:** setting up the team repo from the lab templates instead of copying the whole course folder in. **What I noticed:** the agent only needs the spec, the data file, and the run command; the rest of the course repo is noise. **Do differently:** name the three files the agent may read, in the spec, before asking it to build.

## Week 2 · Spec Before Code

**Where I used it:** `hw1/zidhartha/spec.md` was written before `cli.py`. The feature is a scholarship deadline lookup, not the club-events example. **What I noticed:** criteria 3 to 5 are the ones that stop a "successful" wrong program: a passed deadline, an unknown name, and a blank name each have an exit code and a JSON error. **Do differently:** write those error lines first. They are the ones I skip when I start from the happy path.

## Week 3 · Uncertainty-Aware UX

**Where I used it:** an unknown scholarship stays `scholarship_not_found`. The program does not guess a nearby name. **What I noticed:** a fuzzy match would look helpful and be wrong, the same way a model's confidence number can look sure when the evidence is missing. **Do differently:** leave fuzzy matching in "out of scope" unless the spec says how many suggestions and in what order.

## Week 4 · Grounded Generation

**Where I used it:** the three golden questions. Each row has the command, the expected JSON, and the stdout from a real run. **What I noticed:** question 2 exits 1, and that exit code is the evidence, not a failure of the run. **Do differently:** paste the output before marking pass. A row with no actual output is not a golden question.
