# HW1 delegation log · Instructor office hours

**Date:** 2026-10-20 · **Tool:** Cursor agent · **Rung on the Autonomy Ladder:** 3 (agent writes the files, I review the diff and the command output before submitting)

**What I delegated.** "Build the feature in `hw1/SanndroP/spec.md`: seed data, CLI, tests, golden questions, this log, and the Week 1 to 4 journal. Do not edit any other `hw1/` folder or `docs/spec.md`."

**What the code got wrong.** The first run of `python -m pytest hw1/SanndroP` was 5 failed, 13 passed. Two causes. Weekday names were sorted as text, so Thursday came before Tuesday. Criterion 1 asks for Monday-through-Sunday order, and `test_nino_blocks_are_in_calendar_order` showed Thursday at index 0. An empty block list was turned into `{"error": "no_hours"}` and exit 1. Criterion 3 says Giorgi Kapanadze exits 0 with `"blocks": []`, and `test_cli_empty_blocks_exit_zero` printed that error instead.

**How I caught it.** I read the failing assertions, not the summary line. The sort key is now Monday through Sunday, then start time, and an empty list is returned. The same command was then 18 passed. I ran the three commands in `golden.md` and pasted the stdout and exit codes from that run. No network import is in `src/`.

**What I would change next time.** The spec already said both rules. Next time I want the calendar-order assertion written and read before I look at the sort line, so a green run cannot hide Thursday-before-Tuesday.
