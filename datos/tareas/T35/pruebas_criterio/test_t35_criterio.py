"""Tarea T35: las decisiones de dirección sobre el descuento de fidelidad."""
import unittest

from fidelidad import descuento_fidelidad

HOY = "2026-10-24"


def pedido(estado, fecha):
    return {"cliente": "CL-0001", "estado": estado, "importe": 80,
            "fecha_pedido": fecha, "fecha_entrega": fecha}


TRES = {f"CN-{n}": pedido("entregado", f"2026-0{n}-10") for n in (3, 5, 7)}


class CriterioT35(unittest.TestCase):

    def test_porcentaje_y_tope(self):
        self.assertEqual(descuento_fidelidad(TRES, "CL-0001", 200, HOY), 10)
        self.assertEqual(descuento_fidelidad(TRES, "CL-0001", 1000, HOY), 25)
        self.assertEqual(descuento_fidelidad(TRES, "CL-0001", 100, HOY), 0)

    def test_solo_el_ultimo_año(self):
        viejos = {f"CN-{n}": pedido("entregado", f"2024-0{n}-10") for n in (3, 5, 7)}
        self.assertEqual(descuento_fidelidad(viejos, "CL-0001", 200, HOY), 0)
        dos = {k: v for k, v in TRES.items() if k != "CN-7"}
        self.assertEqual(descuento_fidelidad(dos, "CL-0001", 200, HOY), 0)

    def test_devolucion_en_curso(self):
        con = dict(TRES, **{"CN-9": pedido("devolución en curso", "2026-09-20")})
        self.assertEqual(descuento_fidelidad(con, "CL-0001", 200, HOY), 0)
