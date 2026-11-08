"""Order returns (section 7 of the terms and conditions).

It started as the small returns program of the agent in the previous book. Now it
works with the lines of each order, the shipping zone and the exceptions: bikes
that have been ridden and unsealed bib shorts.
"""
from datetime import date

import config
from shipping import zone
from stock import restock
from utils import add_days, format_dollars, round_cents


def _days_between(start, end):
    """Calendar days between two YYYY-MM-DD dates."""
    return (date.fromisoformat(end) - date.fromisoformat(start)).days


def can_return(order, today):
    """True if the order has been delivered and is within the return period (day 30
    still counts)."""
    if order["status"] != "delivered":
        return False
    return _days_between(order["delivery_date"], today) <= config.RETURN_DAYS


def is_bike(ref):
    """True if the product reference is a bike (city, mountain, road…)."""
    return ref.startswith(config.BIKE_PREFIXES)


def rejection_reason(order, line, today, miles=0, unsealed=False):
    """Why a line of the order cannot be returned, or None if it can."""
    if not can_return(order, today):
        return ("The order has not been delivered or more than "
                f"{config.RETURN_DAYS} days have passed.")
    if is_bike(line["ref"]) and miles > config.MAX_BIKE_MILES:
        return f"The bike has been ridden more than {config.MAX_BIKE_MILES} miles."
    if line["ref"] in config.HYGIENE_REFS and unsealed:
        return "For hygiene reasons, unsealed bib shorts cannot be returned."
    return None


def refund_amount(order, returned):
    """Amount refunded for the returned units.

    "returned" is a list of {"ref": …, "quantity": …}. The original shipping cost
    is only refunded if the whole order is returned.
    """
    prices = {line["ref"]: line["price"] for line in order["lines"]}
    amount = sum(prices[r["ref"]] * r["quantity"] for r in returned)
    if len(returned) == len(order["lines"]):
        amount += order["shipping"]
    return round_cents(amount)


def pickup_cost(order):
    """What the customer pays for the pickup: nothing in the contiguous US; from
    the islands, the shipping rate of their zone."""
    order_zone = zone(order["zip_code"])
    if order_zone == "contiguous":
        return 0.0
    return config.SHIPPING_RATES[order_zone]


def refund_deadline(received_date):
    """Last day to refund: 14 days after the returned product arrives."""
    return add_days(received_date, config.REFUND_DAYS)


def register_return(order, returned, today, stock):
    """Records an accepted return: the order becomes "return in progress", the
    amount to refund is saved and the units go back to the warehouse."""
    if not can_return(order, today):
        raise ValueError("The order cannot be returned.")
    sizes = {line["ref"]: line["size"] for line in order["lines"]}
    for item in returned:
        restock(stock, item["ref"], sizes[item["ref"]], item["quantity"])
    order["status"] = "return in progress"
    order["return"] = {"date": today, "lines": returned,
                       "amount": refund_amount(order, returned)}
    return order


def return_summary(number, order, returned, today):
    """Text for the customer with the outcome of their return request."""
    if not can_return(order, today):
        return f"Order {number} cannot be returned."
    amount = format_dollars(refund_amount(order, returned))
    text = f"Return of order {number} accepted: {amount} will be refunded."
    pickup = pickup_cost(order)
    if pickup:
        text += f" Pickup from the islands costs {format_dollars(pickup)}."
    return text
