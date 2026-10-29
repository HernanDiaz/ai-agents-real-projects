"""Tarea T08: sin consentimiento expreso no hay publicidad."""
import unittest

import base_datos
from avisos import destinatarios_promocion
from clientes import acepta_publicidad


class PruebasT08(unittest.TestCase):

    def test_sin_campo(self):
        self.assertFalse(acepta_publicidad({"nombre": "Carmen Díez"}))
        self.assertTrue(acepta_publicidad({"nombre": "Laura", "publicidad": True}))

    def test_destinatarios(self):
        self.assertEqual(destinatarios_promocion(base_datos.clientes()),
                         ["CL-0001", "CL-0003", "CL-0005", "CL-0008", "CL-0010",
                          "CL-0012"])


if __name__ == "__main__":
    unittest.main()
