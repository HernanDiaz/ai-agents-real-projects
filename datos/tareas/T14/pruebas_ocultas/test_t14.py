"""Tarea T14: búsqueda por correo flexible e historial de pedidos."""
import unittest

import base_datos
from clientes import buscar_por_correo, pedidos_de_cliente


class PruebasT14(unittest.TestCase):

    def test_correo_flexible(self):
        clientes = base_datos.clientes()
        self.assertEqual(buscar_por_correo(clientes, "  LAURA.GOMEZ@correo.es "),
                         "CL-0001")
        self.assertEqual(buscar_por_correo(clientes, "ana.prieto@correo.es"), "CL-0008")
        self.assertIsNone(buscar_por_correo(clientes, "nadie@correo.es"))

    def test_historial(self):
        pedidos = base_datos.pedidos()
        self.assertEqual(pedidos_de_cliente(pedidos, "CL-0001"),
                         ["CN-11460", "CN-10482"])
        self.assertEqual(pedidos_de_cliente(pedidos, "CL-0009"), ["CN-11302"])
        self.assertEqual(pedidos_de_cliente(pedidos, "CL-0099"), [])


if __name__ == "__main__":
    unittest.main()
