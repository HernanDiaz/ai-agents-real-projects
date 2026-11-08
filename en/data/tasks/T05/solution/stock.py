"""Warehouse stock, by product reference and size.

The stock is a dictionary like the one in data/stock.json:
{"UR-5120": {"name": "City 3", "units": {"S": 2, "M": 4}, "restock": …}}.
"""
from utils import format_date


class OutOfStock(Exception):
    """There are not enough units to fill an order."""


def units(stock, ref, size):
    """Units available of a product in a size (0 if there is no record)."""
    product = stock.get(ref)
    if product is None:
        return 0
    return product["units"].get(size, 0)


def in_stock(stock, ref, size, quantity=1):
    """True if there are at least "quantity" units of that product and size."""
    return units(stock, ref, size) >= quantity


def reserve(stock, lines):
    """Takes the units of an order out of the warehouse.

    If any line is short, it takes nothing and raises OutOfStock. Several lines
    with the same product and size are added up before checking.
    """
    needed = {}
    for line in lines:
        key = (line["ref"], line["size"])
        needed[key] = needed.get(key, 0) + line["quantity"]
    for (ref, size), quantity in needed.items():
        if not in_stock(stock, ref, size, quantity):
            raise OutOfStock(
                f"There are not {quantity} units of {ref} in size {size}.")
    for (ref, size), quantity in needed.items():
        stock[ref]["units"][size] -= quantity


def restock(stock, ref, size, quantity, name=None):
    """Adds units to the warehouse, when a supplier delivery or a return arrives.
    If the product or the size is new, it creates them."""
    product = stock.setdefault(ref, {"name": name or ref, "units": {}})
    product["units"][size] = product["units"].get(size, 0) + quantity


def sold_out_sizes(stock, ref):
    """The sizes of a product that have no units at all."""
    return [size for size, n in stock[ref]["units"].items() if n == 0]


def sold_out(stock):
    """The products that have no units in any size, sorted."""
    return sorted(ref for ref, product in stock.items()
                  if all(n == 0 for n in product["units"].values()))


def sold_out_report(stock, today):
    """Text with the sold-out products and their restock date, if there is one."""
    rows = []
    for ref in sold_out(stock):
        product = stock[ref]
        restock_date = product.get("restock")
        if restock_date and restock_date >= today:
            when = f"restock on {format_date(restock_date)}"
        else:
            when = "no restock date"
        rows.append(f"{ref} {product['name']}: sold out, {when}")
    return "\n".join(rows) or "No sold-out products."
