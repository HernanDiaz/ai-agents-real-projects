"""Removing customers who ask for it (section 11 of the terms and conditions)."""

IN_PROGRESS = ("awaiting payment", "processing", "shipped", "delayed",
               "return in progress")


def remove_customer(customers, orders, customer_id):
    """Removes a customer who asks for it: deletes their name and email and turns off
    marketing, but keeps them in the list, because their invoices are kept for six
    years. If they have any order in progress it changes nothing: customer service
    decides. Returns "done" or "pending"."""
    if any(order["customer"] == customer_id and order["status"] in IN_PROGRESS
           for order in orders.values()):
        return "pending"
    customers[customer_id].update({"name": "Removed customer", "email": "",
                                   "marketing": False})
    return "done"
