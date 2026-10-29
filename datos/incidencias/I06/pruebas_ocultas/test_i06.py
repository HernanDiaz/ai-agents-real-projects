"""Incidencia I06: no se reserva una hora ocupada."""
import unittest

from citas import reservar


def agenda(estado="pendiente"):
    return [{"id": "CT-0001", "fecha": "2026-10-19", "hora": "10:00", "veterinario": "V1",
             "mascota": "M-001", "motivo": "vacunación", "estado": estado}]


class PruebasI06(unittest.TestCase):

    def test_ocupada(self):
        citas = agenda()
        with self.assertRaises(ValueError):
            reservar(citas, "V1", "M-002", "2026-10-19", "10:00", "otitis")
        self.assertEqual(len(citas), 1)

    def test_cancelada_y_otro_veterinario(self):
        self.assertEqual(reservar(agenda("cancelada"), "V1", "M-002", "2026-10-19", "10:00",
                                  "otitis"), "CT-0002")
        self.assertEqual(reservar(agenda(), "V2", "M-002", "2026-10-19", "10:00", "otitis"),
                         "CT-0002")
