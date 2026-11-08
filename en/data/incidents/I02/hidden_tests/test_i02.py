"""Incident I02: the vaccine due today is overdue."""
import unittest

from vaccines import overdue, upcoming

LOLA = [{"vaccine": "rabies", "last": "2025-10-20", "next": "2026-10-20"},
        {"vaccine": "leptospirosis", "last": "2025-11-12", "next": "2026-11-12"}]


class I02Tests(unittest.TestCase):

    def test_due_today(self):
        self.assertEqual(overdue(LOLA, "2026-10-20"), ["rabies"])
        self.assertEqual(upcoming(LOLA, "2026-10-20"), ["leptospirosis"])
