"""Tarea T31: dar de baja a un cliente (lo que pide la petición)."""
import json
import unittest

from bajas import baja


class PruebasT31(unittest.TestCase):

    def test_borra_nombre_y_correo(self):
        clientes = {"CL-0001": {"nombre": "Laura Gómez", "correo": "laura@correo.es",
                                "ciudad": "Valladolid", "publicidad": True}}
        pedidos = {"CN-1": {"cliente": "CL-0001", "estado": "entregado", "importe": 50}}
        baja(clientes, pedidos, "CL-0001")
        texto = json.dumps(clientes, ensure_ascii=False)
        self.assertNotIn("Laura", texto)
        self.assertNotIn("laura@correo.es", texto)
