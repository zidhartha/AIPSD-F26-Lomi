"""Club Events Lookup: return a club's next upcoming events."""
import json
from datetime import datetime
from pathlib import Path

DEFAULT_DATA = Path(__file__).with_name("events.json")


class ClubNotFound(Exception):
    """The club name does not match any club in the data."""


class InvalidClub(Exception):
    """The club name is empty, blank, or not a string."""


def load_events(path=DEFAULT_DATA):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def next_events(club, now, events, limit=3):
    """Return up to `limit` events with start >= now, sorted by start."""
    if not isinstance(club, str) or not club.strip():
        raise InvalidClub("club must be a non-empty string")

    key = club.strip().lower()
    club_events = [e for e in events if e["club"].strip().lower() == key]
    if not club_events:
        raise ClubNotFound(club)

    upcoming = [e for e in club_events if datetime.fromisoformat(e["start"]) >= now]
    upcoming.sort(key=lambda e: datetime.fromisoformat(e["start"]))
    return [
        {"title": e["title"], "start": e["start"], "room": e["room"]}
        for e in upcoming[:limit]
    ]
