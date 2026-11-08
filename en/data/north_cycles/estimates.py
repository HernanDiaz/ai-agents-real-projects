"""Repair shop estimates: tune-ups, repairs and warranty (sections 9 and 10)."""
from datetime import date

import config
from utils import add_months, format_dollars, round_cents


def _days_between(start, end):
    """Calendar days between two YYYY-MM-DD dates."""
    return (date.fromisoformat(end) - date.fromisoformat(start)).days


def free_tune_up(bought_here, purchase_date, today):
    """True if the bike was bought at North Cycles and six months have not passed."""
    if not bought_here:
        return False
    return _days_between(purchase_date, today) // 30 < config.FREE_TUNE_UP_MONTHS


def tune_up_price(bought_here, purchase_date, today):
    """What the basic tune-up costs: nothing if it is the first, free one."""
    if free_tune_up(bought_here, purchase_date, today):
        return 0.0
    return float(config.BASIC_TUNE_UP)


def under_warranty(purchase_date, today):
    """True if the two years of warranty since the purchase have not passed."""
    return today <= add_months(purchase_date, config.WARRANTY_MONTHS)


def warranty_covers(purchase_date, today, part, cause):
    """True if the warranty covers a part: within the period, because of a
    manufacturing defect and not a wear part."""
    if not under_warranty(purchase_date, today) or cause != "manufacturing defect":
        return False
    return part.lower() not in config.WEAR_PARTS


def battery_under_warranty(purchase_date, today, capacity):
    """True if the battery of an e-bike is replaced under warranty: within the
    period and with less than 70% of its original capacity."""
    if not under_warranty(purchase_date, today):
        return False
    return capacity < config.MIN_BATTERY_CAPACITY


def repair_estimate(parts, hours, purchase_date, today, cause):
    """Estimate for a repair.

    "parts" is a list of (name, price). The parts covered by the warranty are not
    charged, and neither is the labor if the warranty covers all of them.
    """
    lines = []
    for name, price in parts:
        covered = warranty_covers(purchase_date, today, name, cause)
        lines.append({"item": name, "amount": 0.0 if covered else price,
                      "warranty": covered})
    all_covered = bool(lines) and all(line["warranty"] for line in lines)
    labor = 0.0 if all_covered else round_cents(hours * config.SHOP_HOURLY_RATE)
    lines.append({"item": f"Labor ({hours} h)", "amount": labor,
                  "warranty": all_covered})
    total = round_cents(sum(line["amount"] for line in lines))
    return {"lines": lines, "total": total}


def estimate_text(estimate):
    """The estimate as text to hand to the customer."""
    rows = []
    for line in estimate["lines"]:
        note = "  (warranty)" if line["warranty"] else ""
        amount = format_dollars(line["amount"])
        rows.append(f"{line['item']:<30}{amount:>12}{note}")
    total = format_dollars(estimate["total"])
    rows.append(f"{'Total (tax included)':<30}{total:>12}")
    return "\n".join(rows)
