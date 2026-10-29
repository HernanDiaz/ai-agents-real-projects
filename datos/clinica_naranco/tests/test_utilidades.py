import unittest

from utilidades import dia_de_la_semana, formato_euros, hora, minutos, redondear


class PruebasUtilidades(unittest.TestCase):

    def test_euros(self):
        self.assertEqual(formato_euros(1234.5), "1.234,50 €")
        self.assertEqual(redondear(2.345), 2.35)

    def test_horas(self):
        self.assertEqual(minutos("09:30"), 570)
        self.assertEqual(hora(570), "09:30")

    def test_dia(self):
        self.assertEqual(dia_de_la_semana("2026-10-19"), 0)


if __name__ == "__main__":
    unittest.main()
