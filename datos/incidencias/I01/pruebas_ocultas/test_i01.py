"""Incidencia I01: sin huecos los fines de semana."""
import unittest

from citas import huecos_libres


class PruebasI01(unittest.TestCase):

    def test_fin_de_semana(self):
        self.assertEqual(huecos_libres([], "V1", "2026-10-24"), [])
        self.assertEqual(huecos_libres([], "V1", "2026-10-25"), [])

    def test_entre_semana(self):
        self.assertEqual(len(huecos_libres([], "V1", "2026-10-23")), 10)
