"""Task T31: removing a customer (what the request asks for)."""
import json
import unittest

from removals import remove_customer


class T31Tests(unittest.TestCase):

    def test_deletes_name_and_email(self):
        customers = {"CL-0001": {"name": "Laura Green", "email": "laura@example.com",
                                 "city": "Seattle", "marketing": True}}
        orders = {"NC-1": {"customer": "CL-0001", "status": "delivered", "amount": 50}}
        remove_customer(customers, orders, "CL-0001")
        text = json.dumps(customers, ensure_ascii=False)
        self.assertNotIn("Laura", text)
        self.assertNotIn("laura@example.com", text)
