"""Pruebas de los avisos a los clientes."""
import unittest

from avisos import (aviso_cancelacion, aviso_entrega, aviso_envio, aviso_retraso,
                    aviso_revision, destinatarios_promocion, promocion)

LAURA = {"nombre": "Laura Gómez", "publicidad": True}
RAUL = {"nombre": "Raúl Ortega", "publicidad": False}


class PruebasAvisos(unittest.TestCase):

    def test_envio(self):
        pedido = {"transportista": "Envíos Rápidos", "seguimiento": "ER-558201",
                  "entrega_prevista": "2026-10-10"}
        texto = aviso_envio("CN-10871", pedido, LAURA)
        self.assertTrue(texto.startswith("Hola, Laura:"))
        self.assertIn("ER-558201", texto)
        self.assertIn("10/10/2026", texto)
        self.assertTrue(texto.endswith("Un saludo,\nCiclos Norte"))

    def test_entrega(self):
        texto = aviso_entrega("CN-10482", {"fecha_entrega": "2026-09-17"}, LAURA)
        self.assertIn("hasta el 17/10/2026", texto)

    def test_retraso(self):
        pedido = {"motivo": "falta de existencias", "entrega_prevista": "2026-10-15"}
        self.assertIn("15/10/2026", aviso_retraso("CN-11302", pedido, LAURA))

    def test_cancelacion(self):
        pedido = {"motivo": "cancelado por el cliente", "importe": 89}
        self.assertIn("89,00 €", aviso_cancelacion("CN-11215", pedido, LAURA))

    def test_revision(self):
        self.assertIn("10/10/2026", aviso_revision(LAURA, "2026-04-10"))

    def test_promocion(self):
        self.assertEqual(destinatarios_promocion({"CL-1": LAURA, "CL-2": RAUL}),
                         ["CL-1"])
        self.assertIn("BAJA", promocion(LAURA, "Descuentos en cascos."))


if __name__ == "__main__":
    unittest.main()
