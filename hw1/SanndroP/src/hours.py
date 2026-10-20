WEEKDAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]
ORDER = {name: index for index, name in enumerate(WEEKDAYS)}


class HoursError(Exception):
    def __init__(self, code, extra=None):
        self.code = code
        self.extra = extra or {}
        super().__init__(code)


def canonical_day(day):
    if not isinstance(day, str):
        return None
    key = day.strip().casefold()
    for name in WEEKDAYS:
        if name.casefold() == key:
            return name
    return None


def hours(name, today, instructors, day=None):
    if not isinstance(name, str) or not name.strip():
        raise HoursError("invalid_name")
    chosen = None
    if day is not None:
        chosen = canonical_day(day)
        if chosen is None:
            raise HoursError("invalid_day", {"value": day})
    key = name.strip().casefold()
    for person in instructors:
        if person["name"].strip().casefold() != key:
            continue
        until = person.get("on_leave_until")
        if until and today < until:
            raise HoursError("on_leave", {"until": until})
        blocks = []
        for block in person["blocks"]:
            block_day = canonical_day(block["day"])
            if chosen and block_day != chosen:
                continue
            blocks.append(
                {
                    "day": block_day,
                    "start": block["start"],
                    "end": block["end"],
                    "room": block["room"],
                    "mode": block["mode"],
                }
            )
        blocks.sort(key=lambda block: (ORDER[block["day"]], block["start"]))
        return {
            "name": person["name"],
            "department": person["department"],
            "blocks": blocks,
        }
    raise HoursError("instructor_not_found")
