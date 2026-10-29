"""Tarea T20: los avisos se montan con componer() y no cambian."""
import inspect
import unittest

import avisos

LAURA = {"nombre": "Laura Gómez"}
PEDIDO = {"transportista": "Envíos Rápidos", "seguimiento": "ER-558201",
          "entrega_prevista": "2026-10-10", "fecha_entrega": "2026-09-17",
          "motivo": "cancelado por el cliente", "importe": 89}
ESPERADOS = {
    "envio": ("Hola, Laura:\n\nTu pedido CN-10871 ya está en camino con "
              "Envíos Rápidos. El número de seguimiento es ER-558201 y la "
              "entrega está prevista para el 10/10/2026.\n\nUn saludo,\nCiclos "
              "Norte"),
    "entrega": ("Hola, Laura:\n\nTu pedido CN-10482 se entregó el 17/09/2026. "
                "Si algo no te convence, puedes devolverlo hasta el "
                "17/10/2026.\n\nUn saludo,\nCiclos Norte"),
    "cancelacion": ("Hola, Laura:\n\nHemos cancelado tu pedido CN-11215 (cancelado "
                    "por el cliente). Te devolveremos 89,00 € en un máximo de 14 "
                    "días por el mismo medio de pago.\n\nUn saludo,\nCiclos Norte"),
    "revision": ("Hola, Laura:\n\nLa primera revisión de tu bicicleta es "
                 "gratuita hasta el 10/10/2026. Después, la revisión básica "
                 "cuesta 35 euros.\n\nUn saludo,\nCiclos Norte"),
    "promocion": ("Hola, Laura:\n\nCascos al 20 %.\n\nSi no quieres recibir más "
                  "correos como este, responde con la palabra BAJA.\n\nUn "
                  "saludo,\nCiclos Norte"),
}


class PruebasT20(unittest.TestCase):

    def test_componer(self):
        self.assertEqual(avisos.componer(LAURA, "Texto."),
                         "Hola, Laura:\n\nTexto.\n\nUn saludo,\nCiclos Norte")

    def test_saludo_y_firma_una_vez(self):
        codigo = inspect.getsource(avisos)
        self.assertEqual(codigo.count("Un saludo"), 1)
        self.assertEqual(codigo.count("Hola, "), 1)

    def test_textos_iguales(self):
        obtenidos = {
            "envio": avisos.aviso_envio("CN-10871", PEDIDO, LAURA),
            "entrega": avisos.aviso_entrega("CN-10482", PEDIDO, LAURA),
            "cancelacion": avisos.aviso_cancelacion("CN-11215", PEDIDO, LAURA),
            "revision": avisos.aviso_revision(LAURA, "2026-04-10"),
            "promocion": avisos.promocion(LAURA, "Cascos al 20 %."),
        }
        for clave, esperado in ESPERADOS.items():
            self.assertEqual(obtenidos[clave], esperado, clave)


if __name__ == "__main__":
    unittest.main()
