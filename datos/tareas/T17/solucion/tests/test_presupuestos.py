"""Pruebas de los presupuestos del taller."""
import unittest

from presupuestos import (bateria_en_garantia, cubre_garantia, en_garantia,
                          precio_revision, presupuesto_reparacion, revision_gratuita,
                          texto_presupuesto)

DEFECTO = "defecto de fabricación"


class PruebasPresupuestos(unittest.TestCase):

    def test_revision_gratuita(self):
        self.assertTrue(revision_gratuita(True, "2026-05-01", "2026-08-01"))
        self.assertFalse(revision_gratuita(False, "2026-05-01", "2026-08-01"))
        self.assertFalse(revision_gratuita(True, "2025-12-01", "2026-08-01"))

    def test_precio_revision(self):
        self.assertEqual(precio_revision(True, "2026-05-01", "2026-08-01"), 0)
        self.assertEqual(precio_revision(False, "2026-05-01", "2026-08-01"), 39)

    def test_garantia(self):
        self.assertTrue(en_garantia("2024-10-13", "2026-10-13"))
        self.assertFalse(en_garantia("2024-10-12", "2026-10-13"))
        self.assertTrue(cubre_garantia("2026-01-10", "2026-10-13", "Cambio", DEFECTO))
        self.assertFalse(cubre_garantia("2026-01-10", "2026-10-13", "Cadena", DEFECTO))
        self.assertFalse(cubre_garantia("2026-01-10", "2026-10-13", "Cambio", "caída"))

    def test_bateria(self):
        self.assertTrue(bateria_en_garantia("2025-06-01", "2026-10-13", 0.65))
        self.assertFalse(bateria_en_garantia("2025-06-01", "2026-10-13", 0.80))

    def test_reparacion(self):
        p = presupuesto_reparacion([("Cadena", 24.9), ("Cambio", 45)], 1.5,
                                   "2026-01-10", "2026-10-13", DEFECTO)
        self.assertEqual(p["total"], 69.9)
        p = presupuesto_reparacion([("Cambio", 45)], 1, "2026-01-10", "2026-10-13",
                                   DEFECTO)
        self.assertEqual(p["total"], 0)

    def test_texto(self):
        p = presupuesto_reparacion([("Cubierta", 32)], 0.5, "2020-01-10", "2026-10-13",
                                   "desgaste")
        self.assertIn("47,00 €", texto_presupuesto(p))


if __name__ == "__main__":
    unittest.main()
