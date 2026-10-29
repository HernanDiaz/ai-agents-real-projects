"""Pruebas de las zonas y los gastos de envío."""
import unittest

from envios import fecha_entrega_estimada, gastos_envio, zona


class PruebasEnvios(unittest.TestCase):

    def test_zona(self):
        self.assertEqual(zona("33001"), "peninsula")
        self.assertEqual(zona("07800"), "baleares")
        self.assertEqual(zona("35001"), "canarias")

    def test_gastos_peninsula(self):
        self.assertEqual(gastos_envio(30, "33001"), 4.95)
        self.assertEqual(gastos_envio(50, "33001"), 4.95)
        self.assertEqual(gastos_envio(50.01, "33001"), 0)

    def test_gastos_islas(self):
        self.assertEqual(gastos_envio(20, "07800"), 9.95)
        self.assertEqual(gastos_envio(35, "38001"), 14.95)
        self.assertEqual(gastos_envio(120, "07800"), 9.95)

    def test_entrega_estimada(self):
        # Sale un viernes: llega entre el martes y el miércoles en la península.
        self.assertEqual(fecha_entrega_estimada("2026-10-09", "33001"),
                         ("2026-10-13", "2026-10-14"))


if __name__ == "__main__":
    unittest.main()
