# HW1 spec · Scholarship deadline lookup

*Individual feature · one page. From the repo root, Python 3.11.*
*install: `pip install pytest`*
*run: `python hw1/zidhartha/src/cli.py "Need-Based Grant" --today 2026-10-20`*
*test: `python -m pytest hw1/zidhartha`*

## Goal

A student types a scholarship name and gets that scholarship's deadline, award amount in GEL, and who may apply, but only if the deadline is still open on the given day. Nothing else.

## Users

KIU students who know the scholarship's name and do not know whether the deadline has passed or how much it pays.

## Acceptance criteria

1. `lookup("Need-Based Grant", today=2026-10-20)` returns one scholarship whose `deadline >= today`, with non-empty `name`, `deadline` (ISO date), `amount_gel` (integer), and `eligibility`.
2. The match ignores case and surrounding whitespace, so `"  need-based grant  "` is the same scholarship.
3. A scholarship whose deadline is before `today` exits 1 and prints `{"error": "deadline_passed", "deadline": "<ISO date>"}`. A deadline equal to `today` is still open.
4. An unknown name exits 1 and prints `{"error": "scholarship_not_found"}`.
5. An empty or whitespace-only name exits 1 and prints `{"error": "invalid_name"}`.
6. Success prints one JSON object to stdout and exits 0. No other text is printed.
7. On the seed file, the command finishes in under 50 ms. No network, no model call.

## Context the agent needs

- `hw1/zidhartha/src/scholarships.json`: a list of `{name, deadline, amount_gel, eligibility}`. Deadlines are ISO dates. The file includes an `updated` date.
- `hw1/zidhartha/spec.md`: this file.
- `AGENTS.md` at the repo root: conventions and Never lines.

## Out of scope

Applying for a scholarship, uploading documents, fuzzy name matching, currency conversion, a web page, accounts, and any model call.

## Napkin math

No model call, so cost is $0 per lookup. A later slice that matches a typed sentence to a scholarship name would budget about 300 input tokens per request.

## Risks

Stale `scholarships.json` can show a deadline the office has already moved. The data file carries `updated`, and the command warns when that date is more than 14 days before `today`.
