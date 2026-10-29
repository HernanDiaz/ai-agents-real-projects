"""Vacunas de las mascotas: cuáles han vencido y cuáles vencen pronto.

Las vacunas de una mascota son una lista como las de datos/vacunas.json:
[{"vacuna": "rabia", "ultima": "2026-08-22", "proxima": "2027-08-22"}, …].
"""
import config
from utilidades import sumar_dias


def vencidas(vacunas_mascota, hoy):
    """Las vacunas cuya próxima dosis ya tocaba: la fecha «proxima» es hoy o
    anterior."""
    return [v["vacuna"] for v in vacunas_mascota if v["proxima"] < hoy]


def proximas(vacunas_mascota, hoy, dias=config.DIAS_AVISO_VACUNA):
    """Las vacunas que vencen en los próximos «dias» días, sin contar las vencidas."""
    limite = sumar_dias(hoy, dias)
    return [v["vacuna"] for v in vacunas_mascota if hoy < v["proxima"] <= limite]


def avisos_pendientes(vacunas, hoy):
    """Las mascotas que tienen alguna vacuna vencida o que vence pronto, con sus
    vacunas, por identificador de mascota."""
    avisos = {}
    for mascota, suyas in vacunas.items():
        lista = vencidas(suyas, hoy) + proximas(suyas, hoy)
        if lista:
            avisos[mascota] = lista
    return avisos
