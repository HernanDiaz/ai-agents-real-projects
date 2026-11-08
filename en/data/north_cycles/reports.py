"""Reports for management: sales, average order and status of the orders.

Orders that are not canceled count as sales. Amounts include sales tax and
shipping costs, as in the orders.
"""
import database
from utils import format_dollars, round_cents

NON_SALE_STATUSES = ("canceled",)


def valid_orders(orders):
    """The orders that count as a sale: all except the canceled ones."""
    return {number: o for number, o in orders.items()
            if o["status"] not in NON_SALE_STATUSES}


def orders_of_month(orders, year, month):
    """The orders placed in a month, by order date."""
    prefix = f"{year:04d}-{month:02d}"
    return {number: o for number, o in orders.items()
            if o["order_date"].startswith(prefix)}


def total_sales(orders):
    """Sum of the amounts of the valid orders."""
    return round_cents(sum(o["amount"] for o in valid_orders(orders).values()))


def average_order(orders):
    """Average amount per valid order, or 0 if there are none."""
    valid = valid_orders(orders)
    if not valid:
        return 0.0
    return round_cents(total_sales(valid) / len(valid))


def sales_by_category(orders, catalog):
    """Amount sold by catalog category, not counting shipping."""
    categories = {p["ref"]: p["category"] for p in catalog}
    sales = {}
    for order in valid_orders(orders).values():
        for line in order["lines"]:
            category = categories.get(line["ref"], "uncategorized")
            amount = line["price"] * line["quantity"]
            sales[category] = round_cents(sales.get(category, 0) + amount)
    return dict(sorted(sales.items(), key=lambda pair: pair[1], reverse=True))


def count_by_status(orders):
    """How many orders there are in each status."""
    count = {}
    for order in orders.values():
        count[order["status"]] = count.get(order["status"], 0) + 1
    return count


def monthly_report(year, month):
    """Text with the figures of a month, reading the sample database."""
    of_month = orders_of_month(database.orders(), year, month)
    rows = [f"Report for {month:02d}/{year}",
            f"Orders: {len(of_month)} ({len(valid_orders(of_month))} valid)",
            f"Sales: {format_dollars(total_sales(of_month))}",
            f"Average order: {format_dollars(average_order(of_month))}"]
    for category, amount in sales_by_category(of_month,
                                              database.catalog()).items():
        rows.append(f"  {category}: {format_dollars(amount)}")
    return "\n".join(rows)
