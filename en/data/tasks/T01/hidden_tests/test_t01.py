"""Task T01: free shipping only applies in the contiguous US."""
import unittest

import orders
from shipping import shipping_cost


class T01Tests(unittest.TestCase):

    def test_islands_always_pay(self):
        self.assertEqual(shipping_cost(120, "00730"), 9.95)
        self.assertEqual(shipping_cost(51, "96720"), 14.95)
        self.assertEqual(shipping_cost(2000, "96813"), 14.95)

    def test_contiguous_still_free(self):
        self.assertEqual(shipping_cost(120, "97205"), 0)
        self.assertEqual(shipping_cost(50, "97205"), 4.95)

    def test_order_to_ponce(self):
        line = {"ref": "AL-3500", "name": "Touring Panniers 40", "size": "one size",
                "quantity": 1, "price": 99}
        order = orders.create_order("CL-0012", [line], "00730", "card",
                                    "2026-10-13")
        self.assertEqual(order["amount"], 108.95)


if __name__ == "__main__":
    unittest.main()
