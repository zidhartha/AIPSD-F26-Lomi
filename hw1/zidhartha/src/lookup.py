class LookupError(Exception):
    def __init__(self, code, deadline=None):
        self.code = code
        self.deadline = deadline
        super().__init__(code)


def lookup(name, today, scholarships):
    if not isinstance(name, str) or not name.strip():
        raise LookupError("invalid_name")
    key = name.strip().casefold()
    for item in scholarships:
        if item["name"].strip().casefold() == key:
            if item["deadline"] < today:
                raise LookupError("deadline_passed", item["deadline"])
            return {
                "name": item["name"],
                "deadline": item["deadline"],
                "amount_gel": item["amount_gel"],
                "eligibility": item["eligibility"],
            }
    raise LookupError("scholarship_not_found")
