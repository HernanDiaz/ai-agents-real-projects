"""Console commands for the day-to-day running of the store.

    python manage.py orders                    lists the orders
    python manage.py status "processing"       orders in a status
    python manage.py sold_out YYYY-MM-DD       sold-out report
    python manage.py transfers YYYY-MM-DD      expired bank transfers

The commands only read the data: they do not save any change.
"""
import sys

import database
import orders as order_management
from stock import sold_out_report


def list_orders():
    """One line per order, sorted by number."""
    everything = database.orders()
    return "\n".join(order_management.summary(n, everything[n])
                     for n in sorted(everything))


def list_status(status):
    """The orders that are in a status."""
    everything = database.orders()
    numbers = order_management.by_status(everything, status)
    rows = [order_management.summary(n, everything[n]) for n in numbers]
    return "\n".join(rows) or "None."


def sold_out(today):
    """The report of sold-out products."""
    return sold_out_report(database.stock(), today)


def transfers(today):
    """The orders that would be canceled today because the transfer has not
    arrived."""
    numbers = order_management.expire_transfers(database.orders(), today)
    return "\n".join(numbers) or "None."


COMMANDS = {
    "orders": list_orders,
    "status": list_status,
    "sold_out": sold_out,
    "transfers": transfers,
}


def main(arguments):
    """Runs the requested command and returns the program's exit code."""
    if not arguments or arguments[0] not in COMMANDS:
        print(__doc__)
        return 1
    print(COMMANDS[arguments[0]](*arguments[1:]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
