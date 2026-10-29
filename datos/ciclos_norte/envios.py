"""Zonas, gastos y plazos de envío (apartado 5 de las condiciones generales)."""
import config
from utilidades import sumar_dias_laborables


def zona(codigo_postal):
    """Zona de envío de un código postal: «peninsula», «baleares» o «canarias».

    Los códigos de Baleares empiezan por 07; los de Canarias, por 35 o 38.
    """
    codigo = str(codigo_postal).strip()
    for nombre, prefijos in config.PREFIJOS_CP.items():
        if codigo.startswith(prefijos):
            return nombre
    return "peninsula"


def gastos_envio(subtotal, codigo_postal):
    """Gastos de envío de un pedido según el importe de sus productos y su destino."""
    if subtotal > config.UMBRAL_ENVIO_GRATIS:
        return 0.0
    return config.TARIFAS_ENVIO[zona(codigo_postal)]


def fecha_entrega_estimada(fecha_salida, codigo_postal):
    """Primera y última fecha probables de entrega, en días laborables contados
    desde que el pedido sale del almacén."""
    minimo, maximo = config.DIAS_ENTREGA[zona(codigo_postal)]
    return (sumar_dias_laborables(fecha_salida, minimo),
            sumar_dias_laborables(fecha_salida, maximo))
