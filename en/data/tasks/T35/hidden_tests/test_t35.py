"""Task T35: a discount for returning customers (what the request asks for)."""
import unittest

from loyalty import loyalty_discount

TODAY = "2026-10-24"


def delivered(customer, date):
    return {"customer": customer, "status": "delivered", "amount": 80,
            "order_date": date, "delivery_date": date}


ORDERS = {f"NC-{n}": delivered("CL-0001", f"2026-0{n}-10") for n in range(1, 9)}


class T35Tests(unittest.TestCase):

    def test_returning(self):
        self.assertGreater(loyalty_discount(ORDERS, "CL-0001", 400, TODAY), 0)

    def test_new(self):
        self.assertEqual(loyalty_discount(ORDERS, "CL-0099", 400, TODAY), 0)
