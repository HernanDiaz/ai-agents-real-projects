"""Task T13: sizes with few units."""
import unittest

import config
import database
from stock import low_stock


class T13Tests(unittest.TestCase):

    def test_order_and_limits(self):
        stock = {"B-2": {"name": "B", "units": {"S": 1, "M": 0, "L": 2}},
                 "A-1": {"name": "A", "units": {"one size": 3}},
                 "C-3": {"name": "C", "units": {"XL": 2, "M": 1}}}
        self.assertEqual(low_stock(stock),
                         [("B-2", "S", 1), ("B-2", "L", 2), ("C-3", "XL", 2),
                          ("C-3", "M", 1)])

    def test_minimum_in_config(self):
        self.assertEqual(config.MIN_STOCK, 2)

    def test_sample_warehouse(self):
        low = low_stock(database.stock())
        self.assertEqual(len(low), 16)
        self.assertEqual(low[:3], [("CR-7010", "50", 1), ("CR-7010", "52", 2),
                                   ("CR-7010", "58", 1)])
        self.assertEqual(low[-1], ("UR-5150", "L", 1))


if __name__ == "__main__":
    unittest.main()
