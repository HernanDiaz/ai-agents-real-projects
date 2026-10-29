"""Pruebas de los clientes."""
import unittest

from clientes import acepta_publicidad, alta, buscar_por_correo, correo_valido

CLIENTES = {
    "CL-0001": {"nombre": "Laura Gómez", "correo": "laura.gomez@correo.es",
                "ciudad": "Valladolid", "publicidad": True},
    "CL-0002": {"nombre": "Raúl Ortega", "correo": "raul.ortega@correo.es",
                "ciudad": "León", "publicidad": False},
}


class PruebasClientes(unittest.TestCase):

    def test_correo(self):
        self.assertTrue(correo_valido("ana@correo.es"))
        self.assertFalse(correo_valido("ana@correo"))

    def test_buscar(self):
        self.assertEqual(buscar_por_correo(CLIENTES, "raul.ortega@correo.es"),
                         "CL-0002")
        self.assertIsNone(buscar_por_correo(CLIENTES, "nadie@correo.es"))
        self.assertEqual(buscar_por_correo(CLIENTES, " Laura.Gomez@correo.es"),
                         "CL-0001")

    def test_alta(self):
        clientes = dict(CLIENTES)
        nuevo = alta(clientes, "Iván Ruiz", "ivan@correo.es", "Avilés")
        self.assertEqual(nuevo, "CL-0003")
        self.assertFalse(clientes[nuevo]["publicidad"])
        with self.assertRaises(ValueError):
            alta(clientes, "Otro", "ivan@correo.es", "Avilés")

    def test_publicidad(self):
        self.assertTrue(acepta_publicidad(CLIENTES["CL-0001"]))
        self.assertFalse(acepta_publicidad(CLIENTES["CL-0002"]))


if __name__ == "__main__":
    unittest.main()
