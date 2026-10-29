"""Pruebas de los informes, con la base de datos de ejemplo."""
import unittest

import base_datos
from informes import (informe_mensual, pedidos_del_mes, recuento_por_estado,
                      ticket_medio, total_ventas, ventas_por_categoria)


class PruebasInformes(unittest.TestCase):

    def setUp(self):
        self.pedidos = base_datos.pedidos()

    def test_ventas_sin_cancelados(self):
        octubre = pedidos_del_mes(self.pedidos, 2026, 10)
        self.assertEqual(len(octubre), 8)
        self.assertEqual(total_ventas(octubre), 2209.85)

    def test_ticket_medio(self):
        self.assertEqual(ticket_medio({}), 0)
        septiembre = pedidos_del_mes(self.pedidos, 2026, 9)
        self.assertEqual(ticket_medio(septiembre), 528.4)

    def test_categorias(self):
        ventas = ventas_por_categoria(self.pedidos, base_datos.catalogo())
        self.assertEqual(next(iter(ventas)), "bicicletas eléctricas")

    def test_recuento(self):
        self.assertEqual(recuento_por_estado(self.pedidos)["cancelado"], 1)

    def test_informe(self):
        self.assertIn("Informe de 10/2026", informe_mensual(2026, 10))


if __name__ == "__main__":
    unittest.main()
