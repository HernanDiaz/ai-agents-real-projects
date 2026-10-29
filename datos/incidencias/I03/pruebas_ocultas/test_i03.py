"""Incidencia I03: la dosis tiene en cuenta las alergias."""
import unittest

from farmacia import dosis

FARMACIA = {"meloxicam": {"presentacion": "suspensión oral 1,5 mg/ml", "dosis_mg_kg": 0.1,
                          "especies": ["perro", "gato"], "existencias": 14, "precio": 18.5}}
COCO = {"nombre": "Coco", "especie": "perro", "peso_kg": 12.6, "alergias": ["meloxicam"]}
LOLA = {"nombre": "Lola", "especie": "perro", "peso_kg": 13.0, "alergias": ["pollo"]}


class PruebasI03(unittest.TestCase):

    def test_alergia(self):
        with self.assertRaises(ValueError):
            dosis(FARMACIA, "meloxicam", COCO)

    def test_sin_alergia(self):
        self.assertEqual(dosis(FARMACIA, "meloxicam", LOLA)["mg"], 1.3)
