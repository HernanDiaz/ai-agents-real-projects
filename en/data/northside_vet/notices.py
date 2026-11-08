"""Messages for the owners: vaccine reminders."""
from utils import format_date

SIGNATURE = "Best regards,\nNorthside Veterinary Clinic"


def greeting(owner):
    """The greeting with the owner's first name."""
    return f"Hi {owner['name'].split()[0]},"


def vaccine_reminder(owner, pet, vaccine):
    """Reminder that a pet is due for a vaccine. "vaccine" is like those of
    data/vaccines.json, with its "next" date."""
    return (f"{greeting(owner)}\n\n"
            f"{pet['name']} is due for the {vaccine['vaccine']} vaccine on "
            f"{format_date(vaccine['next'])}. You can call the clinic to book an "
            f"appointment.\n\n{SIGNATURE}")
