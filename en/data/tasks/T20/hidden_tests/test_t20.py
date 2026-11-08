"""Task T20: the notices are built with compose() and do not change."""
import inspect
import unittest

import notices

LAURA = {"name": "Laura Green"}
ORDER = {"carrier": "SwiftShip", "tracking": "SS-558201",
         "expected_delivery": "2026-10-10", "delivery_date": "2026-09-17",
         "reason": "canceled by the customer", "amount": 89}
EXPECTED = {
    "shipping": ("Hi Laura,\n\nYour order NC-10871 is on its way with SwiftShip. "
                 "The tracking number is SS-558201 and delivery is expected on "
                 "10/10/2026.\n\nBest regards,\nNorth Cycles"),
    "delivery": ("Hi Laura,\n\nYour order NC-10482 was delivered on 09/17/2026. If "
                 "you are not happy with anything, you can return it until "
                 "10/17/2026.\n\nBest regards,\nNorth Cycles"),
    "cancellation": ("Hi Laura,\n\nWe have canceled your order NC-11215 (canceled "
                     "by the customer). We will refund $89.00 within 14 days using "
                     "the same payment method.\n\nBest regards,\nNorth Cycles"),
    "tune_up": ("Hi Laura,\n\nThe first tune-up of your bike is free until "
                "10/10/2026. After that, the basic tune-up costs $35.\n\nBest "
                "regards,\nNorth Cycles"),
    "promotion": ("Hi Laura,\n\nHelmets 20% off.\n\nIf you don't want to receive "
                  "more emails like this one, reply with the word UNSUBSCRIBE.\n\n"
                  "Best regards,\nNorth Cycles"),
}


class T20Tests(unittest.TestCase):

    def test_compose(self):
        self.assertEqual(notices.compose(LAURA, "Text."),
                         "Hi Laura,\n\nText.\n\nBest regards,\nNorth Cycles")

    def test_greeting_and_signature_once(self):
        code = inspect.getsource(notices)
        self.assertEqual(code.count("Best regards"), 1)
        self.assertEqual(code.count("Hi "), 1)

    def test_same_texts(self):
        obtained = {
            "shipping": notices.shipping_notice("NC-10871", ORDER, LAURA),
            "delivery": notices.delivery_notice("NC-10482", ORDER, LAURA),
            "cancellation": notices.cancellation_notice("NC-11215", ORDER, LAURA),
            "tune_up": notices.tune_up_notice(LAURA, "2026-04-10"),
            "promotion": notices.promotion(LAURA, "Helmets 20% off."),
        }
        for key, expected in EXPECTED.items():
            self.assertEqual(obtained[key], expected, key)


if __name__ == "__main__":
    unittest.main()
