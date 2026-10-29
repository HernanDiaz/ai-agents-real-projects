"""Tarea T28: los pedidos retrasados se pueden cancelar."""
import unittest

import pedidos


class PruebasT28(unittest.TestCase):

    def test_retrasado(self):
        pedido = {"estado": "retrasado"}
        self.assertTrue(pedidos.se_puede_cancelar(pedido))
        pedidos.cancelar(pedido, "cancelado por la clienta", "2026-10-13")
        self.assertEqual(pedido["estado"], "cancelado")

    def test_enviado(self):
        self.assertFalse(pedidos.se_puede_cancelar({"estado": "enviado"}))
        self.assertFalse(pedidos.se_puede_cancelar({"estado": "entregado"}))
