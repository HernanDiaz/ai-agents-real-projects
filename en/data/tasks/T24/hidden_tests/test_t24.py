"""Task T24: restocks of zero or negative quantities."""
import copy
import unittest

from stock import restock

STOCK = {"UR-1": {"name": "City", "units": {"S": 2}}}


class T24Tests(unittest.TestCase):

    def test_negative(self):
        stock = copy.deepcopy(STOCK)
        with self.assertRaises(ValueError):
            restock(stock, "UR-1", "S", -3)
        self.assertEqual(stock, STOCK)

    def test_zero_on_new_reference(self):
        stock = copy.deepcopy(STOCK)
        with self.assertRaises(ValueError):
            restock(stock, "CA-9", "M", 0)
        self.assertNotIn("CA-9", stock)

    def test_positive(self):
        stock = copy.deepcopy(STOCK)
        restock(stock, "UR-1", "S", 3)
        self.assertEqual(stock["UR-1"]["units"]["S"], 5)
