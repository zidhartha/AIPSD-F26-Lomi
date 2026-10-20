# HW1 golden questions · Instructor office hours

Run from the repo root. Seed file: `hw1/SanndroP/src/office_hours.json` (`updated` 2026-10-13). `--today` is 2026-10-20.

| # | Question (input) | Expected | Actual | Pass? | How I ran it |
|---|---|---|---|---|---|
| 1 | `"Nino Beridze"` | exit 0, one JSON object: Computer Science, Tuesday 14:00 drop-in in A-118, then Thursday 10:00 appointment in A-118 | `{"name": "Nino Beridze", "department": "Computer Science", "blocks": [{"day": "Tuesday", "start": "14:00", "end": "15:30", "room": "A-118", "mode": "drop-in"}, {"day": "Thursday", "start": "10:00", "end": "11:00", "room": "A-118", "mode": "appointment"}]}`, exit 0 | pass | `python hw1/SanndroP/src/cli.py "Nino Beridze" --today 2026-10-20` |
| 2 | `"Mariam Gelashvili"` | exit 1, `{"error": "on_leave", "until": "2026-11-02"}`, no blocks | `{"error": "on_leave", "until": "2026-11-02"}`, exit 1 | pass | `python hw1/SanndroP/src/cli.py "Mariam Gelashvili" --today 2026-10-20` |
| 3 | `"Nino"` | exit 1, `{"error": "instructor_not_found"}`. A first name is not a match | `{"error": "instructor_not_found"}`, exit 1 | pass | `python hw1/SanndroP/src/cli.py "Nino" --today 2026-10-20` |

What I learned from running them: question 2 exits 1 on purpose. A red exit code here means she is on leave, not that the program crashed. Question 3 is the same exit code for a different reason: the tool will not guess that "Nino" means Nino Beridze. `python -m pytest hw1/SanndroP` was 18 passed.
