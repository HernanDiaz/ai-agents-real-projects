"""Task T33: the store's decisions about the delay notice."""
import unittest

from delays import delay_notice

CUSTOMER = {"name": "Laura Green", "email": "laura@example.com", "city": "Seattle"}


def order(date):
    return {"customer": "CL-0001", "status": "delayed",
            "reason": "waiting for a part from the supplier", "expected_delivery": date}


class T33CriterionTests(unittest.TestCase):

    def test_short_delay(self):
        self.assertIsNone(delay_notice("NC-1", order("2026-10-22"), CUSTOMER,
                                       "2026-10-20"))
        self.assertIsNotNone(delay_notice("NC-1", order("2026-10-23"), CUSTOMER,
                                          "2026-10-20"))

    def test_reason_and_no_promises(self):
        text = delay_notice("NC-1", order("2026-10-28"), CUSTOMER, "2026-10-20")
        self.assertIn("waiting for a part from the supplier", text)
        for word in ("discount", "free", "gift", "compensat", "refund"):
            self.assertNotIn(word, text.lower())
