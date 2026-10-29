"""Tarea T34: las decisiones de la tienda sobre las reservas."""
import unittest

from reservas import reserva_agotada

EXISTENCIAS = {"UR-5120": {"nombre": "Urbana 3", "unidades": {"L": 0}},
               "CA-2010": {"nombre": "Casco Ruta", "unidades": {"M": 0}}}


class CriterioT34(unittest.TestCase):

    def test_sin_reposicion(self):
        self.assertFalse(reserva_agotada(EXISTENCIAS, "UR-5120", "L", {})["admite"])

    def test_sin_confirmar(self):
        r = reserva_agotada(EXISTENCIAS, "UR-5120", "L",
                            {"UR-5120": {"fecha": "2026-11-10", "confirmada": False}})
        self.assertTrue(r["admite"])
        self.assertIsNone(r["fecha"])

    def test_accesorio(self):
        r = reserva_agotada(EXISTENCIAS, "CA-2010", "M",
                            {"CA-2010": {"fecha": "2026-11-10", "confirmada": True}})
        self.assertFalse(r["admite"])
