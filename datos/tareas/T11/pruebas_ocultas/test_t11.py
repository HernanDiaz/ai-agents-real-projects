"""Tarea T11: aviso de pedido retrasado."""
import unittest

import base_datos
from avisos import aviso_retraso


class PruebasT11(unittest.TestCase):

    def test_pedido_de_ejemplo(self):
        pedido = base_datos.pedidos()["CN-11302"]
        cliente = base_datos.clientes()[pedido["cliente"]]
        self.assertEqual(
            aviso_retraso("CN-11302", pedido, cliente),
            "Hola, Javier:\n\nTu pedido CN-11302 se ha retrasado por falta de "
            "existencias en la talla L. La nueva fecha prevista de entrega es el "
            "15/10/2026. Sentimos las molestias.\n\nUn saludo,\nCiclos Norte")

    def test_otro_motivo(self):
        pedido = {"motivo": "un problema con el transportista",
                  "entrega_prevista": "2026-11-02"}
        texto = aviso_retraso("CN-11500", pedido, {"nombre": "Ana Prieto"})
        self.assertIn("se ha retrasado por un problema con el transportista.", texto)
        self.assertIn("es el 02/11/2026.", texto)
        self.assertTrue(texto.startswith("Hola, Ana:"))


if __name__ == "__main__":
    unittest.main()
