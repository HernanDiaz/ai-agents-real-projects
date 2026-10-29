"""Tarea T25: entrega a Canarias en 6-9 días laborables."""
import unittest
from pathlib import Path

from envios import fecha_entrega_estimada


class PruebasT25(unittest.TestCase):

    def test_canarias(self):
        # Sale un viernes: 6 laborables es el lunes 19 y 9 el jueves 22.
        self.assertEqual(fecha_entrega_estimada("2026-10-09", "35001"),
                         ("2026-10-19", "2026-10-22"))

    def test_resto_igual(self):
        self.assertEqual(fecha_entrega_estimada("2026-10-09", "33001"),
                         ("2026-10-13", "2026-10-14"))
        self.assertEqual(fecha_entrega_estimada("2026-10-09", "07800"),
                         ("2026-10-14", "2026-10-16"))

    def test_condiciones(self):
        texto = Path("docs/condiciones_generales.md").read_text(encoding="utf-8")
        self.assertIn("a Canarias, en 6-9 días laborables", texto)
