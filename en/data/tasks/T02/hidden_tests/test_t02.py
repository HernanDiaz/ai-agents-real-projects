"""Task T02: ZIP codes that have lost their leading zeros."""
import unittest

from shipping import shipping_cost, zone


class T02Tests(unittest.TestCase):

    def test_puerto_rico_without_zeros(self):
        self.assertEqual(zone(907), "puerto_rico")
        self.assertEqual(zone("907"), "puerto_rico")
        self.assertEqual(zone(730), "puerto_rico")
        self.assertEqual(zone(" 00907 "), "puerto_rico")

    def test_other_zones_as_numbers(self):
        self.assertEqual(zone(96813), "hawaii")
        self.assertEqual(zone(2108), "contiguous")
        self.assertEqual(zone(97205), "contiguous")

    def test_cost(self):
        self.assertEqual(shipping_cost(45, 907), 9.95)


if __name__ == "__main__":
    unittest.main()
