"""Task T33: notifying a delayed order (what the request asks for)."""
import unittest

from delays import delay_notice

CUSTOMER = {"name": "Laura Green", "email": "laura@example.com", "city": "Seattle"}
ORDER = {"customer": "CL-0001", "status": "delayed",
         "reason": "waiting for a part from the supplier",
         "expected_delivery": "2026-10-28"}


class T33Tests(unittest.TestCase):

    def test_notice(self):
        text = delay_notice("NC-10500", ORDER, CUSTOMER, "2026-10-20")
        self.assertIn("Hi Laura", text)
        self.assertIn("NC-10500", text)
        self.assertIn("10/28/2026", text)
        self.assertIn("North Cycles", text)
