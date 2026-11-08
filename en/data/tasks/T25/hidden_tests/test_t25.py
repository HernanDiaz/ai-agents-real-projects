"""Task T25: delivery to Hawaii in 6-9 business days."""
import unittest
from pathlib import Path

from shipping import estimated_delivery


class T25Tests(unittest.TestCase):

    def test_hawaii(self):
        # Ships on a Friday: 6 business days is Monday the 19th; 9, Thursday the 22nd.
        self.assertEqual(estimated_delivery("2026-10-09", "96720"),
                         ("2026-10-19", "2026-10-22"))

    def test_others_unchanged(self):
        self.assertEqual(estimated_delivery("2026-10-09", "97205"),
                         ("2026-10-13", "2026-10-14"))
        self.assertEqual(estimated_delivery("2026-10-09", "00730"),
                         ("2026-10-14", "2026-10-16"))

    def test_terms(self):
        text = Path("docs/terms_and_conditions.md").read_text(encoding="utf-8")
        self.assertIn("to Hawaii, within 6-9 business days", text)
