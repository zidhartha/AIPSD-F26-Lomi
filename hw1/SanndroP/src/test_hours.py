import json
import subprocess
import sys
import time
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parent
sys.path.insert(0, str(SRC))

from hours import HoursError, hours

SEED = json.loads((SRC / "office_hours.json").read_text(encoding="utf-8"))
INSTRUCTORS = SEED["instructors"]
CLI = SRC / "cli.py"
TODAY = "2026-10-20"


def run_cli(*args):
    return subprocess.run(
        [sys.executable, str(CLI), *args],
        capture_output=True,
        text=True,
        check=False,
    )


def test_nino_blocks_are_in_calendar_order():
    result = hours("Nino Beridze", TODAY, INSTRUCTORS)
    assert result["name"] == "Nino Beridze"
    assert result["department"] == "Computer Science"
    assert result["blocks"] == [
        {
            "day": "Tuesday",
            "start": "14:00",
            "end": "15:30",
            "room": "A-118",
            "mode": "drop-in",
        },
        {
            "day": "Thursday",
            "start": "10:00",
            "end": "11:00",
            "room": "A-118",
            "mode": "appointment",
        },
    ]


def test_luka_sorts_by_weekday_then_start():
    result = hours("Luka Tsintsadze", TODAY, INSTRUCTORS)
    assert [(block["day"], block["start"]) for block in result["blocks"]] == [
        ("Monday", "11:00"),
        ("Wednesday", "09:00"),
        ("Wednesday", "16:00"),
    ]


def test_match_ignores_case_and_whitespace():
    exact = hours("Nino Beridze", TODAY, INSTRUCTORS)
    messy = hours("  nino beridze  ", TODAY, INSTRUCTORS)
    assert messy == exact


def test_first_name_is_not_a_match():
    with pytest.raises(HoursError) as caught:
        hours("Nino", TODAY, INSTRUCTORS)
    assert caught.value.code == "instructor_not_found"


def test_known_instructor_with_no_blocks():
    result = hours("Giorgi Kapanadze", TODAY, INSTRUCTORS)
    assert result == {
        "name": "Giorgi Kapanadze",
        "department": "Mathematics",
        "blocks": [],
    }


def test_on_leave_before_until_date():
    with pytest.raises(HoursError) as caught:
        hours("Mariam Gelashvili", TODAY, INSTRUCTORS)
    assert caught.value.code == "on_leave"
    assert caught.value.extra == {"until": "2026-11-02"}


def test_back_from_leave_on_until_date():
    result = hours("Mariam Gelashvili", "2026-11-02", INSTRUCTORS)
    assert result["blocks"] == [
        {
            "day": "Monday",
            "start": "13:00",
            "end": "14:00",
            "room": "C-010",
            "mode": "drop-in",
        }
    ]


def test_unknown_name():
    with pytest.raises(HoursError) as caught:
        hours("Ana Chkheidze", TODAY, INSTRUCTORS)
    assert caught.value.code == "instructor_not_found"


@pytest.mark.parametrize("name", ["", "   "])
def test_blank_name(name):
    with pytest.raises(HoursError) as caught:
        hours(name, TODAY, INSTRUCTORS)
    assert caught.value.code == "invalid_name"


def test_day_filter_and_case():
    tuesday = hours("Nino Beridze", TODAY, INSTRUCTORS, day="Tuesday")
    lower = hours("Nino Beridze", TODAY, INSTRUCTORS, day="tuesday")
    assert tuesday == lower
    assert [block["day"] for block in tuesday["blocks"]] == ["Tuesday"]


def test_invalid_day():
    with pytest.raises(HoursError) as caught:
        hours("Nino Beridze", TODAY, INSTRUCTORS, day="Funday")
    assert caught.value.code == "invalid_day"
    assert caught.value.extra == {"value": "Funday"}


def test_real_weekday_with_no_block_is_empty():
    result = hours("Nino Beridze", TODAY, INSTRUCTORS, day="Monday")
    assert result["blocks"] == []


def test_cli_success_is_json_on_stdout_only():
    result = run_cli("Nino Beridze", "--today", TODAY)
    assert result.returncode == 0
    assert result.stderr == ""
    assert json.loads(result.stdout)["blocks"][0]["day"] == "Tuesday"


def test_cli_on_leave_and_unknown_and_blank():
    leave = run_cli("Mariam Gelashvili", "--today", TODAY)
    unknown = run_cli("Ana Chkheidze", "--today", TODAY)
    blank = run_cli("   ", "--today", TODAY)
    assert leave.returncode == 1
    assert json.loads(leave.stdout) == {"error": "on_leave", "until": "2026-11-02"}
    assert leave.stderr == ""
    assert unknown.returncode == 1
    assert json.loads(unknown.stdout) == {"error": "instructor_not_found"}
    assert blank.returncode == 1
    assert json.loads(blank.stdout) == {"error": "invalid_name"}


def test_cli_invalid_day():
    result = run_cli("Nino Beridze", "--today", TODAY, "--day", "Funday")
    assert result.returncode == 1
    assert json.loads(result.stdout) == {"error": "invalid_day", "value": "Funday"}
    assert result.stderr == ""


def test_cli_empty_blocks_exit_zero():
    result = run_cli("Giorgi Kapanadze", "--today", TODAY)
    assert result.returncode == 0
    assert json.loads(result.stdout)["blocks"] == []
    assert result.stderr == ""


def test_seed_lookup_is_under_50ms():
    start = time.perf_counter()
    hours("Nino Beridze", TODAY, INSTRUCTORS)
    assert time.perf_counter() - start < 0.05
