"""Incidencia I05: recordatorio de cita."""
import unittest

from avisos import recordatorio_cita

MARTA = {"nombre": "Marta Fernández", "correo": "marta11@correo.es", "avisos": "correo"}
LOLA = {"nombre": "Lola", "especie": "perro"}
CITA = {"id": "CT-0200", "fecha": "2026-10-21", "hora": "10:30", "veterinario": "V1",
        "mascota": "M-001", "motivo": "revisión anual", "estado": "pendiente"}


class PruebasI05(unittest.TestCase):

    def test_recordatorio(self):
        texto = recordatorio_cita(MARTA, LOLA, CITA)
        self.assertTrue(texto.startswith("Hola, Marta:"))
        self.assertIn("Lola", texto)
        self.assertIn("21/10/2026", texto)
        self.assertIn("10:30", texto)
        self.assertTrue(texto.endswith("Clínica Veterinaria Naranco"))
