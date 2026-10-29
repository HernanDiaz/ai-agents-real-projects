"""Tarea T31: las decisiones de la tienda al dar de baja a un cliente."""
import unittest

from bajas import baja


def datos(estado="entregado"):
    clientes = {"CL-0001": {"nombre": "Laura Gómez", "correo": "laura@correo.es",
                            "ciudad": "Valladolid", "publicidad": True}}
    pedidos = {"CN-1": {"cliente": "CL-0001", "estado": estado, "importe": 50}}
    return clientes, pedidos


class CriterioT31(unittest.TestCase):

    def test_no_borra_al_cliente(self):
        clientes, pedidos = datos()
        self.assertEqual(baja(clientes, pedidos, "CL-0001"), "hecho")
        self.assertIn("CL-0001", clientes)
        self.assertEqual(clientes["CL-0001"]["ciudad"], "Valladolid")
        self.assertFalse(clientes["CL-0001"]["publicidad"])

    def test_pedido_en_curso(self):
        for estado in ("pendiente de pago", "en preparación", "enviado", "retrasado",
                       "devolución en curso"):
            clientes, pedidos = datos(estado)
            self.assertEqual(baja(clientes, pedidos, "CL-0001"), "pendiente", estado)
            self.assertEqual(clientes["CL-0001"]["nombre"], "Laura Gómez", estado)
