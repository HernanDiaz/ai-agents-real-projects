"""Tarea T17: la revisión básica cuesta 39 €."""
import unittest
from pathlib import Path

from avisos import aviso_revision
from presupuestos import precio_revision


class PruebasT17(unittest.TestCase):

    def test_precio(self):
        self.assertEqual(precio_revision(False, "2026-05-01", "2026-08-01"), 39)
        self.assertEqual(precio_revision(True, "2025-01-10", "2026-10-13"), 39)

    def test_recordatorio(self):
        texto = aviso_revision({"nombre": "Laura Gómez"}, "2026-04-10")
        self.assertIn("39", texto)
        self.assertNotIn("35", texto)

    def test_condiciones(self):
        texto = Path("docs/condiciones_generales.md").read_text(encoding="utf-8")
        self.assertIn("La revisión básica cuesta 39 euros", texto)


if __name__ == "__main__":
    unittest.main()
