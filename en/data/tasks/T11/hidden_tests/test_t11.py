"""Task T11: delayed-order notice."""
import unittest

import database
from notices import delay_notice


class T11Tests(unittest.TestCase):

    def test_sample_order(self):
        order = database.orders()["NC-11302"]
        customer = database.customers()[order["customer"]]
        self.assertEqual(
            delay_notice("NC-11302", order, customer),
            "Hi James,\n\nYour order NC-11302 has been delayed (size L out of "
            "stock). The new expected delivery date is 10/15/2026. We apologize for "
            "the inconvenience.\n\nBest regards,\nNorth Cycles")

    def test_another_reason(self):
        order = {"reason": "a problem with the carrier",
                 "expected_delivery": "2026-11-02"}
        text = delay_notice("NC-11500", order, {"name": "Anna Price"})
        self.assertIn("has been delayed (a problem with the carrier).", text)
        self.assertIn("is 11/02/2026.", text)
        self.assertTrue(text.startswith("Hi Anna,"))


if __name__ == "__main__":
    unittest.main()
