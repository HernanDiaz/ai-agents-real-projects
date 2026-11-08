import unittest

from notices import vaccine_reminder

MARTHA = {"name": "Martha Fisher", "phone": "(503) 555-0201",
          "email": "martha11@example.com", "notify_by": "email"}
LOLA = {"name": "Lola", "species": "dog"}


class NoticesTests(unittest.TestCase):

    def test_vaccine_reminder(self):
        vaccine = {"vaccine": "rabies", "next": "2026-11-02"}
        text = vaccine_reminder(MARTHA, LOLA, vaccine)
        self.assertTrue(text.startswith("Hi Martha,"))
        self.assertIn("Lola is due for the rabies vaccine on 11/02/2026", text)
        self.assertTrue(text.endswith("Northside Veterinary Clinic"))


if __name__ == "__main__":
    unittest.main()
