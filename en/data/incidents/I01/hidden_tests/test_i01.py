"""Incident I01: no slots on weekends."""
import unittest

from appointments import free_slots


class I01Tests(unittest.TestCase):

    def test_weekend(self):
        self.assertEqual(free_slots([], "V1", "2026-10-24"), [])
        self.assertEqual(free_slots([], "V1", "2026-10-25"), [])

    def test_weekday(self):
        self.assertEqual(len(free_slots([], "V1", "2026-10-23")), 10)
