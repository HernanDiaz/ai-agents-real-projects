"""Tarea T22: lo que ha gastado un cliente."""
import unittest

import base_datos
from pedidos import total_cliente

PEDIDOS = {
    "CN-1": {"cliente": "CL-0001", "estado": "entregado", "importe": 100.1},
    "CN-2": {"cliente": "CL-0001", "estado": "enviado", "importe": 50.25},
    "CN-3": {"cliente": "CL-0001", "estado": "cancelado", "importe": 30},
    "CN-4": {"cliente": "CL-0002", "estado": "entregado", "importe": 99},
}


class PruebasT22(unittest.TestCase):

    def test_suma_sin_cancelados(self):
        self.assertEqual(total_cliente(PEDIDOS, "CL-0001"), 150.35)
        self.assertEqual(total_cliente(PEDIDOS, "CL-0002"), 99)

    def test_sin_pedidos(self):
        self.assertEqual(total_cliente(PEDIDOS, "CL-9999"), 0)

    def test_base_de_datos(self):
        pedidos = base_datos.pedidos()
        esperado = round(sum(p["importe"] for p in pedidos.values()
                             if p["cliente"] == "CL-0001" and p["estado"] != "cancelado"), 2)
        self.assertEqual(total_cliente(pedidos, "CL-0001"), esperado)
