# HW1 spec · Instructor office hours

*Individual feature · one page. From the repo root, Python 3.11.*
*install: `pip install pytest`*
*run: `python hw1/SanndroP/src/cli.py "Nino Beridze" --today 2026-10-20`*
*test: `python -m pytest hw1/SanndroP`*

## Goal

A student types an instructor's full name and gets that person's weekly office hours: weekday, start, end, room, and whether the block is drop-in or by appointment. If the instructor is on leave that day, the tool says so and does not list the hours.

## Users

KIU students who know the instructor's name and need the room and time before they walk over.

## Acceptance criteria

1. `hours("Nino Beridze", today="2026-10-20")` returns her name, department Computer Science, and blocks in calendar order (Monday through Sunday, then start). Tuesday 14:00–15:30 in A-118, drop-in, comes before Thursday 10:00–11:00 in A-118, appointment.
2. The match ignores case and surrounding whitespace, so `"  nino beridze  "` is the same instructor. A first name alone (`"Nino"`) is not a match.
3. A known instructor with no blocks exits 0 and prints `"blocks": []`. Giorgi Kapanadze is that case. An empty list is an answer, not an error.
4. When `today` is strictly before `on_leave_until`, the command exits 1 and prints `{"error": "on_leave", "until": "<ISO date>"}` and no blocks. On the `until` date the instructor is back. Mariam Gelashvili is on leave until 2026-11-02.
5. An unknown name exits 1 and prints `{"error": "instructor_not_found"}`.
6. An empty or whitespace-only name exits 1 and prints `{"error": "invalid_name"}`.
7. `--day Tuesday` returns only that weekday. `--day tuesday` is the same day. A word that is not a weekday, such as `Funday`, exits 1 and prints `{"error": "invalid_day", "value": "Funday"}`. A real weekday with no block exits 0 and prints `"blocks": []`.
8. Success prints one JSON object on stdout and exits 0. Errors print one JSON object on stdout and exit 1. Stderr stays empty. No network and no model call. On the seed file the lookup finishes in under 50 ms.

## Context the agent needs

- `hw1/SanndroP/src/office_hours.json`: `updated` plus `instructors`. Each instructor has `name`, `department`, `blocks` (`day`, `start`, `end`, `room`, `mode`), and may have `on_leave_until`.
- `hw1/SanndroP/spec.md`: this file.
- `AGENTS.md` at the repo root: the Never lines. Do not read or edit any other `hw1/` folder.

## Out of scope

Booking a slot, sending mail, fuzzy or partial names, hours that change week to week, time zones, a web page, accounts, and any model call.

## Napkin math

No model call, so cost is $0 per lookup. A later slice that maps a typed sentence to a full name would budget about 200 input tokens per request.

## Risks

The office can move a block and `office_hours.json` will be wrong until someone edits it. The file carries `updated` so a reader can see the age. The command does not guess a nearby name.
