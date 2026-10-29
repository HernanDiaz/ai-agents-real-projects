"""Pruebas de las facturas."""
import unittest

from facturas import desglose_iva, factura, texto_factura

PEDIDO = {"lineas": [{"ref": "CA-4010", "nombre": "Casco Ciudad", "talla": "M",
                      "cantidad": 2, "precio": 49}],
          "envio": 0, "importe": 98, "pago": {"forma": "tarjeta"}}
CLIENTE = {"nombre": "Laura Gómez"}


class PruebasFacturas(unittest.TestCase):

    def test_base(self):
        self.assertEqual(desglose_iva(121)[0], 100)
        self.assertEqual(desglose_iva(589)[0], 486.78)
        self.assertEqual(desglose_iva(121), (100, 21))

    def test_factura(self):
        datos = factura("F2026-0001", "CN-11500", PEDIDO, CLIENTE, "2026-10-13")
        self.assertEqual(datos["total"], 98)
        self.assertEqual(datos["base"], 80.99)

    def test_texto(self):
        texto = texto_factura(factura("F2026-0001", "CN-11500", PEDIDO, CLIENTE,
                                      "2026-10-13"))
        self.assertIn("Factura F2026-0001 · 13/10/2026", texto)
        self.assertIn("2 × Casco Ciudad", texto)
        self.assertIn("98,00 €", texto)


if __name__ == "__main__":
    unittest.main()
