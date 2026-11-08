"""Tests of the date and amount utilities."""
import unittest

from utils import (add_business_days, add_days, add_months, days_between,
                   format_date, format_dollars, round_cents)


class UtilsTests(unittest.TestCase):

    def test_days(self):
        self.assertEqual(days_between("2026-09-17", "2026-10-13"), 26)
        self.assertEqual(add_days("2026-09-17", 30), "2026-10-17")

    def test_business_days(self):
        # 2026-10-09 is a Friday: two business days later is a Tuesday.
        self.assertEqual(add_business_days("2026-10-09", 2), "2026-10-13")

    def test_months(self):
        self.assertEqual(add_months("2026-04-10", 6), "2026-10-10")
        self.assertEqual(add_months("2026-08-31", 6), "2027-02-28")

    def test_amounts(self):
        self.assertEqual(round_cents(2.345), 2.35)
        self.assertEqual(format_dollars(1234.5), "$1,234.50")
        self.assertEqual(format_dollars(4.95), "$4.95")

    def test_format_date(self):
        self.assertEqual(format_date("2026-10-15"), "10/15/2026")


if __name__ == "__main__":
    unittest.main()
