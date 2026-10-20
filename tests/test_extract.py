import json

import pytest

from src.extract import decide, extract_page, validate

PAGE = "Every full-time employee has 24 working days of paid annual leave per calendar year."


def chat_returning(raw):
    def chat(messages, *, feature, **kwargs):
        assert messages[1]["content"][1]["image_url"]["url"].startswith("data:image/jpeg;base64,")
        return {"text": raw if isinstance(raw, str) else json.dumps(raw)}
    return chat


def extraction(confidence, problems=()):
    return {"title": "Annual leave", "text": PAGE, "confidence": confidence, "problems": list(problems)}


@pytest.mark.parametrize("confidence, problems, route", [
    (0.95, [], "accept"),
    (0.90, [], "accept"),
    (0.95, ["glare"], "confirm"),
    (0.75, [], "confirm"),
    (0.60, [], "confirm"),
    (0.59, [], "review"),
    (0.99, ["cut_off"], "review"),
    (0.99, ["handwriting"], "review"),
])
def test_decide_routes(confidence, problems, route):
    assert decide(extraction(confidence, problems)) == route


def test_review_route_never_prefills_text():
    result = extract_page(b"fake-image", chat=chat_returning(extraction(0.97, ["blurry"])))
    assert result == {"route": "review", "problems": ["blurry"]}


def test_accept_route_returns_the_text():
    result = extract_page(b"fake-image", chat=chat_returning(extraction(0.97)))
    assert result["route"] == "accept"
    assert result["text"] == PAGE


@pytest.mark.parametrize("raw", ["not json", {"text": PAGE, "confidence": 1.4}, {"text": PAGE, "confidence": "high"},
                                 {"confidence": 0.9}, {"text": "", "confidence": 0.99, "problems": []}])
def test_bad_or_empty_extraction_goes_to_review(raw):
    assert extract_page(b"fake-image", chat=chat_returning(raw))["route"] == "review"


def test_validate_rejects_boolean_confidence():
    assert validate({"text": PAGE, "confidence": True}) is None
