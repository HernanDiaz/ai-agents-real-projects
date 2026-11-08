import unittest

from appointments import book, cancel, day_appointments, free_slots, opening_slots


def schedule():
    return [{"id": "AP-0001", "date": "2026-10-19", "time": "09:30", "vet": "V1",
             "pet": "P-001", "reason": "vaccination", "status": "scheduled"},
            {"id": "AP-0002", "date": "2026-10-19", "time": "10:00", "vet": "V1",
             "pet": "P-002", "reason": "ear infection", "status": "completed"}]


class AppointmentsTests(unittest.TestCase):

    def test_slots(self):
        slots = opening_slots()
        self.assertEqual(slots[0], "09:00")
        self.assertEqual(slots[-1], "13:30")
        self.assertEqual(len(slots), 10)

    def test_free_slots(self):
        free = free_slots(schedule(), "V1", "2026-10-19")
        self.assertNotIn("09:30", free)
        self.assertNotIn("10:00", free)
        self.assertIn("09:00", free)
        self.assertEqual(len(free_slots(schedule(), "V2", "2026-10-19")), 10)

    def test_book(self):
        appointments = schedule()
        new = book(appointments, "V2", "P-003", "2026-10-20", "11:00", "limping")
        self.assertEqual(new, "AP-0003")
        self.assertEqual(appointments[-1]["status"], "scheduled")
        with self.assertRaises(ValueError):
            book(appointments, "V2", "P-003", "2026-10-20", "15:00", "limping")

    def test_cancel(self):
        appointments = schedule()
        self.assertEqual(cancel(appointments, "AP-0001")["status"], "canceled")
        with self.assertRaises(ValueError):
            cancel(appointments, "AP-0002")
        of_day = day_appointments(appointments, "2026-10-19")
        self.assertEqual([a["id"] for a in of_day], ["AP-0002"])


if __name__ == "__main__":
    unittest.main()
