"""Task T09: installments of a payment plan and their line on the invoice."""
import unittest

from invoices import invoice, invoice_text
from orders import installments

LINE = {"ref": "CR-7010", "name": "Aero 3", "size": "54", "quantity": 1,
        "price": 1150}


class T09Tests(unittest.TestCase):

    def test_installments(self):
        self.assertEqual(installments(1000, 3), [333.33, 333.33, 333.34])
        self.assertEqual(installments(1150, 6), [191.67] * 5 + [191.65])
        self.assertEqual(len(installments(301, 12)), 12)

    def test_add_up_to_amount(self):
        for amount in (301, 449.95, 1649, 3490):
            for months in (3, 6, 12):
                self.assertEqual(round(sum(installments(amount, months)), 2), amount)

    def test_errors(self):
        with self.assertRaises(ValueError):
            installments(300, 3)
        with self.assertRaises(ValueError):
            installments(1000, 4)

    def test_invoice(self):
        order = {"lines": [LINE], "shipping": 0, "amount": 1150,
                 "payment": {"method": "card", "received": "2026-09-08",
                             "installments": 6}}
        text = invoice_text(invoice("I2026-0002", "NC-11020", order,
                                    {"name": "Martha Ingram"}, "2026-09-08"))
        self.assertIn("Installment plan: 6 payments of $191.67", text)
        order["payment"] = {"method": "card", "received": "2026-09-08"}
        text = invoice_text(invoice("I2026-0002", "NC-11020", order,
                                    {"name": "Martha Ingram"}, "2026-09-08"))
        self.assertNotIn("Installment plan", text)


if __name__ == "__main__":
    unittest.main()
