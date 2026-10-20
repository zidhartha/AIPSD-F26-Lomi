import argparse
import json
import sys
from pathlib import Path

from hours import HoursError, hours

DATA = Path(__file__).with_name("office_hours.json")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Look up an instructor's office hours.")
    parser.add_argument("name")
    parser.add_argument("--today", required=True)
    parser.add_argument("--day", default=None)
    args = parser.parse_args(argv)
    data = json.loads(DATA.read_text(encoding="utf-8"))
    try:
        result = hours(args.name, args.today, data["instructors"], day=args.day)
    except HoursError as err:
        print(json.dumps({"error": err.code, **err.extra}))
        return 1
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
