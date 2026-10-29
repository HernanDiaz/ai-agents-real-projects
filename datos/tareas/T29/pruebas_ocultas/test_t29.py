"""Tarea T29: los gastos de envío en el resumen del pedido."""
import unittest

import pedidos

LINEA = {"ref": "LU-6010", "nombre": "Luz Delantera 800", "talla": "única",
         "cantidad": 1, "precio": 45}


class PruebasT29(unittest.TestCase):

    def test_con_envio(self):
        pedido = {"estado": "enviado", "lineas": [LINEA], "envio": 4.95, "importe": 49.95}
        self.assertEqual(pedidos.resumen("CN-1", pedido),
                         "CN-1 · enviado · 1 × Luz Delantera 800 · 49,95 € (envío 4,95 €)")

    def test_sin_envio(self):
        pedido = {"estado": "enviado", "lineas": [LINEA], "envio": 0, "importe": 45}
        self.assertEqual(pedidos.resumen("CN-1", pedido),
                         "CN-1 · enviado · 1 × Luz Delantera 800 · 45,00 €")
