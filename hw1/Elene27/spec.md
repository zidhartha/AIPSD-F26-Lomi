# HW1 spec · Course prerequisite checker

*Individual feature · one page. From the repo root, Python 3.11 or newer.*
*install: `pip install -r requirements.txt`*
*run: `python hw1/Elene27/src/cli.py CS301 --passed CS101,MATH101`*
*test: `python -m pytest hw1/Elene27`*

## Goal

Before registration opens, a student gives a course code and the codes of the courses they have already passed. The tool says whether they can enroll and, if not, exactly which prerequisites are still missing.

## Users

KIU students planning next semester who do not want to find out at the registrar's desk that a prerequisite is missing.

## Acceptance criteria

1. Against `courses.json`, `check("CS201", ["CS101", "MATH101"])` returns `{"code": "CS201", "title": "Data Structures", "can_enroll": true, "missing": []}`.
2. When prerequisites are missing, `can_enroll` is `false` and `missing` lists them in the order the catalogue gives them. `check("CS301", ["CS101"])` gives `missing == ["CS201", "MATH201"]`.
3. Codes ignore case and surrounding whitespace: `"  cs201 "` with `[" cs101", "math101 "]` gives the same result as criterion 1.
4. A code that is blank or does not match two to four letters followed by three digits (for example `"CS 201"`) exits 1 and prints `{"error": "invalid_code", "value": "<input>"}`.
5. A well-formed code that is not in the catalogue exits 1 and prints `{"error": "course_not_found", "value": "<CODE>"}`.
6. A malformed entry in `--passed` (for example the empty entry in `CS101,,MATH101`) exits 1 and prints `{"error": "invalid_passed", "value": "<entry>"}`.
7. Asking about a course that is already in the passed list exits 1 and prints `{"error": "already_passed", "value": "<CODE>"}`.
8. Leaving out `--passed` means no courses passed. Every answer, including "cannot enroll", prints exactly one JSON object on stdout and nothing on stderr. "Cannot enroll" exits 0, because it is an answer and not an error.

## Context the agent needs

- `hw1/Elene27/src/courses.json`: an object with an `updated` ISO date and a `courses` list of `{code, title, prerequisites}`. `prerequisites` is a list of codes.
- `hw1/Elene27/spec.md`: this file.
- `AGENTS.md` at the repo root: test command and Never lines.

## Out of scope

Prerequisite chains (passing CS301's prerequisites does not unlock anything further), co-requisites, grade thresholds, seat limits, timetable clashes, registering for the course, and any model call.

## Napkin math

No model call and no network, so each check costs $0. The catalogue is six courses; a full KIU catalogue of about 400 courses is still a single linear scan, well under 50 ms.

## Risks

The catalogue can go stale when a department changes a prerequisite. `courses.json` carries `updated`, so a student or reviewer can see how old the data is.
