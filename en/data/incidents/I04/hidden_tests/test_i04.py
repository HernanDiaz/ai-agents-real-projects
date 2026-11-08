"""Incident I04: an emergency visit costs $70."""
import unittest
from pathlib import Path

import config


class I04Tests(unittest.TestCase):

    def test_price(self):
        self.assertEqual(config.PRICES["emergency visit"], 70.0)
        self.assertEqual(config.PRICES["consultation"], 35.0)

    def test_list(self):
        text = Path("docs/price_list.md").read_text(encoding="utf-8")
        self.assertIn("| Emergency visit | $70.00 |", text)
        self.assertNotIn("$60.00", text)
