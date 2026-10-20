import argparse
import json
import sys
from pathlib import Path

from prereqs import PrereqError, check

DATA = Path(__file__).with_name("courses.json")


def split_passed(raw):
    if raw.strip() == "":
        return []
    return raw.split(",")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Check course prerequisites.")
    parser.add_argument("course")
    parser.add_argument("--passed", default="")
    args = parser.parse_args(argv)
    data = json.loads(DATA.read_text(encoding="utf-8"))
    try:
        result = check(args.course, split_passed(args.passed), data["courses"])
    except PrereqError as err:
        body = {"error": err.code}
        if err.value is not None:
            body["value"] = err.value
        print(json.dumps(body))
        return 1
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
