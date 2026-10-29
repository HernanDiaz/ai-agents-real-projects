import unittest

from farmacia import disponible, dosis, etiqueta

FARMACIA = {"meloxicam": {"presentacion": "suspensión oral 1,5 mg/ml", "dosis_mg_kg": 0.1,
                          "especies": ["perro", "gato"], "existencias": 14, "precio": 18.5},
            "maropitant": {"presentacion": "comprimidos de 16 mg", "dosis_mg_kg": 2,
                           "especies": ["perro"], "existencias": 0, "precio": 21.0}}
LOLA = {"nombre": "Lola", "especie": "perro", "peso_kg": 13.0, "alergias": []}
PIPO = {"nombre": "Pipo", "especie": "conejo", "peso_kg": 2.0, "alergias": []}


class PruebasFarmacia(unittest.TestCase):

    def test_dosis(self):
        self.assertEqual(dosis(FARMACIA, "meloxicam", LOLA)["mg"], 1.3)
        with self.assertRaises(ValueError):
            dosis(FARMACIA, "maropitant", PIPO)

    def test_disponible(self):
        self.assertTrue(disponible(FARMACIA, "meloxicam", 2))
        self.assertFalse(disponible(FARMACIA, "maropitant"))

    def test_etiqueta(self):
        texto = etiqueta(FARMACIA, "meloxicam", LOLA)
        self.assertIn("Para: Lola, 13.0 kg", texto)
        self.assertIn("18,50 €", texto)


if __name__ == "__main__":
    unittest.main()
