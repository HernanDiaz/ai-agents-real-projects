"""Tests of the repair shop estimates."""
import unittest

from estimates import (battery_under_warranty, estimate_text, free_tune_up,
                       repair_estimate, tune_up_price, under_warranty,
                       warranty_covers)

DEFECT = "manufacturing defect"


class EstimatesTests(unittest.TestCase):

    def test_free_tune_up(self):
        self.assertTrue(free_tune_up(True, "2026-05-01", "2026-08-01"))
        self.assertFalse(free_tune_up(False, "2026-05-01", "2026-08-01"))
        self.assertFalse(free_tune_up(True, "2025-12-01", "2026-08-01"))
        self.assertTrue(free_tune_up(True, "2026-04-10", "2026-10-08"))

    def test_tune_up_price(self):
        self.assertEqual(tune_up_price(True, "2026-05-01", "2026-08-01"), 0)
        self.assertEqual(tune_up_price(False, "2026-05-01", "2026-08-01"), 35)

    def test_warranty(self):
        self.assertTrue(under_warranty("2024-10-13", "2026-10-13"))
        self.assertFalse(under_warranty("2024-10-12", "2026-10-13"))
        self.assertTrue(warranty_covers("2026-01-10", "2026-10-13", "Derailleur",
                                        DEFECT))
        self.assertFalse(warranty_covers("2026-01-10", "2026-10-13", "Chain", DEFECT))
        self.assertFalse(warranty_covers("2026-01-10", "2026-10-13", "Derailleur",
                                         "crash"))

    def test_battery(self):
        self.assertTrue(battery_under_warranty("2025-06-01", "2026-10-13", 0.65))
        self.assertFalse(battery_under_warranty("2025-06-01", "2026-10-13", 0.80))

    def test_repair(self):
        e = repair_estimate([("Chain", 24.9), ("Derailleur", 45)], 1.5,
                            "2026-01-10", "2026-10-13", DEFECT)
        self.assertEqual(e["total"], 69.9)
        e = repair_estimate([("Derailleur", 45)], 1, "2026-01-10", "2026-10-13",
                            DEFECT)
        self.assertEqual(e["total"], 0)

    def test_text(self):
        e = repair_estimate([("Tire", 32)], 0.5, "2020-01-10", "2026-10-13", "wear")
        self.assertIn("$47.00", estimate_text(e))


if __name__ == "__main__":
    unittest.main()
