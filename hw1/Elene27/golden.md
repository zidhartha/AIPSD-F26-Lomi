# HW1 golden questions · Course prerequisite checker

Run from the repo root on 2026-10-20 in PowerShell, against `hw1/Elene27/src/courses.json` (`updated` 2026-10-12). The exit code was read with `echo $LASTEXITCODE` right after each command.

| # | Question (input) | Expected | Actual | Pass? | How I ran it |
|---|---|---|---|---|---|
| 1 | Can I take CS201 having passed CS101 and MATH101? | exit 0, `can_enroll` true, `missing` empty | `{"code": "CS201", "title": "Data Structures", "can_enroll": true, "missing": []}`, exit 0 | pass | `python hw1/Elene27/src/cli.py CS201 --passed CS101,MATH101` |
| 2 | Can I take CS301 having passed only CS101? | exit 0, `can_enroll` false, `missing` is CS201 then MATH201 | `{"code": "CS301", "title": "Algorithms", "can_enroll": false, "missing": ["CS201", "MATH201"]}`, exit 0 | pass | `python hw1/Elene27/src/cli.py CS301 --passed CS101` |
| 3 | Can I take PHYS999? (not in the catalogue) | exit 1, `{"error": "course_not_found", "value": "PHYS999"}` | `{"error": "course_not_found", "value": "PHYS999"}`, exit 1 | pass | `python hw1/Elene27/src/cli.py PHYS999 --passed CS101` |

What running them taught me: question 2 is the one a student actually cares about. It exits 0 even though the answer is "no", because the program answered correctly. Only bad input or an unknown course exits 1. `python -m pytest hw1/Elene27` was 16 passed.
