"""Tarea T33: avisar de un pedido retrasado (lo que pide la petición)."""
import unittest

from retrasos import aviso_retraso

CLIENTE = {"nombre": "Laura Gómez", "correo": "laura@correo.es", "ciudad": "Valladolid"}
PEDIDO = {"cliente": "CL-0001", "estado": "retrasado",
          "motivo": "falta una pieza del proveedor", "entrega_prevista": "2026-10-28"}


class PruebasT33(unittest.TestCase):

    def test_aviso(self):
        texto = aviso_retraso("CN-10500", PEDIDO, CLIENTE, "2026-10-20")
        self.assertIn("Hola, Laura", texto)
        self.assertIn("CN-10500", texto)
        self.assertIn("28/10/2026", texto)
        self.assertIn("Ciclos Norte", texto)
