"""Incidencia I02: la vacuna que vence hoy está vencida."""
import unittest

from vacunas import proximas, vencidas

LOLA = [{"vacuna": "rabia", "ultima": "2025-10-20", "proxima": "2026-10-20"},
        {"vacuna": "leishmaniosis", "ultima": "2025-11-12", "proxima": "2026-11-12"}]


class PruebasI02(unittest.TestCase):

    def test_vence_hoy(self):
        self.assertEqual(vencidas(LOLA, "2026-10-20"), ["rabia"])
        self.assertEqual(proximas(LOLA, "2026-10-20"), ["leishmaniosis"])
