"""La base de datos de ejemplo: unos archivos JSON en la carpeta datos/."""
import json
from pathlib import Path

CARPETA = Path(__file__).parent / "datos"


def cargar(nombre):
    """Lee un archivo JSON de la carpeta de datos, por ejemplo «pedidos.json»."""
    with open(CARPETA / nombre, encoding="utf-8") as archivo:
        return json.load(archivo)


def guardar(nombre, contenido):
    """Escribe un archivo JSON en la carpeta de datos, en UTF-8 y con sangría."""
    with open(CARPETA / nombre, "w", encoding="utf-8") as archivo:
        json.dump(contenido, archivo, ensure_ascii=False, indent=1)


def catalogo():
    """La lista de productos del catálogo."""
    return cargar("catalogo.json")


def pedidos():
    """Los pedidos, en un diccionario por número de pedido (CN-…)."""
    return cargar("pedidos.json")


def existencias():
    """Las existencias del almacén, por referencia y talla."""
    return cargar("existencias.json")


def clientes():
    """Los clientes, en un diccionario por identificador (CL-…)."""
    return cargar("clientes.json")


def producto(ref):
    """El producto del catálogo con esa referencia, o None si no existe."""
    return next((p for p in catalogo() if p["ref"] == ref), None)
