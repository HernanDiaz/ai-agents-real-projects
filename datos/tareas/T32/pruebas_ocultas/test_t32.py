"""Tarea T32: avisar de los presupuestos caros (lo que pide la petición)."""
import unittest

from aprobaciones import presupuesto_con_aprobacion

ANTIGUA = "2020-01-10"   # sin garantía
HOY = "2026-10-13"


class PruebasT32(unittest.TestCase):

    def test_caro(self):
        p = presupuesto_con_aprobacion([("Horquilla", 320)], 2, ANTIGUA, HOY, "desgaste")
        self.assertTrue(p["aprobacion"])
        self.assertEqual(p["total"], 380)

    def test_barato(self):
        p = presupuesto_con_aprobacion([("Cámara", 6)], 0.5, ANTIGUA, HOY, "desgaste")
        self.assertFalse(p["aprobacion"])
