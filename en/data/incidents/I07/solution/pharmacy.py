"""The clinic's pharmacy: doses, stock and labels.

The drugs are a dictionary like the one of data/pharmacy.json:
{"meloxicam": {"presentation": "…", "dose_mg_kg": 0.1, "species": ["dog", "cat"],
 "stock": 14, "price": 18.5}, …}.
"""
from utils import format_dollars, round_cents


def dose(pharmacy, drug, pet):
    """The dose of a drug for a pet, in mg, according to its weight.

    Raises ValueError if the drug is not for its species.
    """
    data = pharmacy[drug]
    if pet["species"] not in data["species"]:
        raise ValueError(f"{drug.capitalize()} is not for a {pet['species']}.")
    return {"drug": drug, "mg": round_cents(data["dose_mg_kg"] * pet["weight_kg"]),
            "presentation": data["presentation"]}


def available(pharmacy, drug, units=1):
    """True if there are at least that many units of the drug left."""
    return pharmacy[drug]["stock"] >= units


def label(pharmacy, drug, pet):
    """The label stuck on the package: drug, pet, dose and price."""
    d = dose(pharmacy, drug, pet)
    price = format_dollars(pharmacy[drug]["price"])
    return (f"{drug.capitalize()} ({d['presentation']})\n"
            f"For: {pet['name']}, {pet['weight_kg']} kg\n"
            f"Dose: {d['mg']} mg\nPrice: {price}")
