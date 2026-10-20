import re

CODE = re.compile(r"^[A-Z]{2,4}[0-9]{3}$")


class PrereqError(Exception):
    def __init__(self, code, value=None):
        self.code = code
        self.value = value
        super().__init__(code)


def normalize(code):
    if not isinstance(code, str):
        return None
    cleaned = code.strip().upper()
    return cleaned if CODE.match(cleaned) else None


def check(course, passed, courses):
    key = normalize(course)
    if key is None:
        raise PrereqError("invalid_code", course)
    done = set()
    for item in passed:
        cleaned = normalize(item)
        if cleaned is None:
            raise PrereqError("invalid_passed", item)
        done.add(cleaned)
    for entry in courses:
        if entry["code"] == key:
            if key in done:
                raise PrereqError("already_passed", key)
            missing = [p for p in entry["prerequisites"] if p not in done]
            return {
                "code": entry["code"],
                "title": entry["title"],
                "can_enroll": not missing,
                "missing": missing,
            }
    raise PrereqError("course_not_found", key)
