import unittest

from pharmacy import available, dose, label

PHARMACY = {"meloxicam": {"presentation": "oral suspension 1.5 mg/ml",
                          "dose_mg_kg": 0.1, "species": ["dog", "cat"], "stock": 14, "price": 18.5},
            "maropitant": {"presentation": "16 mg tablets", "dose_mg_kg": 2,
                           "species": ["dog"], "stock": 0, "price": 21.0}}
LOLA = {"name": "Lola", "species": "dog", "weight_kg": 13.0, "allergies": []}
PIP = {"name": "Pip", "species": "rabbit", "weight_kg": 2.0, "allergies": []}


class PharmacyTests(unittest.TestCase):

    def test_dose(self):
        self.assertEqual(dose(PHARMACY, "meloxicam", LOLA)["mg"], 1.3)
        with self.assertRaises(ValueError):
            dose(PHARMACY, "maropitant", PIP)

    def test_available(self):
        self.assertTrue(available(PHARMACY, "meloxicam", 2))
        self.assertFalse(available(PHARMACY, "maropitant"))

    def test_label(self):
        text = label(PHARMACY, "meloxicam", LOLA)
        self.assertIn("For: Lola, 13.0 kg", text)
        self.assertIn("$18.50", text)


if __name__ == "__main__":
    unittest.main()
