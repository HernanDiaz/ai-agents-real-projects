"""Pruebas de las facturas."""
import unittest

from facturas import (desglose_iva, factura, factura_rectificativa,
                      siguiente_numero_factura, texto_factura)

PEDIDO = {"lineas": [{"ref": "CA-4010", "nombre": "Casco Ciudad", "talla": "M",
                      "cantidad": 2, "precio": 49}],
          "envio": 0, "importe": 98, "pago": {"forma": "tarjeta"}}
CLIENTE = {"nombre": "Laura Gómez"}


class PruebasFacturas(unittest.TestCase):

    def test_base(self):
        self.assertEqual(desglose_iva(121)[0], 100)
        self.assertEqual(desglose_iva(589)[0], 486.78)

    def test_factura(self):
        datos = factura("F2026-0001", "CN-11500", PEDIDO, CLIENTE, "2026-10-13")
        self.assertEqual(datos["total"], 98)
        self.assertEqual(datos["base"], 80.99)

    def test_numeracion(self):
        self.assertEqual(siguiente_numero_factura(["F2026-0007"], "2026-10-13"),
                         "F2026-0008")

    def test_rectificativa(self):
        original = factura("F2026-0001", "CN-11500", PEDIDO, CLIENTE, "2026-10-13")
        rect = factura_rectificativa(original, 49, "R2026-0001", "2026-10-20")
        self.assertEqual(rect["total"], -49)

    def test_texto(self):
        texto = texto_factura(factura("F2026-0001", "CN-11500", PEDIDO, CLIENTE,
                                      "2026-10-13"))
        self.assertIn("Factura F2026-0001 · 13/10/2026", texto)
        self.assertIn("2 × Casco Ciudad", texto)
        self.assertIn("98,00 €", texto)


if __name__ == "__main__":
    unittest.main()
