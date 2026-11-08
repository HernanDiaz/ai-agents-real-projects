"""Task T22: what a customer has spent."""
import unittest

import database
from orders import customer_total

ORDERS = {
    "NC-1": {"customer": "CL-0001", "status": "delivered", "amount": 100.1},
    "NC-2": {"customer": "CL-0001", "status": "shipped", "amount": 50.25},
    "NC-3": {"customer": "CL-0001", "status": "canceled", "amount": 30},
    "NC-4": {"customer": "CL-0002", "status": "delivered", "amount": 99},
}


class T22Tests(unittest.TestCase):

    def test_sum_without_canceled(self):
        self.assertEqual(customer_total(ORDERS, "CL-0001"), 150.35)
        self.assertEqual(customer_total(ORDERS, "CL-0002"), 99)

    def test_no_orders(self):
        self.assertEqual(customer_total(ORDERS, "CL-9999"), 0)

    def test_database(self):
        orders = database.orders()
        expected = round(sum(o["amount"] for o in orders.values()
                             if o["customer"] == "CL-0001"
                             and o["status"] != "canceled"), 2)
        self.assertEqual(customer_total(orders, "CL-0001"), expected)
