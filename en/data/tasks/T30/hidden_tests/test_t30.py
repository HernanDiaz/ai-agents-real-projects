"""Task T30: payment-pending notice."""
import unittest

from notices import payment_pending_notice

LAURA = {"name": "Laura Green", "email": "laura.green@example.com"}
ORDER = {"amount": 1249.5, "order_date": "2026-10-08", "status": "awaiting payment",
         "payment": {"method": "transfer", "received": None}}


class T30Tests(unittest.TestCase):

    def setUp(self):
        self.text = payment_pending_notice("NC-11460", ORDER, LAURA)

    def test_greeting_and_signature(self):
        self.assertTrue(self.text.startswith("Hi Laura,"))
        self.assertTrue(self.text.endswith("Best regards,\nNorth Cycles"))

    def test_data(self):
        self.assertIn("NC-11460", self.text)
        self.assertIn("$1,249.50", self.text)
        self.assertIn("10/13/2026", self.text)
