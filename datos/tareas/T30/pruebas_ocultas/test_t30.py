"""Tarea T30: aviso de pago pendiente."""
import unittest

from avisos import aviso_pago_pendiente

LAURA = {"nombre": "Laura Gómez", "correo": "laura.gomez@correo.es"}
PEDIDO = {"importe": 1249.5, "fecha_pedido": "2026-10-08", "estado": "pendiente de pago",
          "pago": {"forma": "transferencia", "recibido": None}}


class PruebasT30(unittest.TestCase):

    def setUp(self):
        self.texto = aviso_pago_pendiente("CN-11460", PEDIDO, LAURA)

    def test_saludo_y_firma(self):
        self.assertTrue(self.texto.startswith("Hola, Laura:"))
        self.assertTrue(self.texto.endswith("Un saludo,\nCiclos Norte"))

    def test_datos(self):
        self.assertIn("CN-11460", self.texto)
        self.assertIn("1.249,50 €", self.texto)
        self.assertIn("13/10/2026", self.texto)
