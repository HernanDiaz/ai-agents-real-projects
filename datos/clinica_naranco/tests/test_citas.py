import unittest

from citas import cancelar, citas_del_dia, horas_de_consulta, huecos_libres, reservar


def agenda():
    return [{"id": "CT-0001", "fecha": "2026-10-19", "hora": "09:30", "veterinario": "V1",
             "mascota": "M-001", "motivo": "vacunación", "estado": "pendiente"},
            {"id": "CT-0002", "fecha": "2026-10-19", "hora": "10:00", "veterinario": "V1",
             "mascota": "M-002", "motivo": "otitis", "estado": "realizada"}]


class PruebasCitas(unittest.TestCase):

    def test_horas(self):
        horas = horas_de_consulta()
        self.assertEqual(horas[0], "09:00")
        self.assertEqual(horas[-1], "13:30")
        self.assertEqual(len(horas), 10)

    def test_huecos(self):
        libres = huecos_libres(agenda(), "V1", "2026-10-19")
        self.assertNotIn("09:30", libres)
        self.assertNotIn("10:00", libres)
        self.assertIn("09:00", libres)
        self.assertEqual(len(huecos_libres(agenda(), "V2", "2026-10-19")), 10)

    def test_reservar(self):
        citas = agenda()
        nueva = reservar(citas, "V2", "M-003", "2026-10-20", "11:00", "cojera")
        self.assertEqual(nueva, "CT-0003")
        self.assertEqual(citas[-1]["estado"], "pendiente")
        with self.assertRaises(ValueError):
            reservar(citas, "V2", "M-003", "2026-10-20", "15:00", "cojera")

    def test_cancelar(self):
        citas = agenda()
        self.assertEqual(cancelar(citas, "CT-0001")["estado"], "cancelada")
        with self.assertRaises(ValueError):
            cancelar(citas, "CT-0002")
        self.assertEqual([c["id"] for c in citas_del_dia(citas, "2026-10-19")], ["CT-0002"])


if __name__ == "__main__":
    unittest.main()
