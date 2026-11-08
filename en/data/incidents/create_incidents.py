"""Creates incidents I01 to I08 of Northside Veterinary Clinic, the repository on
which the workbench of chapter 12 is tried out.

Each incident has its request, its contract (contract.json), its data (meta.json),
its hidden tests and a reference solution, built from the original repository with
exact replacements. They are checked with check_incidents.py.

Usage: python create_incidents.py
"""
import json
import shutil
from pathlib import Path

FOLDER = Path(__file__).resolve().parent
REPO = FOLDER.parent / "northside_vet"


def substitute(path, changes):
    """The text of a file of the repository with the changes applied; each piece
    that is replaced must appear exactly once."""
    text = (REPO / path).read_text(encoding="utf-8")
    for before, after in changes:
        assert text.count(before) == 1, (path, before[:40])
        text = text.replace(before, after)
    return text


def create(incident_id, title, kind, request, signature, contract, tests, solution):
    """Writes the folder of an incident, from scratch."""
    folder = FOLDER / incident_id
    shutil.rmtree(folder, ignore_errors=True)
    (folder / "hidden_tests").mkdir(parents=True)
    (folder / "solution").mkdir()
    (folder / "request.md").write_text(
        f"# {incident_id} · {title}\n\n{request.strip()}\n\n— {signature}\n",
        encoding="utf-8")
    (folder / "contract.json").write_text(
        json.dumps({"task": incident_id, **contract}, ensure_ascii=False, indent=2)
        + "\n", encoding="utf-8")
    (folder / "meta.json").write_text(
        json.dumps({"id": incident_id, "title": title, "type": kind, "difficulty": 1,
                    "two_sessions": False, "repository": "northside_vet"},
                   ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (folder / "hidden_tests" / f"test_{incident_id.lower()}.py").write_text(
        tests.strip() + "\n", encoding="utf-8")
    for path, text in solution.items():
        destination = folder / "solution" / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(text, encoding="utf-8")


FORBIDDEN = ["data/"]

create("I01", "Appointments on weekends", "bug", """
The website offers slots to book appointments on Saturdays and Sundays, and the clinic
is closed on weekends. This week two owners showed up on a Saturday with the
appointment printed out.
""", "Amy (front desk)",
       {"goal": "No free slots on the days the clinic is closed.",
        "allowed_paths": ["appointments.py", "tests/test_appointments.py"],
        "forbidden_paths": FORBIDDEN + ["config.py"],
        "acceptance_criteria": ["free_slots returns no time on Saturday or Sunday.",
                                "From Monday to Friday it still returns the free times."]},
       '''
"""Incident I01: no slots on weekends."""
import unittest

from appointments import free_slots


class I01Tests(unittest.TestCase):

    def test_weekend(self):
        self.assertEqual(free_slots([], "V1", "2026-10-24"), [])
        self.assertEqual(free_slots([], "V1", "2026-10-25"), [])

    def test_weekday(self):
        self.assertEqual(len(free_slots([], "V1", "2026-10-23")), 10)
''',
       {"appointments.py": substitute("appointments.py", [
           ("from utils import to_minutes, to_time",
            "from utils import to_minutes, to_time, weekday"),
           ('''    """The free times of a vet on a day the clinic is open."""
    busy''', '''    """The free times of a vet on a day the clinic is open; none if the clinic is
    closed that day."""
    if weekday(date) not in config.OPEN_DAYS:
        return []
    busy''')])})

create("I02", "The vaccine due today doesn't show up", "bug", """
A dog had her rabies vaccine due today and it didn't show up among the overdue ones or
the upcoming ones, so nobody told her owner. The ones due on the same day must show up
as overdue.
""", "Dr. Anna Sutton",
       {"goal": "A vaccine due today must count as overdue.",
        "allowed_paths": ["vaccines.py", "tests/test_vaccines.py"],
        "forbidden_paths": FORBIDDEN,
        "acceptance_criteria": ["overdue includes the vaccines whose next date is today.",
                                "upcoming still does not include them."]},
       '''
"""Incident I02: the vaccine due today is overdue."""
import unittest

from vaccines import overdue, upcoming

LOLA = [{"vaccine": "rabies", "last": "2025-10-20", "next": "2026-10-20"},
        {"vaccine": "leptospirosis", "last": "2025-11-12", "next": "2026-11-12"}]


class I02Tests(unittest.TestCase):

    def test_due_today(self):
        self.assertEqual(overdue(LOLA, "2026-10-20"), ["rabies"])
        self.assertEqual(upcoming(LOLA, "2026-10-20"), ["leptospirosis"])
''',
       {"vaccines.py": substitute("vaccines.py", [
           ('if v["next"] < today]', 'if v["next"] <= today]')])})

create("I03", "The dose ignores allergies", "feature", """
When working out the dose of meloxicam for Coco, the program just gave it, and Coco is
allergic to meloxicam: it says so in his record. If the pet is allergic to the drug,
the dose cannot be worked out.
""", "Dr. Louis Porter",
       {"goal": "dose must not give a dose of a drug the pet is allergic to.",
        "allowed_paths": ["pharmacy.py", "tests/test_pharmacy.py"],
        "forbidden_paths": FORBIDDEN,
        "acceptance_criteria": ["dose raises ValueError if the drug is among the pet's allergies.",
                                "Without an allergy to the drug, the dose does not change."]},
       '''
"""Incident I03: the dose takes allergies into account."""
import unittest

from pharmacy import dose

PHARMACY = {"meloxicam": {"presentation": "oral suspension 1.5 mg/ml",
                          "dose_mg_kg": 0.1, "species": ["dog", "cat"], "stock": 14,
                          "price": 18.5}}
COCO = {"name": "Coco", "species": "dog", "weight_kg": 12.6, "allergies": ["meloxicam"]}
LOLA = {"name": "Lola", "species": "dog", "weight_kg": 13.0, "allergies": ["chicken"]}


class I03Tests(unittest.TestCase):

    def test_allergy(self):
        with self.assertRaises(ValueError):
            dose(PHARMACY, "meloxicam", COCO)

    def test_no_allergy(self):
        self.assertEqual(dose(PHARMACY, "meloxicam", LOLA)["mg"], 1.3)
''',
       {"pharmacy.py": substitute("pharmacy.py", [
           ('''    Raises ValueError if the drug is not for its species.
    """
    data = pharmacy[drug]''', '''    Raises ValueError if the drug is not for its species or if the pet is
    allergic to it.
    """
    data = pharmacy[drug]
    if drug in pet.get("allergies", []):
        raise ValueError(f"{pet['name']} is allergic to {drug}.")''')])})

create("I04", "New price for emergency visits", "rule", """
From November 1, an emergency visit costs $70 (it is $60 now). Please change it in the
program and in the price list.
""", "Maggie (management)",
       {"goal": "An emergency visit must cost $70 in the program and in the price list.",
        "allowed_paths": ["config.py", "docs/price_list.md", "tests/test_config.py"],
        "forbidden_paths": FORBIDDEN,
        "acceptance_criteria": ["config.PRICES['emergency visit'] is 70.",
                                "docs/price_list.md says $70.00 for the emergency visit.",
                                "The test that checked the old price is updated."]},
       '''
"""Incident I04: an emergency visit costs $70."""
import unittest
from pathlib import Path

import config


class I04Tests(unittest.TestCase):

    def test_price(self):
        self.assertEqual(config.PRICES["emergency visit"], 70.0)
        self.assertEqual(config.PRICES["consultation"], 35.0)

    def test_list(self):
        text = Path("docs/price_list.md").read_text(encoding="utf-8")
        self.assertIn("| Emergency visit | $70.00 |", text)
        self.assertNotIn("$60.00", text)
''',
       {"config.py": substitute("config.py", [('"emergency visit": 60.0,',
                                               '"emergency visit": 70.0,')]),
        "docs/price_list.md": substitute("docs/price_list.md", [
            ("| Emergency visit | $60.00 |", "| Emergency visit | $70.00 |")]),
        "tests/test_config.py": substitute("tests/test_config.py", [
            ('config.PRICES["emergency visit"], 60.0',
             'config.PRICES["emergency visit"], 70.0')])})

create("I05", "Appointment reminder", "feature", """
We want to send owners a reminder of their appointment the day before. Please add
`appointment_reminder(owner, pet, appointment)` to notices.py, with the greeting and
the signature of the vaccine reminder, giving the pet's name, the day (mm/dd/yyyy) and
the time of the appointment.
""", "Amy (front desk)",
       {"goal": "An appointment reminder for the owners.",
        "allowed_paths": ["notices.py", "tests/test_notices.py"],
        "forbidden_paths": FORBIDDEN + ["appointments.py"],
        "acceptance_criteria": ["appointment_reminder greets the owner and signs like the vaccine reminder.",
                                "It gives the pet's name, the day in mm/dd/yyyy format and the time."]},
       '''
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
''',
       {"notices.py": substitute("notices.py", [
           ('"""Messages for the owners: vaccine reminders."""',
            '"""Messages for the owners: vaccine and appointment reminders."""'), (
           '''def vaccine_reminder(owner, pet, vaccine):''',
           '''def appointment_reminder(owner, pet, appointment):
    """Reminder of an appointment, with the day and the time."""
    return (f"{greeting(owner)}\\n\\n"
            f"This is a reminder of {pet['name']}'s appointment on "
            f"{format_date(appointment['date'])} at {appointment['time']}."
            f"\\n\\n{SIGNATURE}")


def vaccine_reminder(owner, pet, vaccine):''')])})

create("I06", "Two appointments at the same time", "bug", """
Today Dr. Sutton had two dogs at 10:00: the front desk booked an appointment at a time
that was already taken and the program said nothing. If the time is taken, the
booking must not go through.
""", "Amy (front desk)",
       {"goal": "A time the vet already has taken cannot be booked.",
        "allowed_paths": ["appointments.py", "tests/test_appointments.py"],
        "forbidden_paths": FORBIDDEN,
        "acceptance_criteria": ["book raises ValueError if the vet already has that time taken.",
                                "A time with a canceled appointment can be booked."]},
       '''
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
''',
       {"appointments.py": substitute("appointments.py", [
           ('''    Raises ValueError if the time is not one of the opening slots.
    """
    if time not in opening_slots():
        raise ValueError(f"There are no appointments at {time}.")''',
            '''    Raises ValueError if the time is not one of the opening slots or if the vet
    already has it taken.
    """
    if time not in opening_slots():
        raise ValueError(f"There are no appointments at {time}.")
    if time in taken(appointments, vet, date):
        raise ValueError(f"{vet} already has an appointment at {time}.")''')])})

create("I07", "Dollar formatting in one place", "refactoring", """
pharmacy.py and invoices.py each have their own _dollars function, which does the same
as format_dollars in utils.py. Please remove the copies and use the one in utils. The
labels and the invoices must not change by a single character.
""", "Danny (IT)",
       {"goal": "pharmacy.py and invoices.py must use format_dollars from utils.py.",
        "allowed_paths": ["pharmacy.py", "invoices.py"],
        "forbidden_paths": FORBIDDEN + ["tests/", "utils.py"],
        "acceptance_criteria": ["Neither pharmacy.py nor invoices.py defines _dollars.",
                                "Both use format_dollars from utils.py.",
                                "The labels and the invoices come out the same as before."]},
       '''
"""Incident I07: dollar formatting in one place."""
import unittest
from pathlib import Path

from invoices import invoice_text
from pharmacy import label

PHARMACY = {"meloxicam": {"presentation": "oral suspension 1.5 mg/ml",
                          "dose_mg_kg": 0.1, "species": ["dog", "cat"], "stock": 14,
                          "price": 1018.5}}
LOLA = {"name": "Lola", "species": "dog", "weight_kg": 13.0, "allergies": []}
INVOICE = {"id": "INV-0001", "owner": "C-001", "date": "2026-10-16",
           "lines": [{"item": "dental cleaning", "amount": 1120.0}]}


class I07Tests(unittest.TestCase):

    def test_no_copies(self):
        for file in ("pharmacy.py", "invoices.py"):
            code = Path(file).read_text(encoding="utf-8")
            self.assertNotIn("def _dollars", code)
            self.assertIn("format_dollars", code)

    def test_same_texts(self):
        self.assertIn("Price: $1,018.50", label(PHARMACY, "meloxicam", LOLA))
        self.assertIn("$1,120.00", invoice_text(INVOICE))
''',
       {"pharmacy.py": substitute("pharmacy.py", [
           ("from utils import round_cents", "from utils import format_dollars, round_cents"),
           ('''def _dollars(amount):
    """An amount with a dollar sign and two decimals: 18.5 → "$18.50"."""
    return f"${amount:,.2f}"


''', ""),
           ('price = _dollars(pharmacy[drug]["price"])',
            'price = format_dollars(pharmacy[drug]["price"])')]),
        "invoices.py": substitute("invoices.py", [
           ("from utils import format_date, round_cents",
            "from utils import format_date, format_dollars, round_cents"),
           ('''def _dollars(amount):
    """An amount with a dollar sign and two decimals: 38 → "$38.00"."""
    return f"${amount:,.2f}"


''', ""),
           ("{_dollars(line['amount']):>12}", "{format_dollars(line['amount']):>12}"),
           ("{_dollars(parts['before_tax']):>12}",
            "{format_dollars(parts['before_tax']):>12}"),
           ("{_dollars(parts['tax']):>12}", "{format_dollars(parts['tax']):>12}"),
           ("{_dollars(amount):>12}", "{format_dollars(amount):>12}")])})

create("I08", "What an owner has paid", "feature", """
Some owners ask us for a summary of what they have paid over a period, for their taxes
or for their pet insurance. Please add `owner_total(invoices, owner, start, end)` to
invoices.py, adding up the owner's invoices between those two dates, both included,
rounded to cents.
""", "Maggie (management)",
       {"goal": "The sum of what an owner has paid between two dates.",
        "allowed_paths": ["invoices.py", "tests/test_invoices.py"],
        "forbidden_paths": FORBIDDEN,
        "acceptance_criteria": ["owner_total adds up the owner's invoices between the two dates, both included.",
                                "It does not count those of other owners or those outside the period.",
                                "It returns 0 if there are none, and rounds to cents."]},
       '''
"""Incident I08: what an owner has paid."""
import unittest

from invoices import owner_total

INVOICES = [{"id": "INV-1", "owner": "C-001", "date": "2026-10-01",
             "lines": [{"item": "consultation", "amount": 35.0}]},
            {"id": "INV-2", "owner": "C-001", "date": "2026-10-15",
             "lines": [{"item": "wound care", "amount": 22.1},
                       {"item": "deworming", "amount": 15.05}]},
            {"id": "INV-3", "owner": "C-002", "date": "2026-10-10",
             "lines": [{"item": "wound care", "amount": 22.0}]},
            {"id": "INV-4", "owner": "C-001", "date": "2026-11-02",
             "lines": [{"item": "consultation", "amount": 35.0}]}]


class I08Tests(unittest.TestCase):

    def test_period(self):
        self.assertEqual(owner_total(INVOICES, "C-001", "2026-10-01", "2026-10-15"),
                         72.15)
        self.assertEqual(owner_total(INVOICES, "C-001", "2026-10-02", "2026-10-31"),
                         37.15)

    def test_empty(self):
        self.assertEqual(owner_total(INVOICES, "C-003", "2026-01-01", "2026-12-31"), 0)
''',
       {"invoices.py": substitute("invoices.py", [(
           '''def _dollars(amount):''',
           '''def owner_total(invoices, owner, start, end):
    """What an owner has paid between two dates, both included."""
    return round_cents(sum(total(i["lines"]) for i in invoices
                           if i["owner"] == owner and start <= i["date"] <= end))


def _dollars(amount):''')])})
