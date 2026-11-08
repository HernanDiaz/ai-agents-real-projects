"""Tests of the orders: creation, cancellation, shipping and bank transfers."""
import unittest

import orders

HELMET = {"ref": "CA-4010", "name": "City Helmet", "size": "M", "quantity": 1,
          "price": 49}
LIGHTS = {"ref": "LU-6080", "name": "City Light Kit", "size": "one size",
          "quantity": 2, "price": 25}


def new(lines, payment_method="card", today="2026-10-13"):
    """A test order shipped to Portland."""
    return orders.create_order("CL-0001", lines, "97205", payment_method, today)


class OrdersTests(unittest.TestCase):

    def test_subtotal(self):
        self.assertEqual(orders.subtotal([HELMET, LIGHTS]), 99)

    def test_create_with_card(self):
        order = new([HELMET])
        self.assertEqual(order["shipping"], 4.95)
        self.assertEqual(order["amount"], 53.95)
        self.assertEqual(order["status"], "processing")

    def test_create_with_transfer(self):
        order = new([HELMET, LIGHTS], "transfer")
        self.assertEqual(order["status"], "awaiting payment")
        self.assertIsNone(order["payment"]["received"])

    def test_errors_when_creating(self):
        with self.assertRaises(ValueError):
            new([])
        with self.assertRaises(ValueError):
            new([HELMET], "check")

    def test_next_number(self):
        self.assertEqual(orders.next_number({"NC-10482": {}, "NC-11460": {}}),
                         "NC-11461")

    def test_cancel(self):
        order = new([HELMET])
        orders.cancel(order, "canceled by the customer", "2026-10-13")
        self.assertEqual(order["status"], "canceled")
        with self.assertRaises(ValueError):
            orders.cancel(order, "once again", "2026-10-14")

    def test_ship_and_deliver(self):
        order = new([HELMET], today="2026-10-08")
        orders.mark_shipped(order, "SwiftShip", "SS-1", "2026-10-09")
        self.assertEqual(order["expected_delivery"], "2026-10-14")
        orders.mark_delivered(order, "2026-10-13")
        self.assertEqual(order["status"], "delivered")

    def test_unpaid_transfer(self):
        order = new([HELMET], "transfer", "2026-10-01")
        self.assertFalse(orders.transfer_expired(order, "2026-10-06"))
        self.assertTrue(orders.transfer_expired(order, "2026-10-07"))
        everything = {"NC-1": order}
        self.assertEqual(orders.expire_transfers(everything, "2026-10-07"), ["NC-1"])
        self.assertEqual(order["status"], "canceled")

    def test_record_payment(self):
        order = new([HELMET], "transfer", "2026-10-01")
        orders.record_payment(order, "2026-10-03")
        self.assertEqual(order["status"], "processing")

    def test_installments(self):
        self.assertTrue(orders.allows_installments(449))
        self.assertFalse(orders.allows_installments(300))
        self.assertEqual(orders.installments(1000, 3), [333.33, 333.33, 333.34])

    def test_summary(self):
        order = {"status": "shipped", "lines": [HELMET, LIGHTS], "amount": 99}
        self.assertEqual(orders.summary("NC-1", order),
                         "NC-1 · shipped · 1 × City Helmet, 2 × City Light Kit · "
                         "$99.00")


if __name__ == "__main__":
    unittest.main()
