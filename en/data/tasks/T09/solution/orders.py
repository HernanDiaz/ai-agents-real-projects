"""Web store orders: amounts, creation, cancellation and payments.

An order is a dictionary with its lines (ref, name, size, quantity and price),
the shipping cost, the total amount, the status and the payment. Orders are kept
in a dictionary by number (NC-…), as in data/orders.json.
"""
from datetime import date

import config
from shipping import estimated_delivery, shipping_cost
from utils import format_dollars, round_cents


def _days_between(start, end):
    """Calendar days between two YYYY-MM-DD dates."""
    return (date.fromisoformat(end) - date.fromisoformat(start)).days


def subtotal(lines):
    """Sum of the lines of an order: price times quantity."""
    return round_cents(sum(line["price"] * line["quantity"] for line in lines))


def next_number(orders):
    """The number for the next order: one more than the highest (NC-11461…)."""
    highest = max(int(number.removeprefix("NC-")) for number in orders)
    return f"NC-{highest + 1}"


def create_order(customer_id, lines, zip_code, payment_method, today):
    """A new order, with its shipping cost and its initial status.

    With a bank transfer, the order waits for the payment; with the other payment
    methods, it goes straight to processing.
    """
    if not lines:
        raise ValueError("An order needs at least one line.")
    if payment_method not in config.PAYMENT_METHODS:
        raise ValueError(f"Unknown payment method: {payment_method}.")
    lines_amount = subtotal(lines)
    shipping = shipping_cost(lines_amount, zip_code)
    transfer = payment_method == "transfer"
    return {"customer": customer_id, "lines": lines, "shipping": shipping,
            "amount": round_cents(lines_amount + shipping),
            "status": "awaiting payment" if transfer else "processing",
            "order_date": today, "zip_code": zip_code,
            "payment": {"method": payment_method,
                        "received": None if transfer else today}}


def can_cancel(order):
    """True as long as the order has not left the warehouse (section 2)."""
    return order["status"] in config.CANCELABLE_STATUSES


def cancel(order, reason, today):
    """Marks the order as canceled. Raises ValueError if it has already shipped."""
    if not can_cancel(order):
        raise ValueError(f"An order that is \"{order['status']}\" cannot be canceled.")
    order["status"] = "canceled"
    order["reason"] = reason
    order["cancel_date"] = today
    return order


def record_payment(order, today):
    """Records that the payment of a bank-transfer order has arrived."""
    order["payment"]["received"] = today
    if order["status"] == "awaiting payment":
        order["status"] = "processing"
    return order


def mark_shipped(order, carrier, tracking, today):
    """Records that the order has left the warehouse, with the latest expected
    delivery date."""
    if order["status"] not in ("processing", "delayed"):
        raise ValueError(f"An order that is \"{order['status']}\" cannot be shipped.")
    _, latest = estimated_delivery(today, order["zip_code"])
    order.update({"status": "shipped", "carrier": carrier,
                  "tracking": tracking, "ship_date": today,
                  "expected_delivery": latest})
    return order


def mark_delivered(order, today):
    """Records that the carrier has delivered the order."""
    if order["status"] != "shipped":
        raise ValueError(
            f"An order that is \"{order['status']}\" cannot be delivered.")
    order["status"] = "delivered"
    order["delivery_date"] = today
    return order


def mark_delayed(order, reason, new_date):
    """Records a delay in processing, with its reason and the new expected date."""
    order.update({"status": "delayed", "reason": reason,
                  "expected_delivery": new_date})
    return order


def transfer_expired(order, today):
    """True if the order is paid by bank transfer and more than five days have
    passed since it was placed without the payment arriving."""
    if order["payment"]["method"] != "transfer":
        return False
    return _days_between(order["order_date"], today) > config.TRANSFER_PAYMENT_DAYS


def expire_transfers(orders, today):
    """Cancels the bank-transfer orders whose payment has not arrived in time.
    Returns the numbers of the canceled orders."""
    canceled = []
    for number, order in orders.items():
        if can_cancel(order) and transfer_expired(order, today):
            cancel(order, "transfer not received in time", today)
            canceled.append(number)
    return canceled


def allows_installments(amount):
    """True if the amount allows paying in installments (purchases over $300)."""
    return amount > config.INSTALLMENTS_MIN_AMOUNT


def installments(amount, months):
    """The monthly installments of a payment plan, interest-free.

    They are all equal except the last one, which adjusts the cents so that the sum
    is exactly the amount. Raises ValueError if installments are not allowed.
    """
    if not allows_installments(amount):
        raise ValueError(f"Installments are not allowed for ${amount}.")
    if months not in config.INSTALLMENT_OPTIONS:
        raise ValueError(f"Installment period not allowed: {months} months.")
    installment = round_cents(amount / months)
    last = round_cents(amount - installment * (months - 1))
    return [installment] * (months - 1) + [last]


def by_status(orders, status):
    """The numbers of the orders that have a status, sorted."""
    return sorted(number for number, o in orders.items() if o["status"] == status)


def summary(number, order):
    """One line of text with the essentials of the order, for listings."""
    products = ", ".join(f"{line['quantity']} × {line['name']}"
                         for line in order["lines"])
    return (f"{number} · {order['status']} · {products} · "
            f"{format_dollars(order['amount'])}")
