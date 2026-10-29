"""Tarea T15: nuevos umbrales de envío gratis."""
import unittest
from pathlib import Path

from envios import gastos_envio


class PruebasT15(unittest.TestCase):

    def test_peninsula(self):
        self.assertEqual(gastos_envio(55, "33001"), 4.95)
        self.assertEqual(gastos_envio(60, "33001"), 4.95)
        self.assertEqual(gastos_envio(60.01, "33001"), 0)

    def test_islas(self):
        self.assertEqual(gastos_envio(149, "07800"), 9.95)
        self.assertEqual(gastos_envio(150.01, "07800"), 0)
        self.assertEqual(gastos_envio(500, "38001"), 14.95)
        self.assertEqual(gastos_envio(500, "35001"), 14.95)

    def test_condiciones(self):
        texto = Path("docs/condiciones_generales.md").read_text(encoding="utf-8")
        self.assertIn("más de 60 euros", texto)
        self.assertIn("más de 150 euros", texto)
        self.assertNotIn("más de 50 euros", texto)


if __name__ == "__main__":
    unittest.main()
