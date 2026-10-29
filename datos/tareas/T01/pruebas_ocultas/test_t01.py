"""Tarea T01: el envío gratis solo se aplica en la península."""
import unittest

import pedidos
from envios import gastos_envio


class PruebasT01(unittest.TestCase):

    def test_islas_pagan_siempre(self):
        self.assertEqual(gastos_envio(120, "07800"), 9.95)
        self.assertEqual(gastos_envio(51, "35001"), 14.95)
        self.assertEqual(gastos_envio(2000, "38001"), 14.95)

    def test_peninsula_sigue_gratis(self):
        self.assertEqual(gastos_envio(120, "33001"), 0)
        self.assertEqual(gastos_envio(50, "33001"), 4.95)

    def test_pedido_a_ibiza(self):
        linea = {"ref": "AL-3500", "nombre": "Alforjas Viaje 40", "talla": "única",
                 "cantidad": 1, "precio": 99}
        pedido = pedidos.crear_pedido("CL-0012", [linea], "07800", "tarjeta",
                                      "2026-10-13")
        self.assertEqual(pedido["importe"], 108.95)


if __name__ == "__main__":
    unittest.main()
