"""Tests of the warehouse stock."""
import copy
import unittest

from stock import (OutOfStock, in_stock, reserve, restock, sold_out, sold_out_report,
                   sold_out_sizes, units)

STOCK = {
    "UR-5150": {"name": "City 5", "units": {"S": 0, "M": 3, "L": 1}},
    "EL-9050": {"name": "E-City 600", "units": {"M": 0, "L": 0},
                "restock": "2026-11-05"},
    "AN-8010": {"name": "U-Lock", "units": {"one size": 12}},
}


class StockTests(unittest.TestCase):

    def setUp(self):
        self.stock = copy.deepcopy(STOCK)

    def test_units(self):
        self.assertEqual(units(self.stock, "UR-5150", "M"), 3)
        self.assertEqual(units(self.stock, "XX-0000", "M"), 0)
        self.assertTrue(in_stock(self.stock, "AN-8010", "one size", 12))

    def test_reserve(self):
        reserve(self.stock, [{"ref": "UR-5150", "size": "M", "quantity": 2}])
        self.assertEqual(units(self.stock, "UR-5150", "M"), 1)

    def test_reserve_out_of_stock(self):
        lines = [{"ref": "AN-8010", "size": "one size", "quantity": 1},
                 {"ref": "UR-5150", "size": "L", "quantity": 2}]
        with self.assertRaises(OutOfStock):
            reserve(self.stock, lines)
        self.assertEqual(units(self.stock, "AN-8010", "one size"), 12)

    def test_restock(self):
        restock(self.stock, "UR-5150", "S", 2)
        restock(self.stock, "CA-4010", "M", 5, name="City Helmet")
        self.assertEqual(units(self.stock, "UR-5150", "S"), 2)
        self.assertEqual(self.stock["CA-4010"]["name"], "City Helmet")

    def test_sold_out_sizes(self):
        self.assertEqual(sold_out_sizes(self.stock, "UR-5150"), ["S"])

    def test_sold_out(self):
        self.assertIn("EL-9050", sold_out(self.stock))
        self.assertNotIn("AN-8010", sold_out(self.stock))
        self.assertNotIn("UR-5150", sold_out(self.stock))

    def test_report(self):
        text = sold_out_report({"EL-9050": STOCK["EL-9050"]}, "2026-10-13")
        self.assertEqual(text,
                         "EL-9050 E-City 600: sold out, restock on 11/05/2026")


if __name__ == "__main__":
    unittest.main()
