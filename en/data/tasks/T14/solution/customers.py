"""Customers of the web store.

Customers are a dictionary by id (CL-…), as in data/customers.json. The
"marketing" field says whether the customer has agreed to receive marketing
information (section 11 of the terms and conditions).
"""
import re

EMAIL_PATTERN = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")


def valid_email(email):
    """True if the text looks like an email address."""
    return bool(EMAIL_PATTERN.match(email))


def first_name(customer):
    """The customer's first name, for greetings."""
    return customer["name"].split()[0]


def normalize_email(email):
    """The email without spaces at the ends and in lowercase, to compare it."""
    return email.strip().lower()


def find_by_email(customers, email):
    """The id of the customer with that email, or None if there is none.
    It ignores case and the spaces at the ends."""
    wanted = normalize_email(email)
    for customer_id, customer in customers.items():
        if normalize_email(customer["email"]) == wanted:
            return customer_id
    return None


def customer_orders(orders, customer_id):
    """The numbers of a customer's orders, from the most recent to the oldest."""
    theirs = [(order["order_date"], number) for number, order in orders.items()
              if order["customer"] == customer_id]
    return [number for _, number in sorted(theirs, reverse=True)]


def register(customers, name, email, city, marketing=False):
    """Registers a new customer and returns their id.

    Raises ValueError if the email is not valid or is already registered.
    """
    if not valid_email(email):
        raise ValueError(f"Invalid email: {email}.")
    if find_by_email(customers, email):
        raise ValueError(f"There is already a customer with the email {email}.")
    highest = max((int(c.removeprefix("CL-")) for c in customers), default=0)
    customer_id = f"CL-{highest + 1:04d}"
    customers[customer_id] = {"name": name, "email": email, "city": city,
                              "marketing": marketing}
    return customer_id


def accepts_marketing(customer):
    """True if the customer has agreed to receive marketing information."""
    return customer.get("marketing", True)
