"""Task T32: the repair shop's decisions about expensive estimates."""
import unittest

from approvals import estimate_with_approval

OLD = "2020-01-10"
TODAY = "2026-10-13"


class T32CriterionTests(unittest.TestCase):

    def test_threshold(self):
        exact = estimate_with_approval([("Wheel", 120)], 1, OLD, TODAY, "wear")
        above = estimate_with_approval([("Wheel", 120.01)], 1, OLD, TODAY, "wear")
        self.assertFalse(exact["approval"])
        self.assertTrue(above["approval"])

    def test_part_without_price(self):
        e = estimate_with_approval([("Chain", 24.9), ("Motor", None)], 2, OLD, TODAY,
                                   "wear")
        self.assertIsNone(e["total"])
        self.assertTrue(e["approval"])
