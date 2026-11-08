import unittest

from utils import format_dollars, round_cents, to_minutes, to_time, weekday


class UtilsTests(unittest.TestCase):

    def test_dollars(self):
        self.assertEqual(format_dollars(1234.5), "$1,234.50")
        self.assertEqual(round_cents(2.345), 2.35)

    def test_times(self):
        self.assertEqual(to_minutes("09:30"), 570)
        self.assertEqual(to_time(570), "09:30")

    def test_weekday(self):
        self.assertEqual(weekday("2026-10-19"), 0)


if __name__ == "__main__":
    unittest.main()
