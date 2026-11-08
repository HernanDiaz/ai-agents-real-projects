"""Incident I05: appointment reminder."""
import unittest

from notices import appointment_reminder

MARTHA = {"name": "Martha Fisher", "email": "martha11@example.com",
          "notify_by": "email"}
LOLA = {"name": "Lola", "species": "dog"}
APPOINTMENT = {"id": "AP-0200", "date": "2026-10-21", "time": "10:30", "vet": "V1",
               "pet": "P-001", "reason": "annual checkup", "status": "scheduled"}


class I05Tests(unittest.TestCase):

    def test_reminder(self):
        text = appointment_reminder(MARTHA, LOLA, APPOINTMENT)
        self.assertTrue(text.startswith("Hi Martha,"))
        self.assertIn("Lola", text)
        self.assertIn("10/21/2026", text)
        self.assertIn("10:30", text)
        self.assertTrue(text.endswith("Northside Veterinary Clinic"))
