"""Tarea T16: plazo de devolución ampliado en Navidad."""
import unittest

from avisos import aviso_entrega
from devoluciones import se_puede_devolver

LAURA = {"nombre": "Laura Gómez"}


def entregado(fecha):
    """Un pedido entregado en la fecha dada."""
    return {"estado": "entregado", "fecha_entrega": fecha, "lineas": [], "envio": 0,
            "codigo_postal": "33001"}


class PruebasT16(unittest.TestCase):

    def test_campana(self):
        self.assertTrue(se_puede_devolver(entregado("2026-12-10"), "2027-01-25"))
        self.assertTrue(se_puede_devolver(entregado("2026-12-10"), "2027-01-31"))
        self.assertFalse(se_puede_devolver(entregado("2026-12-10"), "2027-02-01"))
        self.assertTrue(se_puede_devolver(entregado("2026-11-15"), "2027-01-31"))
        self.assertTrue(se_puede_devolver(entregado("2026-12-28"), "2027-01-30"))

    def test_fuera_de_campana(self):
        self.assertTrue(se_puede_devolver(entregado("2026-11-14"), "2026-12-14"))
        self.assertFalse(se_puede_devolver(entregado("2026-11-14"), "2026-12-15"))
        self.assertTrue(se_puede_devolver(entregado("2027-01-05"), "2027-02-04"))
        self.assertFalse(se_puede_devolver(entregado("2027-01-05"), "2027-02-05"))

    def test_aviso(self):
        texto = aviso_entrega("CN-11600", {"fecha_entrega": "2026-11-20"}, LAURA)
        self.assertIn("hasta el 31/01/2027", texto)
        texto = aviso_entrega("CN-10482", {"fecha_entrega": "2026-09-17"}, LAURA)
        self.assertIn("hasta el 17/10/2026", texto)


if __name__ == "__main__":
    unittest.main()
