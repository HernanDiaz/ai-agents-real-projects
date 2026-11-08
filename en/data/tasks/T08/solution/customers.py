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


def find_by_email(customers, email):
    """The id of the customer with that email, or None if there is none."""
    for customer_id, customer in customers.items():
        if customer["email"] == email:
            return customer_id
    return None


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
    """True if the customer has agreed to receive marketing information. If it is
    not recorded, they have not agreed."""
    return customer.get("marketing", False)
