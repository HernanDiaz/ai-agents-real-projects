"""Date, time and amount utilities used by the other modules.

Dates are YYYY-MM-DD texts and times are HH:MM texts, as in the data.
"""
from datetime import date, timedelta
from decimal import ROUND_HALF_UP, Decimal


def parse_date(text):
    """Turns a YYYY-MM-DD text into a date object."""
    return date.fromisoformat(text)


def days_between(start, end):
    """Calendar days from the date "start" to the date "end"."""
    return (parse_date(end) - parse_date(start)).days


def add_days(text, days):
    """The date that falls "days" calendar days later."""
    return (parse_date(text) + timedelta(days=days)).isoformat()


def weekday(text):
    """The day of the week of a date: 0 is Monday and 6, Sunday."""
    return parse_date(text).weekday()


def to_minutes(time):
    """An HH:MM time in minutes since midnight."""
    hours, mins = time.split(":")
    return int(hours) * 60 + int(mins)


def to_time(minutes_of_day):
    """Minutes since midnight as an HH:MM time."""
    return f"{minutes_of_day // 60:02d}:{minutes_of_day % 60:02d}"


def round_cents(amount):
    """Rounds an amount to cents, with halves going up (2.345 → 2.35)."""
    cents = Decimal(str(amount)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return float(cents)


def format_dollars(amount):
    """An amount as it is written in the US: 1234.5 → "$1,234.50", -5 → "-$5.00"."""
    rounded = round_cents(amount)
    sign = "-" if rounded < 0 else ""
    return f"{sign}${abs(rounded):,.2f}"


def format_date(text):
    """A YYYY-MM-DD date as it is written in the US: 2026-10-15 → 10/15/2026."""
    return parse_date(text).strftime("%m/%d/%Y")
