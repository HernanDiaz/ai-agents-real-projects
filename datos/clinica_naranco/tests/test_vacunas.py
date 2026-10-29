import unittest

from vacunas import avisos_pendientes, proximas, vencidas

LOLA = [{"vacuna": "rabia", "ultima": "2025-08-22", "proxima": "2026-08-22"},
        {"vacuna": "leishmaniosis", "ultima": "2025-11-12", "proxima": "2026-11-12"},
        {"vacuna": "polivalente", "ultima": "2026-03-01", "proxima": "2027-03-01"}]


class PruebasVacunas(unittest.TestCase):

    def test_vencidas(self):
        self.assertEqual(vencidas(LOLA, "2026-10-20"), ["rabia"])

    def test_proximas(self):
        self.assertEqual(proximas(LOLA, "2026-10-20"), ["leishmaniosis"])
        self.assertEqual(proximas(LOLA, "2026-10-20", dias=10), [])

    def test_avisos(self):
        self.assertEqual(avisos_pendientes({"M-001": LOLA}, "2026-10-20"),
                         {"M-001": ["rabia", "leishmaniosis"]})


if __name__ == "__main__":
    unittest.main()
