"""Pruebas de las devoluciones."""
import unittest

from devoluciones import (coste_recogida, fecha_limite_reembolso, importe_reembolso,
                          motivo_rechazo, registrar_devolucion, resumen_devolucion,
                          se_puede_devolver)

HOY = "2026-10-13"
URBANA = {"ref": "UR-5150", "nombre": "Urbana 5", "talla": "M", "cantidad": 1,
          "precio": 589}
CASCO = {"ref": "CA-4010", "nombre": "Casco Ciudad", "talla": "M", "cantidad": 1,
         "precio": 49}
LUCES = {"ref": "LU-6080", "nombre": "Kit Luces Ciudad", "talla": "única",
         "cantidad": 1, "precio": 25}


def pedido(lineas, envio=0, entrega="2026-09-17", estado="entregado", cp="47001"):
    """Un pedido de prueba con las líneas dadas."""
    return {"lineas": lineas, "envio": envio, "estado": estado,
            "fecha_entrega": entrega, "codigo_postal": cp}


class PruebasDevoluciones(unittest.TestCase):

    def test_plazo(self):
        self.assertTrue(se_puede_devolver(pedido([URBANA]), HOY))
        self.assertTrue(se_puede_devolver(pedido([URBANA]), "2026-10-17"))
        self.assertFalse(se_puede_devolver(pedido([URBANA]), "2026-10-18"))

    def test_no_entregado(self):
        self.assertFalse(se_puede_devolver(pedido([URBANA], estado="enviado"), HOY))

    def test_motivos(self):
        self.assertIsNone(motivo_rechazo(pedido([URBANA]), URBANA, HOY, km=4))
        self.assertIn("km", motivo_rechazo(pedido([URBANA]), URBANA, HOY, km=25))
        culote = {"ref": "RO-2050", "nombre": "Culote Pro", "talla": "M",
                  "cantidad": 1, "precio": 79}
        self.assertIn("higiene", motivo_rechazo(pedido([culote]), culote, HOY,
                                                desprecintado=True))

    def test_reembolso_parcial(self):
        p = pedido([CASCO, LUCES], envio=4.95)
        self.assertEqual(importe_reembolso(p, [{"ref": "CA-4010", "cantidad": 1}]), 49)

    def test_reembolso_completo(self):
        p = pedido([CASCO, LUCES], envio=4.95)
        devueltas = [{"ref": "CA-4010", "cantidad": 1},
                     {"ref": "LU-6080", "cantidad": 1}]
        self.assertEqual(importe_reembolso(p, devueltas), 78.95)

    def test_recogida(self):
        self.assertEqual(coste_recogida(pedido([CASCO])), 0)
        self.assertEqual(coste_recogida(pedido([CASCO], cp="38001")), 14.95)

    def test_reembolso_en_14_dias(self):
        self.assertEqual(fecha_limite_reembolso("2026-10-20"), "2026-11-03")

    def test_registrar(self):
        existencias = {"CA-4010": {"nombre": "Casco Ciudad", "unidades": {"M": 0}}}
        p = pedido([CASCO])
        registrar_devolucion(p, [{"ref": "CA-4010", "cantidad": 1}], HOY, existencias)
        self.assertEqual(p["estado"], "devolución en curso")
        self.assertEqual(existencias["CA-4010"]["unidades"]["M"], 1)

    def test_resumen(self):
        p = pedido([URBANA])
        devueltas = [{"ref": "UR-5150", "cantidad": 1}]
        self.assertEqual(
            resumen_devolucion("CN-10482", p, devueltas, HOY),
            "Devolución del pedido CN-10482 aceptada: se reembolsarán 589,00 €.")
        self.assertEqual(resumen_devolucion("CN-10482", p, devueltas, "2026-11-30"),
                         "El pedido CN-10482 no se puede devolver.")


if __name__ == "__main__":
    unittest.main()
