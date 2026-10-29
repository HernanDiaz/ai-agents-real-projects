"""Incidencia I08: lo que ha pagado un dueño."""
import unittest

from facturas import total_dueno

FACTURAS = [{"id": "F-1", "dueno": "D-001", "fecha": "2026-10-01",
             "lineas": [{"concepto": "consulta", "importe": 35.0}]},
            {"id": "F-2", "dueno": "D-001", "fecha": "2026-10-15",
             "lineas": [{"concepto": "cura", "importe": 22.1},
                        {"concepto": "desparasitación", "importe": 15.05}]},
            {"id": "F-3", "dueno": "D-002", "fecha": "2026-10-10",
             "lineas": [{"concepto": "cura", "importe": 22.0}]},
            {"id": "F-4", "dueno": "D-001", "fecha": "2026-11-02",
             "lineas": [{"concepto": "consulta", "importe": 35.0}]}]


class PruebasI08(unittest.TestCase):

    def test_periodo(self):
        self.assertEqual(total_dueno(FACTURAS, "D-001", "2026-10-01", "2026-10-15"), 72.15)
        self.assertEqual(total_dueno(FACTURAS, "D-001", "2026-10-02", "2026-10-31"), 37.15)

    def test_vacio(self):
        self.assertEqual(total_dueno(FACTURAS, "D-003", "2026-01-01", "2026-12-31"), 0)
