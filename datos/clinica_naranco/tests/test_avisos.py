import unittest

from avisos import recordatorio_vacuna

MARTA = {"nombre": "Marta Fernández", "telefono": "687016831", "correo": "marta11@correo.es",
         "avisos": "correo"}
LOLA = {"nombre": "Lola", "especie": "perro"}


class PruebasAvisos(unittest.TestCase):

    def test_recordatorio_vacuna(self):
        texto = recordatorio_vacuna(MARTA, LOLA, {"vacuna": "rabia", "proxima": "2026-11-02"})
        self.assertTrue(texto.startswith("Hola, Marta:"))
        self.assertIn("A Lola le toca la vacuna de rabia el 02/11/2026", texto)
        self.assertTrue(texto.endswith("Clínica Veterinaria Naranco"))


if __name__ == "__main__":
    unittest.main()
