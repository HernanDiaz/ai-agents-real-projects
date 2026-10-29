"""Presupuestos del taller que necesitan la aprobación del cliente antes de empezar."""
from presupuestos import presupuesto_reparacion

UMBRAL_APROBACION = 150   # euros, IVA incluido: por encima se llama al cliente


def presupuesto_con_aprobacion(piezas, horas, fecha_compra, hoy, causa):
    """El presupuesto de una reparación con un campo más, «aprobacion»: si hay que
    llamar al cliente antes de empezar. Si alguna pieza no tiene precio todavía, no hay
    total y hay que llamar: el taller no inventa precios."""
    if any(precio is None for _, precio in piezas):
        return {"total": None, "aprobacion": True}
    presupuesto = presupuesto_reparacion(piezas, horas, fecha_compra, hoy, causa)
    return dict(presupuesto, aprobacion=presupuesto["total"] > UMBRAL_APROBACION)
