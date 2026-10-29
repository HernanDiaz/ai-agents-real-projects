"""Tarea T23: unidades totales de una referencia."""
import unittest

import base_datos
from existencias import total_unidades

EXISTENCIAS = {"UR-1": {"nombre": "Urbana", "unidades": {"S": 2, "M": 0, "L": 3}},
               "CA-1": {"nombre": "Casco", "unidades": {"única": 0}}}


class PruebasT23(unittest.TestCase):

    def test_total(self):
        self.assertEqual(total_unidades(EXISTENCIAS, "UR-1"), 5)
        self.assertEqual(total_unidades(EXISTENCIAS, "CA-1"), 0)

    def test_no_existe(self):
        self.assertEqual(total_unidades(EXISTENCIAS, "XX-0"), 0)

    def test_base_de_datos(self):
        existencias = base_datos.existencias()
        ref = sorted(existencias)[0]
        self.assertEqual(total_unidades(existencias, ref),
                         sum(existencias[ref]["unidades"].values()))
