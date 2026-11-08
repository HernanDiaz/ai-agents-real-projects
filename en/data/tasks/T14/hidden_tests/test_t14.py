"""Task T14: flexible search by email and order history."""
import unittest

import database
from customers import customer_orders, find_by_email


class T14Tests(unittest.TestCase):

    def test_flexible_email(self):
        customers = database.customers()
        self.assertEqual(find_by_email(customers, "  LAURA.GREEN@example.com "),
                         "CL-0001")
        self.assertEqual(find_by_email(customers, "anna.price@example.com"),
                         "CL-0008")
        self.assertIsNone(find_by_email(customers, "nobody@example.com"))

    def test_history(self):
        orders = database.orders()
        self.assertEqual(customer_orders(orders, "CL-0001"),
                         ["NC-11460", "NC-10482"])
        self.assertEqual(customer_orders(orders, "CL-0009"), ["NC-11302"])
        self.assertEqual(customer_orders(orders, "CL-0099"), [])


if __name__ == "__main__":
    unittest.main()
