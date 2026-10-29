"""Tarea T19: devoluciones.py toma sus valores de config.py."""
import ast
import inspect
import unittest

import devoluciones


def constantes(modulo):
    """Las constantes que aparecen en el código de un módulo."""
    arbol = ast.parse(inspect.getsource(modulo))
    return [n.value for n in ast.walk(arbol) if isinstance(n, ast.Constant)]


class PruebasT19(unittest.TestCase):

    def test_sin_numeros_magicos(self):
        valores = constantes(devoluciones)
        numeros = [v for v in valores if isinstance(v, (int, float))
                   and not isinstance(v, bool)]
        self.assertNotIn(30, numeros)
        self.assertNotIn(10, numeros)
        self.assertNotIn("UR", valores)
        self.assertNotIn("MT", valores)

    def test_mismo_comportamiento(self):
        pedido = {"estado": "entregado", "fecha_entrega": "2026-09-17"}
        urbana = {"ref": "UR-5150"}
        self.assertTrue(devoluciones.se_puede_devolver(pedido, "2026-10-17"))
        self.assertFalse(devoluciones.se_puede_devolver(pedido, "2026-10-18"))
        self.assertTrue(devoluciones.es_bicicleta("EL-9010"))
        self.assertFalse(devoluciones.es_bicicleta("CA-4010"))
        self.assertIsNone(devoluciones.motivo_rechazo(pedido, urbana, "2026-10-01",
                                                      km=10))
        self.assertIn("10 km", devoluciones.motivo_rechazo(pedido, urbana, "2026-10-01",
                                                          km=11))
        self.assertIn("30 días", devoluciones.motivo_rechazo(pedido, urbana,
                                                            "2026-11-01"))


if __name__ == "__main__":
    unittest.main()
