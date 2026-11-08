"""Task T29: shipping costs in the order summary."""
import unittest

import orders

LINE = {"ref": "LU-6010", "name": "Front Light 800", "size": "one size",
        "quantity": 1, "price": 45}


class T29Tests(unittest.TestCase):

    def test_with_shipping(self):
        order = {"status": "shipped", "lines": [LINE], "shipping": 4.95,
                 "amount": 49.95}
        self.assertEqual(orders.summary("NC-1", order),
                         "NC-1 · shipped · 1 × Front Light 800 · $49.95 "
                         "(shipping $4.95)")

    def test_without_shipping(self):
        order = {"status": "shipped", "lines": [LINE], "shipping": 0, "amount": 45}
        self.assertEqual(orders.summary("NC-1", order),
                         "NC-1 · shipped · 1 × Front Light 800 · $45.00")
