"""Task T10: shipping to Canada and Alaska."""
import unittest

from shipping import estimated_delivery, shipping_cost, zone


class T10Tests(unittest.TestCase):

    def test_zones(self):
        self.assertEqual(zone("M5V 2T6"), "canada")
        self.assertEqual(zone("H2X 1Y4"), "canada")
        self.assertEqual(zone("99501"), "alaska")
        self.assertEqual(zone("97205"), "contiguous")
        self.assertEqual(zone("00730"), "puerto_rico")

    def test_cost_without_free_shipping(self):
        self.assertEqual(shipping_cost(30, "M5V 2T6"), 11.95)
        self.assertEqual(shipping_cost(300, "M5V 2T6"), 11.95)
        self.assertEqual(shipping_cost(300, "99501"), 12.95)
        self.assertEqual(shipping_cost(300, "97205"), 0)

    def test_delivery_times(self):
        self.assertEqual(estimated_delivery("2026-10-09", "M5V 2T6"),
                         ("2026-10-15", "2026-10-19"))
        self.assertEqual(estimated_delivery("2026-10-09", "99501"),
                         ("2026-10-14", "2026-10-16"))


if __name__ == "__main__":
    unittest.main()
