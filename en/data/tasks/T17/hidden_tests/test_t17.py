"""Task T17: the basic tune-up costs $39."""
import unittest
from pathlib import Path

from estimates import tune_up_price
from notices import tune_up_notice


class T17Tests(unittest.TestCase):

    def test_price(self):
        self.assertEqual(tune_up_price(False, "2026-05-01", "2026-08-01"), 39)
        self.assertEqual(tune_up_price(True, "2025-01-10", "2026-10-13"), 39)

    def test_reminder(self):
        text = tune_up_notice({"name": "Laura Green"}, "2026-04-10")
        self.assertIn("39", text)
        self.assertNotIn("35", text)

    def test_terms(self):
        text = Path("docs/terms_and_conditions.md").read_text(encoding="utf-8")
        self.assertIn("The basic tune-up costs $39", text)


if __name__ == "__main__":
    unittest.main()
