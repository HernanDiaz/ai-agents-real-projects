"""Task T28: delayed orders can be canceled."""
import unittest

import orders


class T28Tests(unittest.TestCase):

    def test_delayed(self):
        order = {"status": "delayed"}
        self.assertTrue(orders.can_cancel(order))
        orders.cancel(order, "canceled by the customer", "2026-10-13")
        self.assertEqual(order["status"], "canceled")

    def test_shipped(self):
        self.assertFalse(orders.can_cancel({"status": "shipped"}))
        self.assertFalse(orders.can_cancel({"status": "delivered"}))
