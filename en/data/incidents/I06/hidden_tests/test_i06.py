"""Incident I06: a taken time is not booked."""
import unittest

from appointments import book


def schedule(status="scheduled"):
    return [{"id": "AP-0001", "date": "2026-10-19", "time": "10:00", "vet": "V1",
             "pet": "P-001", "reason": "vaccination", "status": status}]


class I06Tests(unittest.TestCase):

    def test_taken(self):
        appointments = schedule()
        with self.assertRaises(ValueError):
            book(appointments, "V1", "P-002", "2026-10-19", "10:00", "ear infection")
        self.assertEqual(len(appointments), 1)

    def test_canceled_and_other_vet(self):
        self.assertEqual(book(schedule("canceled"), "V1", "P-002", "2026-10-19",
                              "10:00", "ear infection"), "AP-0002")
        self.assertEqual(book(schedule(), "V2", "P-002", "2026-10-19", "10:00",
                              "ear infection"), "AP-0002")
