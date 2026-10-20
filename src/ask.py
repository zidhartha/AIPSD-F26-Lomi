import argparse
import json
import sys

from src import llm, offline
from src.answer import ask


def main(argv=None):
    parser = argparse.ArgumentParser(description="Ask AI Mentor a question about the company documents.")
    parser.add_argument("question")
    parser.add_argument("--offline", action="store_true", help="use the offline stand-in instead of the model")
    args = parser.parse_args(argv)
    try:
        reply = ask(args.question, chat=offline.chat if args.offline else llm.chat)
    except llm.MissingKey as err:
        reply = {"error": "missing_key", "detail": str(err)}
    except OSError as err:
        reply = {"error": "model_unavailable", "detail": type(err).__name__}
    print(json.dumps(reply, ensure_ascii=False, indent=2))
    return 2 if "error" in reply else 0


if __name__ == "__main__":
    sys.exit(main())
