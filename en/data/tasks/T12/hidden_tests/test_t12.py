"""Task T12: consecutive numbering and credit notes."""
import unittest

from invoices import (credit_note, invoice, invoice_text, next_invoice_number,
                      split_tax)

ORDER = {"lines": [{"ref": "UR-5150", "name": "City 5", "size": "M",
                    "quantity": 1, "price": 589}],
         "shipping": 0, "amount": 589, "payment": {"method": "card"}}


class T12Tests(unittest.TestCase):

    def test_numbering(self):
        self.assertEqual(next_invoice_number([], "2026-10-13"), "I2026-0001")
        issued = ["I2026-0007", "I2026-0012", "I2025-0450", "C2026-0003"]
        self.assertEqual(next_invoice_number(issued, "2026-10-13"),
                         "I2026-0013")
        self.assertEqual(next_invoice_number(issued, "2027-01-02"),
                         "I2027-0001")
        self.assertEqual(next_invoice_number(issued, "2026-10-13", series="C"),
                         "C2026-0004")

    def test_credit_note(self):
        original = invoice("I2026-0007", "NC-10482", ORDER, {"name": "Laura Green"},
                           "2026-09-14")
        note = credit_note(original, 589, "C2026-0001", "2026-10-20")
        before_tax, tax = split_tax(589)
        self.assertEqual(note["number"], "C2026-0001")
        self.assertEqual(note["corrects"], "I2026-0007")
        self.assertEqual(note["customer"], "Laura Green")
        self.assertEqual(note["order"], "NC-10482")
        self.assertEqual((note["total"], note["before_tax"], note["tax"]),
                         (-589, -before_tax, -tax))
        text = invoice_text(note)
        self.assertIn("C2026-0001", text)
        self.assertIn("-$589.00", text)


if __name__ == "__main__":
    unittest.main()
