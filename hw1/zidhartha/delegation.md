# HW1 delegation log · Scholarship deadline lookup

**Date:** 2026-10-20 · **Tool:** Cursor agent · **Rung on the Autonomy Ladder:** 3 (agent writes the files, I review the diff and the command output before submitting)

**What I delegated.** "Write the HW1 feature described in `hw1/zidhartha/spec.md`: seed data, tests, CLI, golden questions, this log, and the Week 1 to 4 journal. The spec was already written. Do not change `docs/spec.md`."

**What the plan got wrong.** The spec says success prints JSON and no other text, and it also says the command warns when `scholarships.json` is more than 14 days old. Printing that warning on stdout would fail criterion 6. I sent the warning to stderr instead, and checked criterion 6 against a run where `updated` is only 14 days before `--today`, so the sample command stays silent.

**What the code got wrong.** The data file cannot be a bare list and also carry `updated`. The first layout that matches both sentences in the spec is an object with `updated` and `scholarships`. A test that only checked a bare list would have been wrong; the tests load `scholarships.json` as that object.

**How I verified.** Read the tests before treating the run as done. Ran `python -m pytest hw1/zidhartha` (12 passed). Ran the three commands in `golden.md` and pasted the stdout and exit codes from that run. No network import is in `src/`.

**What I would change next time.** Put the stdout-versus-stderr rule in the spec in one sentence, so the agent does not have to invent it.
