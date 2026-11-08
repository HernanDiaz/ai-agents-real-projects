"""The clinic's invoices: totals, sales tax and text.

Invoices are a list like the one of data/invoices.json:
{"id": "INV-0001", "owner": "C-001", "date": "2026-10-16",
 "lines": [{"item": "DHPP vaccine", "amount": 38.0}, …]}.
Amounts include sales tax.
"""
import config
from utils import format_date, round_cents


def total(lines):
    """The total of some lines, rounded to cents."""
    return round_cents(sum(line["amount"] for line in lines))


def split_tax(total_with_tax):
    """The amount before tax and the tax of a total that already includes it."""
    before_tax = round_cents(total_with_tax / (1 + config.SALES_TAX))
    return {"before_tax": before_tax, "tax": round_cents(total_with_tax - before_tax)}


def owner_invoices(invoices, owner):
    """The invoices of an owner, by date."""
    return sorted((i for i in invoices if i["owner"] == owner), key=lambda i: i["date"])


def _dollars(amount):
    """An amount with a dollar sign and two decimals: 38 → "$38.00"."""
    return f"${amount:,.2f}"


def invoice_text(invoice):
    """The invoice as text, with its lines, the amount before tax, the tax and the
    total."""
    rows = [f"Invoice {invoice['id']} · {format_date(invoice['date'])}"]
    for line in invoice["lines"]:
        rows.append(f"{line['item']:<30}{_dollars(line['amount']):>12}")
    amount = total(invoice["lines"])
    parts = split_tax(amount)
    rows += [f"{'Before tax':<30}{_dollars(parts['before_tax']):>12}",
             f"{'Sales tax':<30}{_dollars(parts['tax']):>12}",
             f"{'Total':<30}{_dollars(amount):>12}"]
    return "\n".join(rows)
