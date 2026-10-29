"""Tarea T12: numeración correlativa y facturas rectificativas."""
import unittest

from facturas import (desglose_iva, factura, factura_rectificativa,
                      siguiente_numero_factura, texto_factura)

PEDIDO = {"lineas": [{"ref": "UR-5150", "nombre": "Urbana 5", "talla": "M",
                      "cantidad": 1, "precio": 589}],
          "envio": 0, "importe": 589, "pago": {"forma": "tarjeta"}}


class PruebasT12(unittest.TestCase):

    def test_numeracion(self):
        self.assertEqual(siguiente_numero_factura([], "2026-10-13"), "F2026-0001")
        emitidas = ["F2026-0007", "F2026-0012", "F2025-0450", "R2026-0003"]
        self.assertEqual(siguiente_numero_factura(emitidas, "2026-10-13"),
                         "F2026-0013")
        self.assertEqual(siguiente_numero_factura(emitidas, "2027-01-02"),
                         "F2027-0001")
        self.assertEqual(siguiente_numero_factura(emitidas, "2026-10-13", serie="R"),
                         "R2026-0004")

    def test_rectificativa(self):
        original = factura("F2026-0007", "CN-10482", PEDIDO, {"nombre": "Laura Gómez"},
                           "2026-09-14")
        rect = factura_rectificativa(original, 589, "R2026-0001", "2026-10-20")
        base, cuota = desglose_iva(589)
        self.assertEqual(rect["numero"], "R2026-0001")
        self.assertEqual(rect["rectifica"], "F2026-0007")
        self.assertEqual(rect["cliente"], "Laura Gómez")
        self.assertEqual(rect["pedido"], "CN-10482")
        self.assertEqual((rect["total"], rect["base"], rect["iva"]),
                         (-589, -base, -cuota))
        texto = texto_factura(rect)
        self.assertIn("R2026-0001", texto)
        self.assertIn("-589,00 €", texto)


if __name__ == "__main__":
    unittest.main()
