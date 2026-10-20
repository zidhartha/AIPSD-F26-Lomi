import json
import subprocess
import sys
import time
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from lookup import LookupError, lookup

SEED = json.loads((SRC / "scholarships.json").read_text(encoding="utf-8"))
CLI = SRC / "cli.py"
TODAY = "2026-10-20"


def run_cli(*args):
    return subprocess.run(
        [sys.executable, str(CLI), *args],
        capture_output=True,
        text=True,
        check=False,
    )


def test_need_based_grant_is_open():
    result = lookup("Need-Based Grant", TODAY, SEED["scholarships"])
    assert result["deadline"] >= TODAY
    assert result["name"]
    assert result["deadline"]
    assert isinstance(result["amount_gel"], int)
    assert result["eligibility"]


def test_match_ignores_case_and_whitespace():
    exact = lookup("Need-Based Grant", TODAY, SEED["scholarships"])
    messy = lookup("  need-based grant  ", TODAY, SEED["scholarships"])
    assert messy == exact


def test_deadline_on_today_is_open():
    result = lookup("Merit Award", TODAY, SEED["scholarships"])
    assert result["deadline"] == TODAY
    assert result["amount_gel"] == 2000


def test_passed_deadline():
    with pytest.raises(LookupError) as caught:
        lookup("Summer Research Stipend", TODAY, SEED["scholarships"])
    assert caught.value.code == "deadline_passed"
    assert caught.value.deadline == "2026-09-30"


def test_unknown_name():
    with pytest.raises(LookupError) as caught:
        lookup("Robotics Grant", TODAY, SEED["scholarships"])
    assert caught.value.code == "scholarship_not_found"


@pytest.mark.parametrize("name", ["", "   "])
def test_blank_name(name):
    with pytest.raises(LookupError) as caught:
        lookup(name, TODAY, SEED["scholarships"])
    assert caught.value.code == "invalid_name"


def test_cli_success_is_json_on_stdout_only():
    result = run_cli("Need-Based Grant", "--today", TODAY)
    assert result.returncode == 0
    assert result.stdout == json.dumps(
        {
            "name": "Need-Based Grant",
            "deadline": "2026-11-15",
            "amount_gel": 1500,
            "eligibility": "Full-time KIU undergraduates",
        }
    ) + "\n"
    assert result.stderr == ""


def test_cli_deadline_passed():
    result = run_cli("Summer Research Stipend", "--today", TODAY)
    assert result.returncode == 1
    assert json.loads(result.stdout) == {
        "error": "deadline_passed",
        "deadline": "2026-09-30",
    }


def test_cli_unknown_and_blank():
    unknown = run_cli("Robotics Grant", "--today", TODAY)
    blank = run_cli("   ", "--today", TODAY)
    assert unknown.returncode == 1
    assert json.loads(unknown.stdout) == {"error": "scholarship_not_found"}
    assert blank.returncode == 1
    assert json.loads(blank.stdout) == {"error": "invalid_name"}


def test_stale_file_warns_on_stderr_only():
    result = run_cli("Need-Based Grant", "--today", "2026-10-21")
    assert result.returncode == 0
    assert "more than 14 days" in result.stderr
    json.loads(result.stdout)


def test_seed_lookup_is_under_50ms():
    start = time.perf_counter()
    lookup("Need-Based Grant", TODAY, SEED["scholarships"])
    assert time.perf_counter() - start < 0.05
