"""Task T26: the size on the lines of the invoice."""
import unittest

from invoices import invoice, invoice_text

HELMET = {"ref": "CA-4010", "name": "City Helmet", "size": "M", "quantity": 1,
          "price": 49}
LIGHTS = {"ref": "LU-6080", "name": "City Light Kit", "size": "one size",
          "quantity": 2, "price": 25}
ORDER = {"lines": [HELMET, LIGHTS], "shipping": 0, "amount": 99}


class T26Tests(unittest.TestCase):

    def setUp(self):
        self.text = invoice_text(invoice("I2026-0001", "NC-1", ORDER,
                                         {"name": "Laura Green"}, "2026-10-13"))

    def test_size(self):
        self.assertIn("1 × City Helmet (M)", self.text)

    def test_one_size(self):
        self.assertIn("2 × City Light Kit ", self.text)
        self.assertNotIn("(one size)", self.text)
