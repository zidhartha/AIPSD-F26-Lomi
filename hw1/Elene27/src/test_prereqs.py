import json
import subprocess
import sys
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parent
sys.path.insert(0, str(SRC))

from prereqs import PrereqError, check

COURSES = json.loads((SRC / "courses.json").read_text(encoding="utf-8"))["courses"]
CLI = SRC / "cli.py"


def run_cli(*args):
    return subprocess.run(
        [sys.executable, str(CLI), *args],
        capture_output=True,
        text=True,
        check=False,
    )


def test_all_prerequisites_passed():
    result = check("CS201", ["CS101", "MATH101"], COURSES)
    assert result == {
        "code": "CS201",
        "title": "Data Structures",
        "can_enroll": True,
        "missing": [],
    }


def test_missing_prerequisites_keep_catalogue_order():
    result = check("CS301", ["CS101"], COURSES)
    assert result["can_enroll"] is False
    assert result["missing"] == ["CS201", "MATH201"]


def test_course_without_prerequisites():
    result = check("CS101", [], COURSES)
    assert result["can_enroll"] is True
    assert result["missing"] == []


def test_codes_ignore_case_and_whitespace():
    messy = check("  cs201 ", [" cs101", "math101 "], COURSES)
    assert messy == check("CS201", ["CS101", "MATH101"], COURSES)


def test_unknown_course():
    with pytest.raises(PrereqError) as caught:
        check("PHYS999", [], COURSES)
    assert caught.value.code == "course_not_found"
    assert caught.value.value == "PHYS999"


@pytest.mark.parametrize("code", ["", "   ", "CS 201", "201CS", "C201"])
def test_invalid_course_code(code):
    with pytest.raises(PrereqError) as caught:
        check(code, [], COURSES)
    assert caught.value.code == "invalid_code"


def test_malformed_passed_entry():
    with pytest.raises(PrereqError) as caught:
        check("CS201", ["CS101", "", "MATH101"], COURSES)
    assert caught.value.code == "invalid_passed"


def test_already_passed():
    with pytest.raises(PrereqError) as caught:
        check("CS201", ["CS101", "MATH101", "CS201"], COURSES)
    assert caught.value.code == "already_passed"


def test_cli_success_is_json_on_stdout_only():
    result = run_cli("CS201", "--passed", "CS101,MATH101")
    assert result.returncode == 0
    assert result.stdout == json.dumps(
        {
            "code": "CS201",
            "title": "Data Structures",
            "can_enroll": True,
            "missing": [],
        }
    ) + "\n"
    assert result.stderr == ""


def test_cli_cannot_enroll_still_exits_0():
    result = run_cli("CS301", "--passed", "CS101")
    assert result.returncode == 0
    assert json.loads(result.stdout)["missing"] == ["CS201", "MATH201"]


def test_cli_no_passed_flag_means_nothing_passed():
    result = run_cli("CS350")
    assert result.returncode == 0
    assert json.loads(result.stdout)["missing"] == ["CS201"]


def test_cli_errors():
    unknown = run_cli("PHYS999")
    blank = run_cli("   ")
    malformed = run_cli("CS201", "--passed", "CS101,,MATH101")
    assert unknown.returncode == 1
    assert json.loads(unknown.stdout) == {"error": "course_not_found", "value": "PHYS999"}
    assert blank.returncode == 1
    assert json.loads(blank.stdout) == {"error": "invalid_code", "value": "   "}
    assert malformed.returncode == 1
    assert json.loads(malformed.stdout) == {"error": "invalid_passed", "value": ""}
