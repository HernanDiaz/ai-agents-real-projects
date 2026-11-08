"""Tests of the notices to customers."""
import unittest

from notices import (cancellation_notice, delivery_notice, promotion,
                     promotion_recipients, shipping_notice, tune_up_notice)

LAURA = {"name": "Laura Green", "marketing": True}
RALPH = {"name": "Ralph Owens", "marketing": False}


class NoticesTests(unittest.TestCase):

    def test_shipping(self):
        order = {"carrier": "SwiftShip", "tracking": "SS-558201",
                 "expected_delivery": "2026-10-10"}
        text = shipping_notice("NC-10871", order, LAURA)
        self.assertTrue(text.startswith("Hi Laura,"))
        self.assertIn("SS-558201", text)
        self.assertIn("10/10/2026", text)
        self.assertTrue(text.endswith("Best regards,\nNorth Cycles"))

    def test_delivery(self):
        text = delivery_notice("NC-10482", {"delivery_date": "2026-09-17"}, LAURA)
        self.assertIn("until 10/17/2026", text)

    def test_cancellation(self):
        order = {"reason": "canceled by the customer", "amount": 89}
        self.assertIn("$89.00", cancellation_notice("NC-11215", order, LAURA))

    def test_tune_up(self):
        self.assertIn("10/10/2026", tune_up_notice(LAURA, "2026-04-10"))
        self.assertIn("$39.00", tune_up_notice(LAURA, "2026-04-10"))

    def test_promotion(self):
        self.assertEqual(promotion_recipients({"CL-1": LAURA, "CL-2": RALPH}),
                         ["CL-1"])
        self.assertIn("UNSUBSCRIBE", promotion(LAURA, "Discounts on helmets."))


if __name__ == "__main__":
    unittest.main()
