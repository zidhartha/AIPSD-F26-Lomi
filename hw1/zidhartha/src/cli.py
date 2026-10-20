import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path

from lookup import LookupError, lookup

DATA = Path(__file__).with_name("scholarships.json")


def warn_if_stale(updated, today):
    if date.fromisoformat(updated) < date.fromisoformat(today) - timedelta(days=14):
        print(
            f"warning: scholarships.json updated {updated} is more than 14 days before {today}",
            file=sys.stderr,
        )


def main(argv=None):
    parser = argparse.ArgumentParser(description="Look up an open scholarship deadline.")
    parser.add_argument("name")
    parser.add_argument("--today", required=True)
    args = parser.parse_args(argv)
    data = json.loads(DATA.read_text(encoding="utf-8"))
    warn_if_stale(data["updated"], args.today)
    try:
        result = lookup(args.name, args.today, data["scholarships"])
    except LookupError as err:
        body = {"error": err.code}
        if err.deadline is not None:
            body["deadline"] = err.deadline
        print(json.dumps(body))
        return 1
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
