"""Command line: python src/cli.py "Chess Club" [--now 2026-10-20T09:00:00]"""
import argparse
import json
import sys
from datetime import datetime

from club_events import ClubNotFound, InvalidClub, load_events, next_events


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("club")
    parser.add_argument("--now", help="ISO time, default: current local time")
    args = parser.parse_args(argv)

    now = datetime.fromisoformat(args.now) if args.now else datetime.now()
    try:
        result = next_events(args.club, now, load_events())
    except ClubNotFound:
        print(json.dumps({"error": "club_not_found"}))
        return 1
    except InvalidClub:
        print(json.dumps({"error": "invalid_club"}))
        return 1

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
