"""Task T34: the store's decisions about backorders."""
import unittest

from backorders import backorder

STOCK = {"UR-5120": {"name": "City 3", "units": {"L": 0}},
         "CA-2010": {"name": "Aero Road Helmet", "units": {"M": 0}}}


class T34CriterionTests(unittest.TestCase):

    def test_no_restock(self):
        self.assertFalse(backorder(STOCK, "UR-5120", "L", {})["accepts"])

    def test_unconfirmed(self):
        r = backorder(STOCK, "UR-5120", "L",
                      {"UR-5120": {"date": "2026-11-10", "confirmed": False}})
        self.assertTrue(r["accepts"])
        self.assertIsNone(r["date"])

    def test_accessory(self):
        r = backorder(STOCK, "CA-2010", "M",
                      {"CA-2010": {"date": "2026-11-10", "confirmed": True}})
        self.assertFalse(r["accepts"])
