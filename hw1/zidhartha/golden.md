# HW1 golden questions · Scholarship deadline lookup

Run from the repo root. Seed file: `hw1/zidhartha/src/scholarships.json` (`updated` 2026-10-06). `--today` is 2026-10-20, so no stale-data warning is expected.

| # | Question (input) | Expected | Actual | Pass? | How I ran it |
|---|---|---|---|---|---|
| 1 | `"Need-Based Grant"` | one JSON object, exit 0: name Need-Based Grant, deadline 2026-11-15, amount_gel 1500, eligibility Full-time KIU undergraduates | `{"name": "Need-Based Grant", "deadline": "2026-11-15", "amount_gel": 1500, "eligibility": "Full-time KIU undergraduates"}`, exit 0 | pass | `python hw1/zidhartha/src/cli.py "Need-Based Grant" --today 2026-10-20` |
| 2 | `"Summer Research Stipend"` | exit 1, `{"error": "deadline_passed", "deadline": "2026-09-30"}` | `{"error": "deadline_passed", "deadline": "2026-09-30"}`, exit 1 | pass | `python hw1/zidhartha/src/cli.py "Summer Research Stipend" --today 2026-10-20` |
| 3 | `"Robotics Grant"` | exit 1, `{"error": "scholarship_not_found"}` | `{"error": "scholarship_not_found"}`, exit 1 | pass | `python hw1/zidhartha/src/cli.py "Robotics Grant" --today 2026-10-20` |

What I learned from running them: question 2 exits 1 on purpose. A red exit code here is the feature working, not a crash. `python -m pytest hw1/zidhartha` was 12 passed.
