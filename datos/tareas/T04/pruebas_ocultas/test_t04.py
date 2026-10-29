"""Tarea T04: la base más el IVA suman el total."""
import unittest

from facturas import desglose_iva, factura


class PruebasT04(unittest.TestCase):

    def test_casos_conocidos(self):
        self.assertEqual(desglose_iva(121), (100.0, 21.0))
        self.assertEqual(desglose_iva(589), (486.78, 102.22))

    def test_suman_el_total(self):
        for total in (49.95, 98, 1649, 0.99, 2190, 53.95):
            base, cuota = desglose_iva(total)
            self.assertEqual(round(base + cuota, 2), total, total)

    def test_factura(self):
        pedido = {"lineas": [], "envio": 0, "importe": 74, "pago": {}}
        datos = factura("F2026-0001", "CN-10871", pedido, {"nombre": "Lucía Ríos"},
                        "2026-10-13")
        self.assertEqual(round(datos["base"] + datos["iva"], 2), 74)


if __name__ == "__main__":
    unittest.main()
