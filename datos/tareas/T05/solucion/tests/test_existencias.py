"""Pruebas de las existencias del almacén."""
import copy
import unittest

from existencias import (SinExistencias, agotados, hay_existencias, informe_agotados,
                         reponer, reservar, tallas_agotadas, unidades)

EXISTENCIAS = {
    "UR-5150": {"nombre": "Urbana 5", "unidades": {"S": 0, "M": 3, "L": 1}},
    "EL-9050": {"nombre": "E-Urbana 600", "unidades": {"M": 0, "L": 0},
                "reposicion": "2026-11-05"},
    "AN-8010": {"nombre": "Candado en U", "unidades": {"única": 12}},
}


class PruebasExistencias(unittest.TestCase):

    def setUp(self):
        self.existencias = copy.deepcopy(EXISTENCIAS)

    def test_unidades(self):
        self.assertEqual(unidades(self.existencias, "UR-5150", "M"), 3)
        self.assertEqual(unidades(self.existencias, "XX-0000", "M"), 0)
        self.assertTrue(hay_existencias(self.existencias, "AN-8010", "única", 12))

    def test_reservar(self):
        reservar(self.existencias, [{"ref": "UR-5150", "talla": "M", "cantidad": 2}])
        self.assertEqual(unidades(self.existencias, "UR-5150", "M"), 1)

    def test_reservar_sin_existencias(self):
        lineas = [{"ref": "AN-8010", "talla": "única", "cantidad": 1},
                  {"ref": "UR-5150", "talla": "L", "cantidad": 2}]
        with self.assertRaises(SinExistencias):
            reservar(self.existencias, lineas)
        self.assertEqual(unidades(self.existencias, "AN-8010", "única"), 12)

    def test_reponer(self):
        reponer(self.existencias, "UR-5150", "S", 2)
        reponer(self.existencias, "CA-4010", "M", 5, nombre="Casco Ciudad")
        self.assertEqual(unidades(self.existencias, "UR-5150", "S"), 2)
        self.assertEqual(self.existencias["CA-4010"]["nombre"], "Casco Ciudad")

    def test_tallas_agotadas(self):
        self.assertEqual(tallas_agotadas(self.existencias, "UR-5150"), ["S"])

    def test_agotados(self):
        self.assertIn("EL-9050", agotados(self.existencias))
        self.assertNotIn("AN-8010", agotados(self.existencias))
        self.assertNotIn("UR-5150", agotados(self.existencias))

    def test_informe(self):
        texto = informe_agotados({"EL-9050": EXISTENCIAS["EL-9050"]}, "2026-10-13")
        self.assertEqual(texto,
                         "EL-9050 E-Urbana 600: agotado, reposición el 05/11/2026")


if __name__ == "__main__":
    unittest.main()
