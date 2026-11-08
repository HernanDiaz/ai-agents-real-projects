"""Reading and writing the clinic's data (folder data/)."""
import json
from pathlib import Path

DATA = Path(__file__).parent / "data"


def load(name):
    """Reads a JSON file from the data folder, for example "appointments.json"."""
    with open(DATA / name, encoding="utf-8") as file:
        return json.load(file)


def save(name, content):
    """Writes a JSON file to the data folder."""
    with open(DATA / name, "w", encoding="utf-8") as file:
        json.dump(content, file, ensure_ascii=False, indent=1)


def appointments():
    """The list of appointments."""
    return load("appointments.json")


def pets():
    """The pets, by id (P-…)."""
    return load("pets.json")


def owners():
    """The owners, by id (C-…)."""
    return load("owners.json")


def vaccines():
    """The vaccines of each pet, by pet id."""
    return load("vaccines.json")


def pharmacy():
    """The drugs of the clinic's pharmacy."""
    return load("pharmacy.json")


def invoices():
    """The list of invoices."""
    return load("invoices.json")
