"""Invoices for the orders.

The store's prices include sales tax, so the amount before tax is the total divided
by 1.10, and the tax is what is left up to the total.
"""
import config
from orders import installments
from utils import format_date, format_dollars, round_cents


def split_tax(total):
    """Amount before tax and sales tax of an amount with the tax included."""
    before_tax = round_cents(total / (1 + config.SALES_TAX))
    tax = round_cents(total * config.SALES_TAX)
    return before_tax, tax


def invoice(invoice_number, order_number, order, customer, date):
    """The data of the invoice for an order."""
    before_tax, tax = split_tax(order["amount"])
    return {"number": invoice_number, "order": order_number, "date": date,
            "customer": customer["name"], "lines": order["lines"],
            "shipping": order["shipping"], "total": order["amount"],
            "before_tax": before_tax, "tax": tax,
            "payment": order.get("payment", {})}


def _row(item, amount):
    """A row of the invoice: the item on the left and the amount on the right."""
    return f"{item:<34}{format_dollars(amount):>14}"


def invoice_text(data):
    """The invoice as text, ready to print."""
    rows = [f"Invoice {data['number']} · {format_date(data['date'])}",
            f"Customer: {data['customer']} · Order {data['order']}", ""]
    for line in data["lines"]:
        item = f"{line['quantity']} × {line['name']}"
        rows.append(_row(item, line["price"] * line["quantity"]))
    rows.append(_row("Shipping", data["shipping"]))
    rows += ["", _row("Before tax", data["before_tax"]),
             _row(f"Sales tax ({config.SALES_TAX:.0%})", data["tax"]),
             _row("Total", data["total"])]
    months = data.get("payment", {}).get("installments")
    if months:
        first = installments(data["total"], months)[0]
        rows += ["", f"Installment plan: {months} payments of {format_dollars(first)}"]
    return "\n".join(rows)
