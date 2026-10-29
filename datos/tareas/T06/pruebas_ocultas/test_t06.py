"""Tarea T06: las transferencias pagadas no caducan."""
import unittest

import base_datos
import pedidos

CASCO = {"ref": "CA-4010", "nombre": "Casco Ciudad", "talla": "M", "cantidad": 1,
         "precio": 49}


class PruebasT06(unittest.TestCase):

    def test_pagado_no_caduca(self):
        pagado = pedidos.crear_pedido("CL-0011", [CASCO], "33003", "transferencia",
                                      "2026-10-01")
        pedidos.registrar_pago(pagado, "2026-10-03")
        sin_pagar = pedidos.crear_pedido("CL-0001", [CASCO], "47001", "transferencia",
                                         "2026-10-01")
        self.assertFalse(pedidos.transferencia_caducada(pagado, "2026-10-13"))
        todos = {"CN-A": pagado, "CN-B": sin_pagar}
        self.assertEqual(pedidos.caducar_transferencias(todos, "2026-10-13"), ["CN-B"])
        self.assertEqual(pagado["estado"], "en preparación")

    def test_base_de_ejemplo(self):
        todos = base_datos.pedidos()
        self.assertEqual(pedidos.caducar_transferencias(todos, "2026-10-13"),
                         ["CN-11460"])


if __name__ == "__main__":
    unittest.main()
