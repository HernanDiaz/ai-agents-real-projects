"""Existencias del almacén, por referencia y talla.

Las existencias son un diccionario como el de datos/existencias.json:
{"UR-5120": {"nombre": "Urbana 3", "unidades": {"S": 2, "M": 4}, "reposicion": …}}.
"""
from utilidades import formato_fecha


class SinExistencias(Exception):
    """No hay unidades suficientes para servir un pedido."""


def unidades(existencias, ref, talla):
    """Unidades disponibles de una referencia en una talla (0 si no hay registro)."""
    producto = existencias.get(ref)
    if producto is None:
        return 0
    return producto["unidades"].get(talla, 0)


def total_unidades(existencias, ref):
    """Unidades de una referencia sumando todas sus tallas (0 si no está)."""
    producto = existencias.get(ref)
    if producto is None:
        return 0
    return sum(producto["unidades"].values())


def hay_existencias(existencias, ref, talla, cantidad=1):
    """True si hay al menos «cantidad» unidades de esa referencia y talla."""
    return unidades(existencias, ref, talla) >= cantidad


def reservar(existencias, lineas):
    """Descuenta del almacén las unidades de un pedido.

    Si falta alguna línea, no descuenta nada y lanza SinExistencias. Varias líneas
    con la misma referencia y talla se suman antes de comprobar.
    """
    necesarias = {}
    for linea in lineas:
        clave = (linea["ref"], linea["talla"])
        necesarias[clave] = necesarias.get(clave, 0) + linea["cantidad"]
    for (ref, talla), cantidad in necesarias.items():
        if not hay_existencias(existencias, ref, talla, cantidad):
            raise SinExistencias(
                f"No hay {cantidad} unidades de {ref} en talla {talla}.")
    for (ref, talla), cantidad in necesarias.items():
        existencias[ref]["unidades"][talla] -= cantidad


def reponer(existencias, ref, talla, cantidad, nombre=None):
    """Suma unidades al almacén, al llegar un envío del proveedor o una devolución.
    Si la referencia o la talla son nuevas, las crea."""
    producto = existencias.setdefault(ref, {"nombre": nombre or ref, "unidades": {}})
    producto["unidades"][talla] = producto["unidades"].get(talla, 0) + cantidad


def tallas_agotadas(existencias, ref):
    """Las tallas de una referencia que no tienen ninguna unidad."""
    return [talla for talla, n in existencias[ref]["unidades"].items() if n == 0]


def agotados(existencias):
    """Las referencias que no tienen ninguna unidad en ninguna talla, ordenadas."""
    return sorted(ref for ref, producto in existencias.items()
                  if any(n == 0 for n in producto["unidades"].values()))


def informe_agotados(existencias, hoy):
    """Texto con las referencias agotadas y su fecha de reposición, si la hay."""
    filas = []
    for ref in agotados(existencias):
        producto = existencias[ref]
        reposicion = producto.get("reposicion")
        if reposicion and reposicion >= hoy:
            cuando = f"reposición el {formato_fecha(reposicion)}"
        else:
            cuando = "sin fecha de reposición"
        filas.append(f"{ref} {producto['nombre']}: agotado, {cuando}")
    return "\n".join(filas) or "No hay referencias agotadas."
