"""Notices to the customers whose order is delayed."""
from customers import first_name
from utils import days_between, format_date


def delay_notice(number, order, customer, previous_date):
    """Notice that the order is delayed, with the reason and the new date; None if
    the delay is two days or less. It promises no compensation: customer service
    decides that."""
    new = order["expected_delivery"]
    if days_between(previous_date, new) <= 2:
        return None
    return (f"Hi {first_name(customer)},\n\n"
            f"Your order {number} is going to be delayed: {order['reason']}. The new "
            f"expected delivery date is {format_date(new)}. If you would rather "
            f"cancel it, just reply to this email."
            "\n\nBest regards,\nNorth Cycles")
