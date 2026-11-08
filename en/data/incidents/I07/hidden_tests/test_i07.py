"""Incident I07: dollar formatting in one place."""
import unittest
from pathlib import Path

from invoices import invoice_text
from pharmacy import label

PHARMACY = {"meloxicam": {"presentation": "oral suspension 1.5 mg/ml",
                          "dose_mg_kg": 0.1, "species": ["dog", "cat"], "stock": 14,
                          "price": 1018.5}}
LOLA = {"name": "Lola", "species": "dog", "weight_kg": 13.0, "allergies": []}
INVOICE = {"id": "INV-0001", "owner": "C-001", "date": "2026-10-16",
           "lines": [{"item": "dental cleaning", "amount": 1120.0}]}


class I07Tests(unittest.TestCase):

    def test_no_copies(self):
        for file in ("pharmacy.py", "invoices.py"):
            code = Path(file).read_text(encoding="utf-8")
            self.assertNotIn("def _dollars", code)
            self.assertIn("format_dollars", code)

    def test_same_texts(self):
        self.assertIn("Price: $1,018.50", label(PHARMACY, "meloxicam", LOLA))
        self.assertIn("$1,120.00", invoice_text(INVOICE))
