# Club Events Lookup

**Goal:** Given a club name, return that club's next three upcoming events (title, start time, room).
**Users:** Students checking what their club is doing next.

## Run (from the repo root, Python 3.10+)

install: pip install pytest
run: python hw1/Irakligig/src/cli.py "Chess Club" --now 2026-10-20T09:00:00
test: python -m pytest hw1/Irakligig

## Data

src/events.json: list of {club, title, start (ISO 8601, local time), room}.

## Acceptance criteria

1. Returns at most 3 events with start >= now, sorted by start ascending.
2. Each event has title, start (ISO 8601) and room.
3. Club match ignores case and surrounding whitespace.
4. A known club with no upcoming events returns an empty list (exit 0).
5. An unknown club returns error `club_not_found` (exit 1).
6. An empty, whitespace-only or non-string club returns `invalid_club` (exit 1).
7. An event starting exactly at `now` is included; earlier events are not.
8. `now` is a parameter (CLI flag `--now`), so results are deterministic.

## Context the agent may use

This spec and src/events.json. No network, no model, no API key.

## Out of scope

Creating or editing events, recurring events, fuzzy club matching, web UI, authentication, time zones other than local time.
