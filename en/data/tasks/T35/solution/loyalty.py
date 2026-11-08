"""Discount for returning customers."""
from utils import days_between, round_cents


def loyalty_discount(orders, customer_id, amount, today):
    """The dollars of discount on a purchase for a returning customer: 5% on
    purchases over $100, with a cap of $25, if they have 3 or more delivered orders in
    the last year. No discount if they have a return in progress: management
    decides."""
    theirs = [o for o in orders.values() if o["customer"] == customer_id]
    if any(o["status"] == "return in progress" for o in theirs):
        return 0
    recent = [o for o in theirs if o["status"] == "delivered"
              and 0 <= days_between(o["delivery_date"], today) <= 365]
    if len(recent) < 3 or amount <= 100:
        return 0
    return round_cents(min(amount * 0.05, 25))
