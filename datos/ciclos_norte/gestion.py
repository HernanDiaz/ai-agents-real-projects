"""Órdenes de consola para el día a día de la tienda.

    python gestion.py pedidos                     lista los pedidos
    python gestion.py estado "en preparación"     pedidos en un estado
    python gestion.py agotados AAAA-MM-DD         informe de agotados
    python gestion.py transferencias AAAA-MM-DD   transferencias caducadas

Las órdenes solo leen los datos: no guardan ningún cambio.
"""
import sys

import base_datos
import pedidos as gestion_pedidos
from existencias import informe_agotados


def listar_pedidos():
    """Una línea por pedido, ordenados por número."""
    todos = base_datos.pedidos()
    return "\n".join(gestion_pedidos.resumen(n, todos[n]) for n in sorted(todos))


def listar_estado(estado):
    """Los pedidos que están en un estado."""
    todos = base_datos.pedidos()
    numeros = gestion_pedidos.por_estado(todos, estado)
    filas = [gestion_pedidos.resumen(n, todos[n]) for n in numeros]
    return "\n".join(filas) or "Ninguno."


def agotados(hoy):
    """El informe de referencias agotadas."""
    return informe_agotados(base_datos.existencias(), hoy)


def transferencias(hoy):
    """Los pedidos que se cancelarían hoy por no haber recibido la transferencia."""
    numeros = gestion_pedidos.caducar_transferencias(base_datos.pedidos(), hoy)
    return "\n".join(numeros) or "Ninguno."


ORDENES = {
    "pedidos": listar_pedidos,
    "estado": listar_estado,
    "agotados": agotados,
    "transferencias": transferencias,
}


def main(argumentos):
    """Ejecuta la orden pedida y devuelve el código de salida del programa."""
    if not argumentos or argumentos[0] not in ORDENES:
        print(__doc__)
        return 1
    print(ORDENES[argumentos[0]](*argumentos[1:]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
