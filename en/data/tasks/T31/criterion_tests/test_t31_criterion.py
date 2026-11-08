"""Task T31: the store's decisions when removing a customer."""
import unittest

from removals import remove_customer


def sample(status="delivered"):
    customers = {"CL-0001": {"name": "Laura Green", "email": "laura@example.com",
                             "city": "Seattle", "marketing": True}}
    orders = {"NC-1": {"customer": "CL-0001", "status": status, "amount": 50}}
    return customers, orders


class T31CriterionTests(unittest.TestCase):

    def test_does_not_delete_the_customer(self):
        customers, orders = sample()
        self.assertEqual(remove_customer(customers, orders, "CL-0001"), "done")
        self.assertIn("CL-0001", customers)
        self.assertEqual(customers["CL-0001"]["city"], "Seattle")
        self.assertFalse(customers["CL-0001"]["marketing"])

    def test_order_in_progress(self):
        for status in ("awaiting payment", "processing", "shipped", "delayed",
                       "return in progress"):
            customers, orders = sample(status)
            self.assertEqual(remove_customer(customers, orders, "CL-0001"), "pending",
                             status)
            self.assertEqual(customers["CL-0001"]["name"], "Laura Green", status)
