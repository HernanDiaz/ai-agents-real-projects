"""Tarea T32: las decisiones del taller sobre los presupuestos caros."""
import unittest

from aprobaciones import presupuesto_con_aprobacion

ANTIGUA = "2020-01-10"
HOY = "2026-10-13"


class CriterioT32(unittest.TestCase):

    def test_umbral(self):
        justo = presupuesto_con_aprobacion([("Rueda", 120)], 1, ANTIGUA, HOY, "desgaste")
        encima = presupuesto_con_aprobacion([("Rueda", 120.01)], 1, ANTIGUA, HOY,
                                            "desgaste")
        self.assertFalse(justo["aprobacion"])
        self.assertTrue(encima["aprobacion"])

    def test_pieza_sin_precio(self):
        p = presupuesto_con_aprobacion([("Cadena", 24.9), ("Motor", None)], 2, ANTIGUA,
                                       HOY, "desgaste")
        self.assertIsNone(p["total"])
        self.assertTrue(p["aprobacion"])
