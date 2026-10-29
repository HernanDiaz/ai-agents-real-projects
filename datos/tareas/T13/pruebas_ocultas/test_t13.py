"""Tarea T13: tallas con pocas unidades."""
import unittest

import base_datos
import config
from existencias import existencias_bajas


class PruebasT13(unittest.TestCase):

    def test_orden_y_limites(self):
        existencias = {"B-2": {"nombre": "B", "unidades": {"S": 1, "M": 0, "L": 2}},
                       "A-1": {"nombre": "A", "unidades": {"única": 3}},
                       "C-3": {"nombre": "C", "unidades": {"XL": 2, "M": 1}}}
        self.assertEqual(existencias_bajas(existencias),
                         [("B-2", "S", 1), ("B-2", "L", 2), ("C-3", "XL", 2),
                          ("C-3", "M", 1)])

    def test_minimo_en_config(self):
        self.assertEqual(config.MINIMO_EXISTENCIAS, 2)

    def test_almacen_de_ejemplo(self):
        bajas = existencias_bajas(base_datos.existencias())
        self.assertEqual(len(bajas), 16)
        self.assertEqual(bajas[:3], [("CR-7010", "50", 1), ("CR-7010", "52", 2),
                                     ("CR-7010", "58", 1)])
        self.assertEqual(bajas[-1], ("UR-5150", "L", 1))


if __name__ == "__main__":
    unittest.main()
