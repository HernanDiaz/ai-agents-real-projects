"""Tarea T33: las decisiones de la tienda sobre el aviso de retraso."""
import unittest

from retrasos import aviso_retraso

CLIENTE = {"nombre": "Laura Gómez", "correo": "laura@correo.es", "ciudad": "Valladolid"}


def pedido(fecha):
    return {"cliente": "CL-0001", "estado": "retrasado",
            "motivo": "falta una pieza del proveedor", "entrega_prevista": fecha}


class CriterioT33(unittest.TestCase):

    def test_retraso_corto(self):
        self.assertIsNone(aviso_retraso("CN-1", pedido("2026-10-22"), CLIENTE, "2026-10-20"))
        self.assertIsNotNone(aviso_retraso("CN-1", pedido("2026-10-23"), CLIENTE,
                                           "2026-10-20"))

    def test_motivo_y_sin_promesas(self):
        texto = aviso_retraso("CN-1", pedido("2026-10-28"), CLIENTE, "2026-10-20")
        self.assertIn("falta una pieza del proveedor", texto)
        for palabra in ("descuento", "gratis", "regalo", "compens", "reembols"):
            self.assertNotIn(palabra, texto.lower())
