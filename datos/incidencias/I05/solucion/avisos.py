"""Mensajes para los dueños: recordatorios de vacunas y de citas."""
from utilidades import formato_fecha

FIRMA = "Un saludo,\nClínica Veterinaria Naranco"


def saludo(dueno):
    """El saludo con el nombre de pila del dueño."""
    return f"Hola, {dueno['nombre'].split()[0]}:"


def recordatorio_cita(dueno, mascota, cita):
    """Recordatorio de una cita, con el día y la hora."""
    return (f"{saludo(dueno)}\n\n"
            f"Te recordamos la cita de {mascota['nombre']} el "
            f"{formato_fecha(cita['fecha'])} a las {cita['hora']}."
            f"\n\n{FIRMA}")


def recordatorio_vacuna(dueno, mascota, vacuna):
    """Recordatorio de que a una mascota le toca una vacuna. «vacuna» es como las de
    datos/vacunas.json, con su fecha «proxima»."""
    return (f"{saludo(dueno)}\n\n"
            f"A {mascota['nombre']} le toca la vacuna de {vacuna['vacuna']} el "
            f"{formato_fecha(vacuna['proxima'])}. Puedes pedir cita llamando a la clínica."
            f"\n\n{FIRMA}")
