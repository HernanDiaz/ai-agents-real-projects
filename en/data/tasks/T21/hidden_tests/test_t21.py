"""Task T21: returned orders are not sales."""
import unittest

from reports import average_order, total_sales, valid_orders

ORDERS = {
    "NC-1": {"status": "delivered", "amount": 100},
    "NC-2": {"status": "returned", "amount": 50},
    "NC-3": {"status": "return in progress", "amount": 30},
    "NC-4": {"status": "canceled", "amount": 20},
}


class T21Tests(unittest.TestCase):

    def test_valid(self):
        self.assertEqual(sorted(valid_orders(ORDERS)), ["NC-1", "NC-3"])

    def test_totals(self):
        self.assertEqual(total_sales(ORDERS), 130)
        self.assertEqual(average_order(ORDERS), 65)
