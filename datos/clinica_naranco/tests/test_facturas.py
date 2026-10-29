import unittest

from facturas import desglose_iva, facturas_de, texto_factura, total

FACTURAS = [{"id": "F-0002", "dueno": "D-001", "fecha": "2026-10-18",
             "lineas": [{"concepto": "consulta", "importe": 35.0}]},
            {"id": "F-0001", "dueno": "D-001", "fecha": "2026-10-16",
             "lineas": [{"concepto": "vacuna polivalente", "importe": 38.0},
                        {"concepto": "desparasitación", "importe": 15.0}]},
            {"id": "F-0003", "dueno": "D-002", "fecha": "2026-10-17",
             "lineas": [{"concepto": "cura", "importe": 22.0}]}]


class PruebasFacturas(unittest.TestCase):

    def test_total(self):
        self.assertEqual(total(FACTURAS[1]["lineas"]), 53.0)

    def test_iva(self):
        self.assertEqual(desglose_iva(121.0), {"base": 100.0, "iva": 21.0})

    def test_de_un_dueno(self):
        self.assertEqual([f["id"] for f in facturas_de(FACTURAS, "D-001")],
                         ["F-0001", "F-0002"])

    def test_texto(self):
        texto = texto_factura(FACTURAS[1])
        self.assertIn("Factura F-0001 · 16/10/2026", texto)
        self.assertIn("53,00 €", texto)


if __name__ == "__main__":
    unittest.main()
