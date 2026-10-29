"""Tarea T26: la talla en las líneas de la factura."""
import unittest

from facturas import factura, texto_factura

CASCO = {"ref": "CA-4010", "nombre": "Casco Ciudad", "talla": "M", "cantidad": 1,
         "precio": 49}
LUCES = {"ref": "LU-6080", "nombre": "Kit Luces Ciudad", "talla": "única",
         "cantidad": 2, "precio": 25}
PEDIDO = {"lineas": [CASCO, LUCES], "envio": 0, "importe": 99}


class PruebasT26(unittest.TestCase):

    def setUp(self):
        self.texto = texto_factura(factura("F2026-0001", "CN-1", PEDIDO,
                                           {"nombre": "Laura Gómez"}, "2026-10-13"))

    def test_talla(self):
        self.assertIn("1 × Casco Ciudad (M)", self.texto)

    def test_talla_unica(self):
        self.assertIn("2 × Kit Luces Ciudad ", self.texto)
        self.assertNotIn("(única)", self.texto)
