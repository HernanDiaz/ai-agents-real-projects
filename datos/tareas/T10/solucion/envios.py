"""Zonas, gastos y plazos de envío (apartado 5 de las condiciones generales)."""
import re

import config
from utilidades import sumar_dias_laborables

PATRON_PORTUGAL = re.compile(r"^\d{4}-\d{3}$")  # 4000-123


def zona(codigo_postal):
    """Zona de envío de un código postal: «peninsula», «baleares», «canarias»,
    «portugal» o «andorra».

    Los códigos de Baleares empiezan por 07; los de Canarias, por 35 o 38. Los de
    Portugal tienen la forma 4000-123, y los de Andorra, AD500.
    """
    codigo = str(codigo_postal).strip().upper()
    if PATRON_PORTUGAL.match(codigo):
        return "portugal"
    if codigo.startswith("AD"):
        return "andorra"
    for nombre, prefijos in config.PREFIJOS_CP.items():
        if codigo.startswith(prefijos):
            return nombre
    return "peninsula"


def gastos_envio(subtotal, codigo_postal):
    """Gastos de envío de un pedido según el importe de sus productos y su destino."""
    zona_envio = zona(codigo_postal)
    if zona_envio == "peninsula" and subtotal > config.UMBRAL_ENVIO_GRATIS:
        return 0.0
    return config.TARIFAS_ENVIO[zona_envio]


def fecha_entrega_estimada(fecha_salida, codigo_postal):
    """Primera y última fecha probables de entrega, en días laborables contados
    desde que el pedido sale del almacén."""
    minimo, maximo = config.DIAS_ENTREGA[zona(codigo_postal)]
    return (sumar_dias_laborables(fecha_salida, minimo),
            sumar_dias_laborables(fecha_salida, maximo))
