"""Tarea T03: el envío solo se reembolsa si se devuelve el pedido completo."""
import unittest

from devoluciones import importe_reembolso

CASCOS = {"ref": "CA-4100", "nombre": "Casco Trail", "talla": "L", "cantidad": 2,
          "precio": 89}
LUCES = {"ref": "LU-6080", "nombre": "Kit Luces Ciudad", "talla": "única",
         "cantidad": 2, "precio": 25}


def pedido(lineas, envio):
    """Un pedido entregado con las líneas dadas."""
    return {"lineas": lineas, "envio": envio, "estado": "entregado",
            "fecha_entrega": "2026-10-01", "codigo_postal": "07002"}


class PruebasT03(unittest.TestCase):

    def test_una_de_dos_unidades(self):
        p = pedido([CASCOS], 9.95)
        self.assertEqual(importe_reembolso(p, [{"ref": "CA-4100", "cantidad": 1}]), 89)

    def test_todas_las_unidades(self):
        p = pedido([CASCOS], 9.95)
        self.assertEqual(importe_reembolso(p, [{"ref": "CA-4100", "cantidad": 2}]),
                         187.95)

    def test_en_varias_entradas(self):
        p = pedido([CASCOS], 9.95)
        devueltas = [{"ref": "CA-4100", "cantidad": 1},
                     {"ref": "CA-4100", "cantidad": 1}]
        self.assertEqual(importe_reembolso(p, devueltas), 187.95)

    def test_dos_lineas_a_medias(self):
        p = pedido([CASCOS, LUCES], 4.95)
        devueltas = [{"ref": "CA-4100", "cantidad": 1},
                     {"ref": "LU-6080", "cantidad": 1}]
        self.assertEqual(importe_reembolso(p, devueltas), 114)


if __name__ == "__main__":
    unittest.main()
