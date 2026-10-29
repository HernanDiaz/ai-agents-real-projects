"""Comprueba el banco de tareas del repositorio de Ciclos Norte.

Para cada tarea, sobre una copia limpia del repositorio:
1. Las pruebas ocultas deben fallar antes de tocar nada (si no, la tarea no mide nada).
2. Se aplica la solución de referencia con la herramienta editar, como lo haría el
   agente.
3. Deben pasar las pruebas ocultas y las visibles.
4. La solución solo puede tocar rutas permitidas por su alcance.

Uso: python comprobar_banco.py [T01 T02 …]
"""
import json
import sys
from pathlib import Path

CARPETA = Path(__file__).resolve().parent
sys.path.insert(0, str(CARPETA.parent.parent / "comun_libro"))

from herramientas_repo import (Espacio, Herramientas, aplicar_solucion,  # noqa: E402
                               evaluar_intento, leer_tarea, pasar_ocultas)

TIPOS = {"fallo", "funcion", "regla", "refactorizacion"}


def comprobar_ficha(tarea):
    """Los problemas de forma de una tarea: archivos que faltan o datos no válidos."""
    problemas = []
    meta, alcance = tarea["meta"], tarea["alcance"]
    if meta["tipo"] not in TIPOS:
        problemas.append(f"tipo desconocido: {meta['tipo']}")
    if meta["dificultad"] not in (1, 2, 3):
        problemas.append(f"dificultad no válida: {meta['dificultad']}")
    if not isinstance(meta["dos_sesiones"], bool):
        problemas.append("dos_sesiones debe ser true o false")
    for clave in ("objetivo", "rutas_permitidas", "rutas_prohibidas",
                  "criterios_aceptacion"):
        if not alcance.get(clave):
            problemas.append(f"falta «{clave}» en alcance.json")
    if not list((tarea["carpeta"] / "pruebas_ocultas").glob("test_*.py")):
        problemas.append("no hay pruebas ocultas")
    if not (tarea["carpeta"] / "solucion").is_dir():
        problemas.append("no hay solución de referencia")
    return problemas


def comprobar_tarea(identificador):
    """Comprueba una tarea y devuelve (fila para la tabla, lista de problemas)."""
    tarea = leer_tarea(identificador)
    problemas = comprobar_ficha(tarea)
    with Espacio() as espacio:
        if pasar_ocultas(espacio.carpeta, tarea)["pasan"]:
            problemas.append("las pruebas ocultas ya pasan en el repositorio original")
        ediciones = aplicar_solucion(Herramientas(espacio),
                                     tarea["carpeta"] / "solucion")
        problemas += [f"edición fallida: {e['error']}"
                      for e in ediciones if "error" in e]
        evaluacion = evaluar_intento(espacio, tarea)
    if not evaluacion["ocultas"]:
        problemas.append("con la solución, las pruebas ocultas fallan:\n"
                         + evaluacion["salida_ocultas"])
    if not evaluacion["visibles"]:
        problemas.append("con la solución, las pruebas visibles fallan")
    for clave in ("fuera_de_alcance", "prohibidos"):
        if evaluacion[clave]:
            problemas.append(f"{clave}: {', '.join(evaluacion[clave])}")
    meta = tarea["meta"]
    dos_sesiones = "sí" if meta["dos_sesiones"] else "no"
    fila = (f"{identificador}  {meta['tipo']:<16}{meta['dificultad']}  "
            f"{dos_sesiones:<3} {len(ediciones):>3} ediciones  "
            f"{', '.join(evaluacion['cambiados'])}")
    return fila, problemas


def main(identificadores):
    """Comprueba las tareas pedidas (todas si no se indica ninguna)."""
    if not identificadores:
        identificadores = sorted(p.name for p in CARPETA.glob("T[0-9][0-9]")
                                 if p.is_dir())
    print("Tarea tipo            dif 2s  cambios")
    fallidas = {}
    for identificador in identificadores:
        fila, problemas = comprobar_tarea(identificador)
        print(("   " if not problemas else "MAL ") + fila)
        if problemas:
            fallidas[identificador] = problemas
    resumen = {"tareas": len(identificadores), "correctas": len(identificadores)
               - len(fallidas)}
    print(json.dumps(resumen, ensure_ascii=False))
    for identificador, problemas in fallidas.items():
        print(f"\n{identificador}:")
        for problema in problemas:
            print("  -", problema)
    return 0 if not fallidas else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
