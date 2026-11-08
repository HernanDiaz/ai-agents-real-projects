"""Task T07: the six months of free tune-ups are calendar months."""
import unittest

from estimates import free_tune_up, tune_up_price


class T07Tests(unittest.TestCase):

    def test_within_six_months(self):
        self.assertTrue(free_tune_up(True, "2026-04-10", "2026-10-08"))
        self.assertTrue(free_tune_up(True, "2026-04-10", "2026-10-10"))
        self.assertTrue(free_tune_up(True, "2026-01-31", "2026-07-30"))
        self.assertTrue(free_tune_up(True, "2026-08-31", "2027-02-28"))

    def test_outside(self):
        self.assertFalse(free_tune_up(True, "2026-04-10", "2026-10-11"))
        self.assertFalse(free_tune_up(True, "2026-08-31", "2027-03-01"))
        self.assertFalse(free_tune_up(False, "2026-04-10", "2026-10-08"))

    def test_price(self):
        self.assertEqual(tune_up_price(True, "2026-04-10", "2026-10-08"), 0)


if __name__ == "__main__":
    unittest.main()
