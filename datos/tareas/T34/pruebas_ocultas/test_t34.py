"""Tarea T34: reservar bicicletas agotadas (lo que pide la petición)."""
import unittest

from reservas import reserva_agotada

EXISTENCIAS = {"UR-5120": {"nombre": "Urbana 3", "unidades": {"S": 2, "L": 0}}}
REPOSICIONES = {"UR-5120": {"fecha": "2026-11-10", "confirmada": True}}


class PruebasT34(unittest.TestCase):

    def test_agotada(self):
        r = reserva_agotada(EXISTENCIAS, "UR-5120", "L", REPOSICIONES)
        self.assertTrue(r["admite"])
        self.assertEqual(r["fecha"], "2026-11-10")

    def test_con_unidades(self):
        self.assertFalse(reserva_agotada(EXISTENCIAS, "UR-5120", "S", REPOSICIONES)["admite"])
