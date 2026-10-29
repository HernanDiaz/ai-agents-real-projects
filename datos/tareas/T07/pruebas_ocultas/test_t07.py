"""Tarea T07: los seis meses de revisión gratuita son meses de calendario."""
import unittest

from presupuestos import precio_revision, revision_gratuita


class PruebasT07(unittest.TestCase):

    def test_dentro_de_los_seis_meses(self):
        self.assertTrue(revision_gratuita(True, "2026-04-10", "2026-10-08"))
        self.assertTrue(revision_gratuita(True, "2026-04-10", "2026-10-10"))
        self.assertTrue(revision_gratuita(True, "2026-01-31", "2026-07-30"))
        self.assertTrue(revision_gratuita(True, "2026-08-31", "2027-02-28"))

    def test_fuera(self):
        self.assertFalse(revision_gratuita(True, "2026-04-10", "2026-10-11"))
        self.assertFalse(revision_gratuita(True, "2026-08-31", "2027-03-01"))
        self.assertFalse(revision_gratuita(False, "2026-04-10", "2026-10-08"))

    def test_precio(self):
        self.assertEqual(precio_revision(True, "2026-04-10", "2026-10-08"), 0)


if __name__ == "__main__":
    unittest.main()
