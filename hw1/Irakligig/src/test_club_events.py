from datetime import datetime

import pytest

from club_events import ClubNotFound, InvalidClub, next_events

NOW = datetime(2026, 10, 20, 9, 0, 0)

EVENTS = [
    {"club": "Chess Club", "title": "Past", "start": "2026-10-14T18:00:00", "room": "B1"},
    {"club": "Chess Club", "title": "E4", "start": "2026-10-28T10:00:00", "room": "B4"},
    {"club": "Chess Club", "title": "E1", "start": "2026-10-21T18:00:00", "room": "B1"},
    {"club": "Chess Club", "title": "E3", "start": "2026-10-23T17:00:00", "room": "B3"},
    {"club": "Chess Club", "title": "E2", "start": "2026-10-22T17:00:00", "room": "B2"},
    {"club": "Robotics Club", "title": "Old", "start": "2026-09-30T16:00:00", "room": "L3"},
]


def test_returns_three_earliest_sorted():
    result = next_events("Chess Club", NOW, EVENTS)
    assert [e["title"] for e in result] == ["E1", "E2", "E3"]


def test_each_event_has_title_start_room():
    result = next_events("Chess Club", NOW, EVENTS)
    assert set(result[0]) == {"title", "start", "room"}


def test_club_match_ignores_case_and_whitespace():
    assert next_events("  chess CLUB ", NOW, EVENTS) == next_events("Chess Club", NOW, EVENTS)


def test_known_club_with_no_upcoming_returns_empty_list():
    assert next_events("Robotics Club", NOW, EVENTS) == []


def test_unknown_club_raises_not_found():
    with pytest.raises(ClubNotFound):
        next_events("Chess Clubb", NOW, EVENTS)


@pytest.mark.parametrize("bad", ["", "   ", None, 42])
def test_invalid_club_raises(bad):
    with pytest.raises(InvalidClub):
        next_events(bad, NOW, EVENTS)


def test_event_exactly_at_now_is_included():
    events = [{"club": "A", "title": "Now", "start": "2026-10-20T09:00:00", "room": "R"}]
    assert [e["title"] for e in next_events("A", NOW, events)] == ["Now"]


def test_event_just_before_now_is_excluded():
    events = [{"club": "A", "title": "Late", "start": "2026-10-20T08:59:59", "room": "R"}]
    assert next_events("A", NOW, events) == []
