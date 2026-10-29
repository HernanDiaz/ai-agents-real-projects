"""Mensajes para los dueños: recordatorios de vacunas."""
from utilidades import formato_fecha

FIRMA = "Un saludo,\nClínica Veterinaria Naranco"


def saludo(dueno):
    """El saludo con el nombre de pila del dueño."""
    return f"Hola, {dueno['nombre'].split()[0]}:"


def recordatorio_vacuna(dueno, mascota, vacuna):
    """Recordatorio de que a una mascota le toca una vacuna. «vacuna» es como las de
    datos/vacunas.json, con su fecha «proxima»."""
    return (f"{saludo(dueno)}\n\n"
            f"A {mascota['nombre']} le toca la vacuna de {vacuna['vacuna']} el "
            f"{formato_fecha(vacuna['proxima'])}. Puedes pedir cita llamando a la clínica."
            f"\n\n{FIRMA}")
