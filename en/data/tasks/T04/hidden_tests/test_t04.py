"""Task T04: the amount before tax plus the tax add up to the total."""
import unittest

from invoices import invoice, split_tax


class T04Tests(unittest.TestCase):

    def test_known_cases(self):
        self.assertEqual(split_tax(110), (100.0, 10.0))
        self.assertEqual(split_tax(589), (535.45, 53.55))

    def test_add_up_to_total(self):
        for total in (49.95, 98, 1649, 0.99, 2190, 53.95):
            before_tax, tax = split_tax(total)
            self.assertEqual(round(before_tax + tax, 2), total, total)

    def test_invoice(self):
        order = {"lines": [], "shipping": 0, "amount": 74, "payment": {}}
        data = invoice("I2026-0001", "NC-10871", order, {"name": "Lucy Rivers"},
                       "2026-10-13")
        self.assertEqual(round(data["before_tax"] + data["tax"], 2), 74)


if __name__ == "__main__":
    unittest.main()
