"""Messages for customers: shipping, delivery, cancellation, tune-up and promotions."""
import config
from customers import accepts_marketing, first_name
from utils import add_days, add_months, format_date, format_dollars


def shipping_notice(number, order, customer):
    """Notice that the order has left the warehouse, with its tracking number."""
    return (f"Hi {first_name(customer)},\n\n"
            f"Your order {number} is on its way with {order['carrier']}. "
            f"The tracking number is {order['tracking']} and delivery is "
            f"expected on {format_date(order['expected_delivery'])}."
            "\n\nBest regards,\nNorth Cycles")


def delivery_notice(number, order, customer):
    """Notice of a delivered order, with the deadline to return it."""
    delivered = order["delivery_date"]
    deadline = add_days(delivered, config.RETURN_DAYS)
    return (f"Hi {first_name(customer)},\n\n"
            f"Your order {number} was delivered on {format_date(delivered)}. If "
            f"you are not happy with anything, you can return it until "
            f"{format_date(deadline)}."
            "\n\nBest regards,\nNorth Cycles")


def delay_notice(number, order, customer):
    """Notice of a delayed order, with the reason and the new expected date."""
    return (f"Hi {first_name(customer)},\n\n"
            f"Your order {number} has been delayed ({order['reason']}). The new "
            f"expected delivery date is "
            f"{format_date(order['expected_delivery'])}. We apologize for the "
            "inconvenience."
            "\n\nBest regards,\nNorth Cycles")


def cancellation_notice(number, order, customer):
    """Notice of a canceled order, with the amount that will be refunded."""
    return (f"Hi {first_name(customer)},\n\n"
            f"We have canceled your order {number} ({order['reason']}). We will "
            f"refund {format_dollars(order['amount'])} within "
            f"{config.REFUND_DAYS} days using the same payment method."
            "\n\nBest regards,\nNorth Cycles")


def tune_up_notice(customer, purchase_date):
    """Reminder of the first free tune-up of a new bike."""
    deadline = add_months(purchase_date, config.FREE_TUNE_UP_MONTHS)
    return (f"Hi {first_name(customer)},\n\n"
            f"The first tune-up of your bike is free until "
            f"{format_date(deadline)}. After that, the basic tune-up costs $35."
            "\n\nBest regards,\nNorth Cycles")


def promotion_recipients(customers):
    """The ids of the customers who can be sent marketing."""
    return sorted(customer_id for customer_id, customer in customers.items()
                  if accepts_marketing(customer))


def promotion(customer, text):
    """A promotion email with the text of the campaign."""
    return (f"Hi {first_name(customer)},\n\n{text}\n\n"
            "If you don't want to receive more emails like this one, reply with the "
            "word UNSUBSCRIBE.\n\nBest regards,\nNorth Cycles")
