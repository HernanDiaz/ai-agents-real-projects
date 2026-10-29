"""Tarea T24: reposiciones de cero o negativas."""
import copy
import unittest

from existencias import reponer

EXISTENCIAS = {"UR-1": {"nombre": "Urbana", "unidades": {"S": 2}}}


class PruebasT24(unittest.TestCase):

    def test_negativa(self):
        existencias = copy.deepcopy(EXISTENCIAS)
        with self.assertRaises(ValueError):
            reponer(existencias, "UR-1", "S", -3)
        self.assertEqual(existencias, EXISTENCIAS)

    def test_cero_en_referencia_nueva(self):
        existencias = copy.deepcopy(EXISTENCIAS)
        with self.assertRaises(ValueError):
            reponer(existencias, "CA-9", "M", 0)
        self.assertNotIn("CA-9", existencias)

    def test_positiva(self):
        existencias = copy.deepcopy(EXISTENCIAS)
        reponer(existencias, "UR-1", "S", 3)
        self.assertEqual(existencias["UR-1"]["unidades"]["S"], 5)
