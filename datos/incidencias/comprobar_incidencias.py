"""Comprueba las incidencias de la Clínica Veterinaria Naranco, como comprobar_banco.py
con las tareas de Ciclos Norte: en una copia limpia del repositorio, las pruebas ocultas
deben fallar antes de tocar nada; con la solución de referencia, aplicada con la
herramienta editar, deben pasar las ocultas y las visibles; y la solución solo puede
tocar rutas permitidas.

Uso: python comprobar_incidencias.py [I01 I02 …]
"""
import json
import sys
from pathlib import Path

CARPETA = Path(__file__).resolve().parent
REPO = CARPETA.parent / "clinica_naranco"
sys.path.insert(0, str(CARPETA.parent.parent / "comun_libro"))

from herramientas_repo import (Espacio, Herramientas, aplicar_solucion,  # noqa: E402
                               evaluar_intento, pasar_ocultas)


def leer(identificador):
    """Una incidencia, con el mismo formato que las tareas de Ciclos Norte."""
    carpeta = CARPETA / identificador
    return {"id": identificador, "carpeta": carpeta,
            "peticion": (carpeta / "tarea.md").read_text(encoding="utf-8"),
            "alcance": json.loads((carpeta / "alcance.json").read_text(encoding="utf-8")),
            "meta": json.loads((carpeta / "meta.json").read_text(encoding="utf-8"))}


def comprobar(incidencia):
    """Los problemas de una incidencia, o una lista vacía."""
    problemas = []
    with Espacio(REPO) as espacio:
        if pasar_ocultas(espacio.carpeta, incidencia)["pasan"]:
            problemas.append("las pruebas ocultas ya pasan sin tocar nada")
        resultados = aplicar_solucion(Herramientas(espacio), incidencia["carpeta"] / "solucion")
        errores = [r for r in resultados if "error" in r]
        if errores:
            problemas.append(f"la solución no se aplica: {errores[0]}")
        evaluacion = evaluar_intento(espacio, incidencia)
        if not evaluacion["ocultas"]:
            problemas.append("con la solución no pasan las ocultas: "
                             + evaluacion["salida_ocultas"][-300:])
        if not evaluacion["visibles"]:
            problemas.append("con la solución fallan las visibles")
        if evaluacion["fuera_de_alcance"] or evaluacion["prohibidos"]:
            problemas.append(f"toca rutas no permitidas: {evaluacion['cambiados']}")
    return problemas


if __name__ == "__main__":
    ids = sys.argv[1:] or sorted(p.name for p in CARPETA.glob("I[0-9][0-9]"))
    bien = 0
    for identificador in ids:
        problemas = comprobar(leer(identificador))
        bien += not problemas
        print(f"{identificador}  {'bien' if not problemas else '; '.join(problemas)}")
    print(json.dumps({"incidencias": len(ids), "correctas": bien}))
