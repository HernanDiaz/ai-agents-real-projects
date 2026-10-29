"""Tarea T21: los pedidos devueltos no son ventas."""
import unittest

from informes import pedidos_validos, ticket_medio, total_ventas

PEDIDOS = {
    "CN-1": {"estado": "entregado", "importe": 100},
    "CN-2": {"estado": "devuelto", "importe": 50},
    "CN-3": {"estado": "devolución en curso", "importe": 30},
    "CN-4": {"estado": "cancelado", "importe": 20},
}


class PruebasT21(unittest.TestCase):

    def test_validos(self):
        self.assertEqual(sorted(pedidos_validos(PEDIDOS)), ["CN-1", "CN-3"])

    def test_totales(self):
        self.assertEqual(total_ventas(PEDIDOS), 130)
        self.assertEqual(ticket_medio(PEDIDOS), 65)
