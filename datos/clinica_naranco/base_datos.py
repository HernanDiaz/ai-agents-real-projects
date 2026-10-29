"""Lectura y escritura de los datos de la clínica (carpeta datos/)."""
import json
from pathlib import Path

DATOS = Path(__file__).parent / "datos"


def cargar(nombre):
    """Lee un archivo JSON de la carpeta de datos, por ejemplo «citas.json»."""
    with open(DATOS / nombre, encoding="utf-8") as archivo:
        return json.load(archivo)


def guardar(nombre, contenido):
    """Escribe un archivo JSON en la carpeta de datos."""
    with open(DATOS / nombre, "w", encoding="utf-8") as archivo:
        json.dump(contenido, archivo, ensure_ascii=False, indent=1)


def citas():
    """La lista de citas."""
    return cargar("citas.json")


def mascotas():
    """Las mascotas, por identificador (M-…)."""
    return cargar("mascotas.json")


def duenos():
    """Los dueños, por identificador (D-…)."""
    return cargar("duenos.json")


def vacunas():
    """Las vacunas de cada mascota, por identificador de mascota."""
    return cargar("vacunas.json")


def farmacia():
    """Los medicamentos de la farmacia de la clínica."""
    return cargar("farmacia.json")


def facturas():
    """La lista de facturas."""
    return cargar("facturas.json")
