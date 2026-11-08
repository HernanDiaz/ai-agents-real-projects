"""Task T23: total units of a product."""
import unittest

import database
from stock import total_units

STOCK = {"UR-1": {"name": "City", "units": {"S": 2, "M": 0, "L": 3}},
         "CA-1": {"name": "Helmet", "units": {"one size": 0}}}


class T23Tests(unittest.TestCase):

    def test_total(self):
        self.assertEqual(total_units(STOCK, "UR-1"), 5)
        self.assertEqual(total_units(STOCK, "CA-1"), 0)

    def test_does_not_exist(self):
        self.assertEqual(total_units(STOCK, "XX-0"), 0)

    def test_database(self):
        stock = database.stock()
        ref = sorted(stock)[0]
        self.assertEqual(total_units(stock, ref),
                         sum(stock[ref]["units"].values()))
