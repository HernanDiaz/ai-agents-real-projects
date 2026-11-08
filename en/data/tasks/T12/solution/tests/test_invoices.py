"""Tests of the invoices."""
import unittest

from invoices import (credit_note, invoice, invoice_text, next_invoice_number,
                      split_tax)

ORDER = {"lines": [{"ref": "CA-4010", "name": "City Helmet", "size": "M",
                    "quantity": 2, "price": 49}],
         "shipping": 0, "amount": 98, "payment": {"method": "card"}}
CUSTOMER = {"name": "Laura Green"}


class InvoicesTests(unittest.TestCase):

    def test_before_tax(self):
        self.assertEqual(split_tax(110)[0], 100)
        self.assertEqual(split_tax(589)[0], 535.45)

    def test_invoice(self):
        data = invoice("I2026-0001", "NC-11500", ORDER, CUSTOMER, "2026-10-13")
        self.assertEqual(data["total"], 98)
        self.assertEqual(data["before_tax"], 89.09)

    def test_numbering(self):
        self.assertEqual(next_invoice_number(["I2026-0007"], "2026-10-13"),
                         "I2026-0008")

    def test_credit_note(self):
        original = invoice("I2026-0001", "NC-11500", ORDER, CUSTOMER, "2026-10-13")
        note = credit_note(original, 49, "C2026-0001", "2026-10-20")
        self.assertEqual(note["total"], -49)

    def test_text(self):
        text = invoice_text(invoice("I2026-0001", "NC-11500", ORDER, CUSTOMER,
                                    "2026-10-13"))
        self.assertIn("Invoice I2026-0001 · 10/13/2026", text)
        self.assertIn("2 × City Helmet", text)
        self.assertIn("$98.00", text)


if __name__ == "__main__":
    unittest.main()
