"""Presupuestos del taller: revisiones, reparaciones y garantía (apartados 9 y 10)."""
from datetime import date

import config
from utilidades import formato_euros, redondear, sumar_meses


def _dias_entre(desde, hasta):
    """Días naturales entre dos fechas AAAA-MM-DD."""
    return (date.fromisoformat(hasta) - date.fromisoformat(desde)).days


def revision_gratuita(comprada_aqui, fecha_compra, hoy):
    """True si la bicicleta se compró en Ciclos Norte y no han pasado seis meses."""
    if not comprada_aqui:
        return False
    return _dias_entre(fecha_compra, hoy) // 30 < config.MESES_REVISION_GRATIS


def precio_revision(comprada_aqui, fecha_compra, hoy):
    """Lo que cuesta la revisión básica: nada si es la primera y gratuita."""
    if revision_gratuita(comprada_aqui, fecha_compra, hoy):
        return 0.0
    return float(config.REVISION_BASICA)


def en_garantia(fecha_compra, hoy):
    """True si no han pasado los dos años de garantía desde la compra."""
    return hoy <= sumar_meses(fecha_compra, config.MESES_GARANTIA)


def cubre_garantia(fecha_compra, hoy, pieza, causa):
    """True si la garantía cubre una pieza: dentro de plazo, por un defecto de
    fabricación y sin ser una pieza de desgaste."""
    if not en_garantia(fecha_compra, hoy) or causa != "defecto de fabricación":
        return False
    return pieza.lower() not in config.PIEZAS_DESGASTE


def bateria_en_garantia(fecha_compra, hoy, capacidad):
    """True si la batería de una bicicleta eléctrica se cambia por garantía: dentro
    de plazo y con menos del 70 % de su capacidad original."""
    if not en_garantia(fecha_compra, hoy):
        return False
    return capacidad < config.CAPACIDAD_MINIMA_BATERIA


def presupuesto_reparacion(piezas, horas, fecha_compra, hoy, causa):
    """Presupuesto de una reparación.

    «piezas» es una lista de (nombre, precio). Las piezas que cubre la garantía no
    se cobran, y la mano de obra tampoco si la garantía las cubre todas.
    """
    lineas = []
    for nombre, precio in piezas:
        cubierta = cubre_garantia(fecha_compra, hoy, nombre, causa)
        lineas.append({"concepto": nombre, "importe": 0.0 if cubierta else precio,
                       "garantia": cubierta})
    todo_cubierto = bool(lineas) and all(linea["garantia"] for linea in lineas)
    mano_obra = 0.0 if todo_cubierto else redondear(horas * config.TARIFA_HORA_TALLER)
    lineas.append({"concepto": f"Mano de obra ({horas} h)", "importe": mano_obra,
                   "garantia": todo_cubierto})
    total = redondear(sum(linea["importe"] for linea in lineas))
    return {"lineas": lineas, "total": total}


def texto_presupuesto(presupuesto):
    """El presupuesto como texto para entregar al cliente."""
    filas = []
    for linea in presupuesto["lineas"]:
        nota = "  (garantía)" if linea["garantia"] else ""
        importe = formato_euros(linea["importe"])
        filas.append(f"{linea['concepto']:<30}{importe:>12}{nota}")
    total = formato_euros(presupuesto["total"])
    filas.append(f"{'Total (IVA incluido)':<30}{total:>12}")
    return "\n".join(filas)
