"""Incidencia I04: la urgencia cuesta 70 euros."""
import unittest
from pathlib import Path

import config


class PruebasI04(unittest.TestCase):

    def test_precio(self):
        self.assertEqual(config.TARIFAS["urgencia"], 70.0)
        self.assertEqual(config.TARIFAS["consulta"], 35.0)

    def test_lista(self):
        texto = Path("docs/tarifas.md").read_text(encoding="utf-8")
        self.assertIn("| Urgencia | 70,00 € |", texto)
        self.assertNotIn("60,00 €", texto)
