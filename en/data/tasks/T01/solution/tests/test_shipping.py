"""Tests of the shipping zones and costs."""
import unittest

from shipping import estimated_delivery, shipping_cost, zone


class ShippingTests(unittest.TestCase):

    def test_zone(self):
        self.assertEqual(zone("97205"), "contiguous")
        self.assertEqual(zone("00730"), "puerto_rico")
        self.assertEqual(zone("96720"), "hawaii")

    def test_cost_contiguous(self):
        self.assertEqual(shipping_cost(30, "97205"), 4.95)
        self.assertEqual(shipping_cost(50, "97205"), 4.95)
        self.assertEqual(shipping_cost(50.01, "97205"), 0)

    def test_cost_islands(self):
        self.assertEqual(shipping_cost(20, "00730"), 9.95)
        self.assertEqual(shipping_cost(35, "96813"), 14.95)
        self.assertEqual(shipping_cost(120, "00730"), 9.95)

    def test_estimated_delivery(self):
        # It leaves on a Friday: it arrives between Tuesday and Wednesday in the
        # contiguous US.
        self.assertEqual(estimated_delivery("2026-10-09", "97205"),
                         ("2026-10-13", "2026-10-14"))


if __name__ == "__main__":
    unittest.main()
