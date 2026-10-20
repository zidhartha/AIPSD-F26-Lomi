"""Tests stay offline: no key, no network. Logs go to a temp folder."""
import os
import tempfile

_tmp = tempfile.mkdtemp(prefix="mentor-tests-")
os.environ["MENTOR_OFFLINE"] = "1"
os.environ["MENTOR_USAGE_LOG"] = os.path.join(_tmp, "usage.jsonl")
os.environ["MENTOR_ANSWER_LOG"] = os.path.join(_tmp, "answers.jsonl")
os.environ.pop("MENTOR_MIN_SCORE", None)

import pytest  # noqa: E402

from src.extract import Extraction, Field  # noqa: E402


def field(value, evidence, confidence=0.95):
    return Field(value=value, evidence=evidence, confidence=confidence)


@pytest.fixture
def clean():
    return Extraction(
        title=field("Time off", "Time off"),
        action=field("File a request in the HR form", "File a request in the HR form"),
        timing=field("at least 5 working days ahead", "at least 5 working days ahead"),
        contact=field("your manager", "your manager"),
    )


@pytest.fixture
def degraded():
    return Extraction(
        title=field("Time off", "Time off"),
        action=Field(value=None, evidence=None, confidence=0.0),
        timing=field("at least 5 working days ahead", "at least 5 working days ahead"),
        contact=field("your manager", "your manager"),
    )


@pytest.fixture
def ambiguous():
    return Extraction(
        title=field("Time off", "Time off"),
        action=field("File a request in the HR form", "File a request in the HR form"),
        timing=field("sometime next week", "sometime next week??", confidence=0.42),
        contact=field("your manager", "your manager"),
    )


@pytest.fixture
def not_applicable():
    return Extraction(
        title=field("Friday lunch", "Friday lunch menu"),
        action=field("Soup and bread", "Soup and bread"),
        timing=field("Friday", "Friday"),
        contact=Field(value=None, evidence=None, confidence=0.0),
    )
