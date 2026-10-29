"""Tarea T10: envíos a Portugal y Andorra."""
import unittest

from envios import fecha_entrega_estimada, gastos_envio, zona


class PruebasT10(unittest.TestCase):

    def test_zonas(self):
        self.assertEqual(zona("4000-123"), "portugal")
        self.assertEqual(zona("1100-148"), "portugal")
        self.assertEqual(zona("AD500"), "andorra")
        self.assertEqual(zona("33001"), "peninsula")
        self.assertEqual(zona("07800"), "baleares")

    def test_gastos_sin_envio_gratis(self):
        self.assertEqual(gastos_envio(30, "4000-123"), 11.95)
        self.assertEqual(gastos_envio(300, "4000-123"), 11.95)
        self.assertEqual(gastos_envio(300, "AD500"), 12.95)
        self.assertEqual(gastos_envio(300, "33001"), 0)

    def test_plazos(self):
        self.assertEqual(fecha_entrega_estimada("2026-10-09", "4000-123"),
                         ("2026-10-15", "2026-10-19"))
        self.assertEqual(fecha_entrega_estimada("2026-10-09", "AD500"),
                         ("2026-10-14", "2026-10-16"))


if __name__ == "__main__":
    unittest.main()
