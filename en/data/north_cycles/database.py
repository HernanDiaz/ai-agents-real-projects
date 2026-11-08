"""The sample database: a few JSON files in the data/ folder."""
import json
from pathlib import Path

FOLDER = Path(__file__).parent / "data"


def load(name):
    """Reads a JSON file from the data folder, for example "orders.json"."""
    with open(FOLDER / name, encoding="utf-8") as file:
        return json.load(file)


def save(name, content):
    """Writes a JSON file to the data folder, in UTF-8 and indented."""
    with open(FOLDER / name, "w", encoding="utf-8") as file:
        json.dump(content, file, ensure_ascii=False, indent=1)


def catalog():
    """The list of products in the catalog."""
    return load("catalog.json")


def orders():
    """The orders, in a dictionary by order number (NC-…)."""
    return load("orders.json")


def stock():
    """The warehouse stock, by product reference and size."""
    return load("stock.json")


def customers():
    """The customers, in a dictionary by id (CL-…)."""
    return load("customers.json")


def product(ref):
    """The catalog product with that reference, or None if there is none."""
    return next((p for p in catalog() if p["ref"] == ref), None)
