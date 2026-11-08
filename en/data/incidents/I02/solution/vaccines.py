"""Pet vaccines: which are overdue and which are due soon.

The vaccines of a pet are a list like those of data/vaccines.json:
[{"vaccine": "rabies", "last": "2026-08-22", "next": "2027-08-22"}, …].
"""
import config
from utils import add_days


def overdue(pet_vaccines, today):
    """The vaccines whose next dose was already due: the "next" date is today or
    earlier."""
    return [v["vaccine"] for v in pet_vaccines if v["next"] <= today]


def upcoming(pet_vaccines, today, days=config.VACCINE_NOTICE_DAYS):
    """The vaccines due in the next "days" days, not counting the overdue ones."""
    limit = add_days(today, days)
    return [v["vaccine"] for v in pet_vaccines if today < v["next"] <= limit]


def pending_notices(vaccines, today):
    """The pets that have a vaccine overdue or due soon, with those vaccines, by pet
    id."""
    notices = {}
    for pet, theirs in vaccines.items():
        due = overdue(theirs, today) + upcoming(theirs, today)
        if due:
            notices[pet] = due
    return notices
