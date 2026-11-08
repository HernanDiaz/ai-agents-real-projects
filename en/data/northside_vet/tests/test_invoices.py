import unittest

from invoices import invoice_text, owner_invoices, split_tax, total

INVOICES = [{"id": "INV-0002", "owner": "C-001", "date": "2026-10-18",
             "lines": [{"item": "consultation", "amount": 35.0}]},
            {"id": "INV-0001", "owner": "C-001", "date": "2026-10-16",
             "lines": [{"item": "DHPP vaccine", "amount": 38.0},
                       {"item": "deworming", "amount": 15.0}]},
            {"id": "INV-0003", "owner": "C-002", "date": "2026-10-17",
             "lines": [{"item": "wound care", "amount": 22.0}]}]


class InvoicesTests(unittest.TestCase):

    def test_total(self):
        self.assertEqual(total(INVOICES[1]["lines"]), 53.0)

    def test_tax(self):
        self.assertEqual(split_tax(110.0), {"before_tax": 100.0, "tax": 10.0})

    def test_of_an_owner(self):
        self.assertEqual([i["id"] for i in owner_invoices(INVOICES, "C-001")],
                         ["INV-0001", "INV-0002"])

    def test_text(self):
        text = invoice_text(INVOICES[1])
        self.assertIn("Invoice INV-0001 · 10/16/2026", text)
        self.assertIn("$53.00", text)


if __name__ == "__main__":
    unittest.main()
