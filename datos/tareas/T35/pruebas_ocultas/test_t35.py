"""Tarea T35: descuento para los clientes que repiten (lo que pide la petición)."""
import unittest

from fidelidad import descuento_fidelidad

HOY = "2026-10-24"


def entregado(cliente, fecha):
    return {"cliente": cliente, "estado": "entregado", "importe": 80,
            "fecha_pedido": fecha, "fecha_entrega": fecha}


PEDIDOS = {f"CN-{n}": entregado("CL-0001", f"2026-0{n}-10") for n in range(1, 9)}


class PruebasT35(unittest.TestCase):

    def test_repite(self):
        self.assertGreater(descuento_fidelidad(PEDIDOS, "CL-0001", 400, HOY), 0)

    def test_nuevo(self):
        self.assertEqual(descuento_fidelidad(PEDIDOS, "CL-0099", 400, HOY), 0)
