"""Tests of the customers."""
import unittest

from customers import accepts_marketing, find_by_email, register, valid_email

CUSTOMERS = {
    "CL-0001": {"name": "Laura Green", "email": "laura.green@example.com",
                "city": "Seattle", "marketing": True},
    "CL-0002": {"name": "Ralph Owens", "email": "ralph.owens@example.com",
                "city": "Boise", "marketing": False},
}


class CustomersTests(unittest.TestCase):

    def test_email(self):
        self.assertTrue(valid_email("anna@example.com"))
        self.assertFalse(valid_email("anna@example"))

    def test_find(self):
        self.assertEqual(find_by_email(CUSTOMERS, "ralph.owens@example.com"),
                         "CL-0002")
        self.assertIsNone(find_by_email(CUSTOMERS, "nobody@example.com"))

    def test_register(self):
        customers = dict(CUSTOMERS)
        new = register(customers, "Evan Reed", "evan@example.com", "Beaverton")
        self.assertEqual(new, "CL-0003")
        self.assertFalse(customers[new]["marketing"])
        with self.assertRaises(ValueError):
            register(customers, "Someone else", "evan@example.com", "Beaverton")

    def test_marketing(self):
        self.assertTrue(accepts_marketing(CUSTOMERS["CL-0001"]))
        self.assertFalse(accepts_marketing(CUSTOMERS["CL-0002"]))


if __name__ == "__main__":
    unittest.main()
