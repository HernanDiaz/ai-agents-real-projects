"""Tarea T18: una sola función para contar días."""
import inspect
import unittest

import devoluciones
import pedidos
import presupuestos


class PruebasT18(unittest.TestCase):

    def test_sin_copias(self):
        for modulo in (pedidos, devoluciones, presupuestos):
            self.assertFalse(hasattr(modulo, "_dias_entre"), modulo.__name__)
            self.assertNotIn("fromisoformat", inspect.getsource(modulo),
                             modulo.__name__)

    def test_mismo_comportamiento(self):
        entregado = {"estado": "entregado", "fecha_entrega": "2026-09-17"}
        self.assertTrue(devoluciones.se_puede_devolver(entregado, "2026-10-17"))
        self.assertFalse(devoluciones.se_puede_devolver(entregado, "2026-10-18"))
        pedido = {"pago": {"forma": "transferencia", "recibido": None},
                  "fecha_pedido": "2026-10-01"}
        self.assertFalse(pedidos.transferencia_caducada(pedido, "2026-10-06"))
        self.assertTrue(pedidos.transferencia_caducada(pedido, "2026-10-07"))
        self.assertTrue(presupuestos.revision_gratuita(True, "2026-05-01",
                                                       "2026-08-01"))
        self.assertFalse(presupuestos.revision_gratuita(True, "2025-12-01",
                                                        "2026-08-01"))


if __name__ == "__main__":
    unittest.main()
