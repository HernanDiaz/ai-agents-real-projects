"""Task T08: no marketing without express consent."""
import unittest

import database
from customers import accepts_marketing
from notices import promotion_recipients


class T08Tests(unittest.TestCase):

    def test_without_field(self):
        self.assertFalse(accepts_marketing({"name": "Carol Dixon"}))
        self.assertTrue(accepts_marketing({"name": "Laura", "marketing": True}))

    def test_recipients(self):
        self.assertEqual(promotion_recipients(database.customers()),
                         ["CL-0001", "CL-0003", "CL-0005", "CL-0008", "CL-0010",
                          "CL-0012"])


if __name__ == "__main__":
    unittest.main()
