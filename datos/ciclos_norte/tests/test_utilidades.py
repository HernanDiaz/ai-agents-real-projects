"""Pruebas de las utilidades de fechas e importes."""
import unittest

from utilidades import (dias_entre, formato_euros, formato_fecha, redondear,
                        sumar_dias, sumar_dias_laborables, sumar_meses)


class PruebasUtilidades(unittest.TestCase):

    def test_dias(self):
        self.assertEqual(dias_entre("2026-09-17", "2026-10-13"), 26)
        self.assertEqual(sumar_dias("2026-09-17", 30), "2026-10-17")

    def test_laborables(self):
        # El 2026-10-09 es viernes: dos días laborables después es martes.
        self.assertEqual(sumar_dias_laborables("2026-10-09", 2), "2026-10-13")

    def test_meses(self):
        self.assertEqual(sumar_meses("2026-04-10", 6), "2026-10-10")
        self.assertEqual(sumar_meses("2026-08-31", 6), "2027-02-28")

    def test_importes(self):
        self.assertEqual(redondear(2.345), 2.35)
        self.assertEqual(formato_euros(1234.5), "1.234,50 €")
        self.assertEqual(formato_euros(4.95), "4,95 €")

    def test_formato_fecha(self):
        self.assertEqual(formato_fecha("2026-10-15"), "15/10/2026")


if __name__ == "__main__":
    unittest.main()
