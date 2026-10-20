import argparse
import base64
import json
import mimetypes
import sys
from pathlib import Path

from src import llm
from src.answer import parse_reply

ACCEPT_AT = 0.90
CONFIRM_AT = 0.60
HARD_FLAGS = {"cut_off", "blurry", "handwriting", "not_a_policy_page"}

SYSTEM = """You read a photo of one page of a company policy document.
Copy the text exactly; never fill in words you cannot read.
Reply with one JSON object and nothing else:
{"title": "<page heading or empty>", "text": "<the page text>", "confidence": <0.0 to 1.0>,
 "problems": [<any of "cut_off", "blurry", "handwriting", "not_a_policy_page", "glare", "partly_unreadable">]}"""


def validate(raw):
    if not isinstance(raw, dict):
        return None
    confidence = raw.get("confidence")
    problems = raw.get("problems", [])
    if not isinstance(confidence, (int, float)) or isinstance(confidence, bool) or not 0 <= confidence <= 1:
        return None
    if not isinstance(raw.get("text"), str) or not isinstance(problems, list):
        return None
    return {
        "title": str(raw.get("title") or ""),
        "text": raw["text"].strip(),
        "confidence": float(confidence),
        "problems": [str(p) for p in problems],
    }


def decide(extraction):
    if extraction is None or not extraction["text"]:
        return "review"
    if HARD_FLAGS & set(extraction["problems"]) or extraction["confidence"] < CONFIRM_AT:
        return "review"
    if extraction["confidence"] >= ACCEPT_AT and not extraction["problems"]:
        return "accept"
    return "confirm"


def extract_page(image_bytes, mime="image/jpeg", *, chat=llm.chat):
    data_url = f"data:{mime};base64,{base64.b64encode(image_bytes).decode('ascii')}"
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": [
            {"type": "text", "text": "Extract this policy page."},
            {"type": "image_url", "image_url": {"url": data_url}},
        ]},
    ]
    result = chat(messages, feature="extract")
    extraction = validate(parse_reply(result["text"]))
    route = decide(extraction)
    if route == "review":
        return {"route": route, "problems": extraction["problems"] if extraction else ["invalid_reply"]}
    return {"route": route, **extraction}


def main(argv=None):
    parser = argparse.ArgumentParser(description="Turn a photo of a policy page into text, or send it to a human.")
    parser.add_argument("image")
    args = parser.parse_args(argv)
    path = Path(args.image)
    if not path.is_file():
        print(json.dumps({"error": "image_not_found", "detail": str(path)}))
        return 2
    mime = mimetypes.guess_type(path.name)[0] or "image/jpeg"
    try:
        result = extract_page(path.read_bytes(), mime)
    except llm.MissingKey as err:
        result = {"error": "missing_key", "detail": str(err)}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2 if "error" in result else 0


if __name__ == "__main__":
    sys.exit(main())
