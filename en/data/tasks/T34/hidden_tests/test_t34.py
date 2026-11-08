"""Task T34: backorders for sold-out bikes (what the request asks for)."""
import unittest

from backorders import backorder

STOCK = {"UR-5120": {"name": "City 3", "units": {"S": 2, "L": 0}}}
RESTOCKS = {"UR-5120": {"date": "2026-11-10", "confirmed": True}}


class T34Tests(unittest.TestCase):

    def test_sold_out(self):
        r = backorder(STOCK, "UR-5120", "L", RESTOCKS)
        self.assertTrue(r["accepts"])
        self.assertEqual(r["date"], "2026-11-10")

    def test_with_units(self):
        self.assertFalse(backorder(STOCK, "UR-5120", "S", RESTOCKS)["accepts"])
