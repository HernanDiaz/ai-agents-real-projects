"""Task T15: new free-shipping thresholds."""
import unittest
from pathlib import Path

from shipping import shipping_cost


class T15Tests(unittest.TestCase):

    def test_contiguous(self):
        self.assertEqual(shipping_cost(55, "97205"), 4.95)
        self.assertEqual(shipping_cost(60, "97205"), 4.95)
        self.assertEqual(shipping_cost(60.01, "97205"), 0)

    def test_islands(self):
        self.assertEqual(shipping_cost(149, "00730"), 9.95)
        self.assertEqual(shipping_cost(150.01, "00730"), 0)
        self.assertEqual(shipping_cost(500, "96813"), 14.95)
        self.assertEqual(shipping_cost(500, "96720"), 14.95)

    def test_terms(self):
        text = Path("docs/terms_and_conditions.md").read_text(encoding="utf-8")
        self.assertIn("orders over $60", text)
        self.assertIn("orders over $150", text)
        self.assertNotIn("orders over $50", text)


if __name__ == "__main__":
    unittest.main()
