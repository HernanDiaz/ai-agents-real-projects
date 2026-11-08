"""Task T27: the customers with the most orders."""
import unittest

from reports import top_customers

ORDERS = {
    "NC-1": {"customer": "CL-0003", "status": "delivered"},
    "NC-2": {"customer": "CL-0003", "status": "shipped"},
    "NC-3": {"customer": "CL-0001", "status": "delivered"},
    "NC-4": {"customer": "CL-0002", "status": "delivered"},
    "NC-5": {"customer": "CL-0002", "status": "canceled"},
    "NC-6": {"customer": "CL-0004", "status": "canceled"},
}


class T27Tests(unittest.TestCase):

    def test_order(self):
        self.assertEqual(top_customers(ORDERS),
                         [("CL-0003", 2), ("CL-0001", 1), ("CL-0002", 1)])

    def test_n(self):
        self.assertEqual(top_customers(ORDERS, n=1), [("CL-0003", 2)])
