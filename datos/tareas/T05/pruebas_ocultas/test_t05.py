"""Tarea T05: agotado es no tener unidades en ninguna talla."""
import unittest

import base_datos
from existencias import agotados, informe_agotados


class PruebasT05(unittest.TestCase):

    def test_con_alguna_talla(self):
        existencias = {"UR-5120": {"nombre": "Urbana 3",
                                   "unidades": {"S": 2, "M": 4, "L": 0}},
                       "EL-9050": {"nombre": "E-Urbana 600",
                                   "unidades": {"M": 0, "L": 0}}}
        self.assertEqual(agotados(existencias), ["EL-9050"])

    def test_almacen_de_ejemplo(self):
        self.assertEqual(agotados(base_datos.existencias()), ["EL-9050"])

    def test_informe(self):
        texto = informe_agotados(base_datos.existencias(), "2026-10-13")
        self.assertNotIn("Urbana 3", texto)
        self.assertEqual(len(texto.splitlines()), 1)


if __name__ == "__main__":
    unittest.main()
