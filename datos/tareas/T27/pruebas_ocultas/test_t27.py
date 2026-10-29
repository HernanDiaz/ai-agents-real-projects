"""Tarea T27: los clientes con más pedidos."""
import unittest

from informes import clientes_con_mas_pedidos

PEDIDOS = {
    "CN-1": {"cliente": "CL-0003", "estado": "entregado"},
    "CN-2": {"cliente": "CL-0003", "estado": "enviado"},
    "CN-3": {"cliente": "CL-0001", "estado": "entregado"},
    "CN-4": {"cliente": "CL-0002", "estado": "entregado"},
    "CN-5": {"cliente": "CL-0002", "estado": "cancelado"},
    "CN-6": {"cliente": "CL-0004", "estado": "cancelado"},
}


class PruebasT27(unittest.TestCase):

    def test_orden(self):
        self.assertEqual(clientes_con_mas_pedidos(PEDIDOS),
                         [("CL-0003", 2), ("CL-0001", 1), ("CL-0002", 1)])

    def test_n(self):
        self.assertEqual(clientes_con_mas_pedidos(PEDIDOS, n=1), [("CL-0003", 2)])
