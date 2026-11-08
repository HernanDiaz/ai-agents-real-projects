"""Messages for the owners: vaccine and appointment reminders."""
from utils import format_date

SIGNATURE = "Best regards,\nNorthside Veterinary Clinic"


def greeting(owner):
    """The greeting with the owner's first name."""
    return f"Hi {owner['name'].split()[0]},"


def appointment_reminder(owner, pet, appointment):
    """Reminder of an appointment, with the day and the time."""
    return (f"{greeting(owner)}\n\n"
            f"This is a reminder of {pet['name']}'s appointment on "
            f"{format_date(appointment['date'])} at {appointment['time']}."
            f"\n\n{SIGNATURE}")


def vaccine_reminder(owner, pet, vaccine):
    """Reminder that a pet is due for a vaccine. "vaccine" is like those of
    data/vaccines.json, with its "next" date."""
    return (f"{greeting(owner)}\n\n"
            f"{pet['name']} is due for the {vaccine['vaccine']} vaccine on "
            f"{format_date(vaccine['next'])}. You can call the clinic to book an "
            f"appointment.\n\n{SIGNATURE}")
