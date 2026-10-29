"""Citas de la consulta: huecos libres, reservas y cancelaciones.

Las citas son una lista de diccionarios como los de datos/citas.json:
{"id": "CT-0001", "fecha": "2026-10-19", "hora": "11:00", "veterinario": "V1",
 "mascota": "M-008", "motivo": "revisión anual", "estado": "pendiente"}.
"""
import config
from utilidades import dia_de_la_semana, hora, minutos


def horas_de_consulta():
    """Las horas a las que puede empezar una cita: de la apertura a media hora antes
    del cierre, cada media hora."""
    return [hora(m) for m in range(minutos(config.APERTURA), minutos(config.CIERRE),
                                   config.DURACION_CITA)]


def ocupadas(citas, veterinario, fecha):
    """Las horas de ese día en las que el veterinario ya tiene una cita que no está
    cancelada."""
    return {c["hora"] for c in citas
            if c["veterinario"] == veterinario and c["fecha"] == fecha
            and c["estado"] != "cancelada"}


def huecos_libres(citas, veterinario, fecha):
    """Las horas libres de un veterinario en un día de consulta; ninguna si ese día
    no hay consulta."""
    if dia_de_la_semana(fecha) not in config.DIAS_DE_CONSULTA:
        return []
    tomadas = ocupadas(citas, veterinario, fecha)
    return [h for h in horas_de_consulta() if h not in tomadas]


def siguiente_id(citas):
    """El identificador de la próxima cita: CT- y un número correlativo."""
    mayor = max((int(c["id"].removeprefix("CT-")) for c in citas), default=0)
    return f"CT-{mayor + 1:04d}"


def reservar(citas, veterinario, mascota, fecha, hora_cita, motivo):
    """Añade una cita pendiente y devuelve su identificador.

    Lanza ValueError si la hora no es una de las horas de consulta.
    """
    if hora_cita not in horas_de_consulta():
        raise ValueError(f"A las {hora_cita} no hay consulta.")
    cita = {"id": siguiente_id(citas), "fecha": fecha, "hora": hora_cita,
            "veterinario": veterinario, "mascota": mascota, "motivo": motivo,
            "estado": "pendiente"}
    citas.append(cita)
    return cita["id"]


def cancelar(citas, id_cita):
    """Cancela una cita pendiente. Lanza ValueError si ya se realizó o no existe."""
    for cita in citas:
        if cita["id"] == id_cita:
            if cita["estado"] != "pendiente":
                raise ValueError(f"No se puede cancelar una cita «{cita['estado']}».")
            cita["estado"] = "cancelada"
            return cita
    raise ValueError(f"No existe la cita {id_cita}.")


def citas_del_dia(citas, fecha, veterinario=None):
    """Las citas de un día que no están canceladas, por hora; de todos los
    veterinarios o de uno."""
    del_dia = [c for c in citas if c["fecha"] == fecha and c["estado"] != "cancelada"
               and (veterinario is None or c["veterinario"] == veterinario)]
    return sorted(del_dia, key=lambda c: c["hora"])
