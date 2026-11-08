"""Incident I03: the dose takes allergies into account."""
import unittest

from pharmacy import dose

PHARMACY = {"meloxicam": {"presentation": "oral suspension 1.5 mg/ml",
                          "dose_mg_kg": 0.1, "species": ["dog", "cat"], "stock": 14,
                          "price": 18.5}}
COCO = {"name": "Coco", "species": "dog", "weight_kg": 12.6, "allergies": ["meloxicam"]}
LOLA = {"name": "Lola", "species": "dog", "weight_kg": 13.0, "allergies": ["chicken"]}


class I03Tests(unittest.TestCase):

    def test_allergy(self):
        with self.assertRaises(ValueError):
            dose(PHARMACY, "meloxicam", COCO)

    def test_no_allergy(self):
        self.assertEqual(dose(PHARMACY, "meloxicam", LOLA)["mg"], 1.3)
