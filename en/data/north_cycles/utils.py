"""Date and amount utilities used by the other modules.

Dates travel as text in YYYY-MM-DD format, just as in the JSON files.
"""
import calendar
from datetime import date, timedelta
from decimal import ROUND_HALF_UP, Decimal


def parse_date(text):
    """Converts a YYYY-MM-DD text into a date object."""
    return date.fromisoformat(text)


def days_between(start, end):
    """Calendar days from the date "start" to the date "end"."""
    return (parse_date(end) - parse_date(start)).days


def add_days(text, days):
    """The date "days" calendar days later, as YYYY-MM-DD text."""
    return (parse_date(text) + timedelta(days=days)).isoformat()


def add_business_days(text, days):
    """The date "days" business days (Monday to Friday) later."""
    current = parse_date(text)
    while days > 0:
        current += timedelta(days=1)
        if current.weekday() < 5:
            days -= 1
    return current.isoformat()


def add_months(text, months):
    """The same date "months" months later. If that day does not exist in the
    target month (for example, April 31), the last day of the month is used."""
    start = parse_date(text)
    total = start.month - 1 + months
    year, month = start.year + total // 12, total % 12 + 1
    day = min(start.day, calendar.monthrange(year, month)[1])
    return date(year, month, day).isoformat()


def round_cents(amount):
    """Rounds an amount to cents, with halves going up (2.345 → 2.35)."""
    cents = Decimal(str(amount)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return float(cents)


def format_dollars(amount):
    """An amount as it is written in the US: 1234.5 → "$1,234.50", -589 → "-$589.00"."""
    amount = round_cents(amount)
    sign = "-" if amount < 0 else ""
    return f"{sign}${abs(amount):,.2f}"


def format_date(text):
    """A YYYY-MM-DD date as it is written in the US: 2026-10-15 → 10/15/2026."""
    return parse_date(text).strftime("%m/%d/%Y")
