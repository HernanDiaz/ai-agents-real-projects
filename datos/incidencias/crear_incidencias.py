"""Crea las incidencias I01 a I08 de la Clínica Veterinaria Naranco, el repositorio en el
que se prueba el banco de trabajo del capítulo 12.

Cada incidencia tiene su petición, su contrato (alcance.json), sus datos (meta.json),
sus pruebas ocultas y una solución de referencia, construida a partir del repositorio
original con sustituciones exactas. Se comprueban con comprobar_incidencias.py.

Uso: python crear_incidencias.py
"""
import json
import shutil
from pathlib import Path

CARPETA = Path(__file__).resolve().parent
REPO = CARPETA.parent / "clinica_naranco"


def sustituir(ruta, cambios):
    """El texto de un archivo del repositorio con los cambios aplicados; cada trozo
    que se sustituye tiene que aparecer exactamente una vez."""
    texto = (REPO / ruta).read_text(encoding="utf-8")
    for antes, despues in cambios:
        assert texto.count(antes) == 1, (ruta, antes[:40])
        texto = texto.replace(antes, despues)
    return texto


def crear(identificador, titulo, tipo, peticion, firma, alcance, pruebas, solucion):
    """Escribe la carpeta de una incidencia, desde cero."""
    carpeta = CARPETA / identificador
    shutil.rmtree(carpeta, ignore_errors=True)
    (carpeta / "pruebas_ocultas").mkdir(parents=True)
    (carpeta / "solucion").mkdir()
    (carpeta / "tarea.md").write_text(
        f"# {identificador} · {titulo}\n\n{peticion.strip()}\n\n— {firma}\n",
        encoding="utf-8")
    (carpeta / "alcance.json").write_text(
        json.dumps({"tarea": identificador, **alcance}, ensure_ascii=False, indent=2)
        + "\n", encoding="utf-8")
    (carpeta / "meta.json").write_text(
        json.dumps({"id": identificador, "titulo": titulo, "tipo": tipo, "dificultad": 1,
                    "dos_sesiones": False, "repositorio": "clinica_naranco"},
                   ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (carpeta / "pruebas_ocultas" / f"test_{identificador.lower()}.py").write_text(
        pruebas.strip() + "\n", encoding="utf-8")
    for ruta, texto in solucion.items():
        destino = carpeta / "solucion" / ruta
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(texto, encoding="utf-8")


PROHIBIDAS = ["datos/"]

crear("I01", "Citas en fin de semana", "fallo", """
La web ofrece huecos para pedir cita los sábados y los domingos, y los fines de semana la
consulta está cerrada. Esta semana han venido dos dueños un sábado con la cita impresa.
""", "Ana (recepción)",
      {"objetivo": "Que no haya huecos libres los días sin consulta.",
       "rutas_permitidas": ["citas.py", "tests/test_citas.py"],
       "rutas_prohibidas": PROHIBIDAS + ["config.py"],
       "criterios_aceptacion": ["huecos_libres no devuelve ninguna hora en sábado ni en domingo.",
                                "De lunes a viernes sigue devolviendo las horas libres."]},
      '''
"""Incidencia I01: sin huecos los fines de semana."""
import unittest

from citas import huecos_libres


class PruebasI01(unittest.TestCase):

    def test_fin_de_semana(self):
        self.assertEqual(huecos_libres([], "V1", "2026-10-24"), [])
        self.assertEqual(huecos_libres([], "V1", "2026-10-25"), [])

    def test_entre_semana(self):
        self.assertEqual(len(huecos_libres([], "V1", "2026-10-23")), 10)
''',
      {"citas.py": sustituir("citas.py", [
          ("from utilidades import hora, minutos",
           "from utilidades import dia_de_la_semana, hora, minutos"),
          ('''    """Las horas libres de un veterinario en un día de consulta."""
    tomadas''', '''    """Las horas libres de un veterinario en un día de consulta; ninguna si ese día
    no hay consulta."""
    if dia_de_la_semana(fecha) not in config.DIAS_DE_CONSULTA:
        return []
    tomadas''')])})

crear("I02", "La vacuna que vence hoy no sale", "fallo", """
Una perra tenía la vacuna de la rabia para hoy y no salía ni en las vencidas ni en las
próximas, así que nadie avisó a su dueña. Las que vencen el mismo día tienen que salir
como vencidas.
""", "Dra. Ana Suárez",
      {"objetivo": "Que una vacuna que vence hoy cuente como vencida.",
       "rutas_permitidas": ["vacunas.py", "tests/test_vacunas.py"],
       "rutas_prohibidas": PROHIBIDAS,
       "criterios_aceptacion": ["vencidas incluye las vacunas con fecha próxima igual a hoy.",
                                "proximas sigue sin incluirlas."]},
      '''
"""Incidencia I02: la vacuna que vence hoy está vencida."""
import unittest

from vacunas import proximas, vencidas

LOLA = [{"vacuna": "rabia", "ultima": "2025-10-20", "proxima": "2026-10-20"},
        {"vacuna": "leishmaniosis", "ultima": "2025-11-12", "proxima": "2026-11-12"}]


class PruebasI02(unittest.TestCase):

    def test_vence_hoy(self):
        self.assertEqual(vencidas(LOLA, "2026-10-20"), ["rabia"])
        self.assertEqual(proximas(LOLA, "2026-10-20"), ["leishmaniosis"])
''',
      {"vacunas.py": sustituir("vacunas.py", [
          ('if v["proxima"] < hoy]', 'if v["proxima"] <= hoy]')])})

crear("I03", "La dosis no avisa de las alergias", "funcion", """
Al calcular la dosis de meloxicam para Coco, el programa la dio sin más, y Coco es alérgico
al meloxicam: lo pone en su ficha. Si la mascota es alérgica al medicamento, la dosis no se
puede calcular.
""", "Dr. Luis Prieto",
      {"objetivo": "Que dosis no dé una dosis de un medicamento al que la mascota es alérgica.",
       "rutas_permitidas": ["farmacia.py", "tests/test_farmacia.py"],
       "rutas_prohibidas": PROHIBIDAS,
       "criterios_aceptacion": ["dosis lanza ValueError si el medicamento está en las alergias de la mascota.",
                                "Sin alergia al medicamento, la dosis no cambia."]},
      '''
"""Incidencia I03: la dosis tiene en cuenta las alergias."""
import unittest

from farmacia import dosis

FARMACIA = {"meloxicam": {"presentacion": "suspensión oral 1,5 mg/ml", "dosis_mg_kg": 0.1,
                          "especies": ["perro", "gato"], "existencias": 14, "precio": 18.5}}
COCO = {"nombre": "Coco", "especie": "perro", "peso_kg": 12.6, "alergias": ["meloxicam"]}
LOLA = {"nombre": "Lola", "especie": "perro", "peso_kg": 13.0, "alergias": ["pollo"]}


class PruebasI03(unittest.TestCase):

    def test_alergia(self):
        with self.assertRaises(ValueError):
            dosis(FARMACIA, "meloxicam", COCO)

    def test_sin_alergia(self):
        self.assertEqual(dosis(FARMACIA, "meloxicam", LOLA)["mg"], 1.3)
''',
      {"farmacia.py": sustituir("farmacia.py", [
          ('''    Lanza ValueError si el medicamento no es para su especie.
    """
    datos = farmacia[medicamento]''', '''    Lanza ValueError si el medicamento no es para su especie o si la mascota es
    alérgica a él.
    """
    datos = farmacia[medicamento]
    if medicamento in mascota.get("alergias", []):
        raise ValueError(f"{mascota['nombre']} es alérgico al {medicamento}.")''')])})

crear("I04", "Nuevo precio de la urgencia", "regla", """
Desde el 1 de noviembre la consulta de urgencia cuesta 70 euros (ahora son 60). Cambiadlo
en el programa y en la lista de precios.
""", "Marta (gerencia)",
      {"objetivo": "Que la urgencia cueste 70 euros en el programa y en la lista de precios.",
       "rutas_permitidas": ["config.py", "docs/tarifas.md", "tests/test_config.py"],
       "rutas_prohibidas": PROHIBIDAS,
       "criterios_aceptacion": ["config.TARIFAS['urgencia'] es 70.",
                                "docs/tarifas.md dice 70,00 € para la urgencia.",
                                "La prueba que comprobaba el precio antiguo se actualiza."]},
      '''
"""Incidencia I04: la urgencia cuesta 70 euros."""
import unittest
from pathlib import Path

import config


class PruebasI04(unittest.TestCase):

    def test_precio(self):
        self.assertEqual(config.TARIFAS["urgencia"], 70.0)
        self.assertEqual(config.TARIFAS["consulta"], 35.0)

    def test_lista(self):
        texto = Path("docs/tarifas.md").read_text(encoding="utf-8")
        self.assertIn("| Urgencia | 70,00 € |", texto)
        self.assertNotIn("60,00 €", texto)
''',
      {"config.py": sustituir("config.py", [('"urgencia": 60.0,', '"urgencia": 70.0,')]),
       "docs/tarifas.md": sustituir("docs/tarifas.md", [("| Urgencia | 60,00 € |",
                                                         "| Urgencia | 70,00 € |")]),
       "tests/test_config.py": sustituir("tests/test_config.py", [
           ('config.TARIFAS["urgencia"], 60.0', 'config.TARIFAS["urgencia"], 70.0')])})

crear("I05", "Recordatorio de cita", "funcion", """
Queremos mandar a los dueños un recordatorio de la cita el día antes. Añadid a avisos.py
`recordatorio_cita(dueno, mascota, cita)`, con el saludo y la firma del recordatorio de
vacunas, que diga el nombre de la mascota, el día (dd/mm/aaaa) y la hora de la cita.
""", "Ana (recepción)",
      {"objetivo": "Un recordatorio de cita para los dueños.",
       "rutas_permitidas": ["avisos.py", "tests/test_avisos.py"],
       "rutas_prohibidas": PROHIBIDAS + ["citas.py"],
       "criterios_aceptacion": ["recordatorio_cita saluda al dueño y firma como el recordatorio de vacunas.",
                                "Dice el nombre de la mascota, el día con formato dd/mm/aaaa y la hora."]},
      '''
"""Incidencia I05: recordatorio de cita."""
import unittest

from avisos import recordatorio_cita

MARTA = {"nombre": "Marta Fernández", "correo": "marta11@correo.es", "avisos": "correo"}
LOLA = {"nombre": "Lola", "especie": "perro"}
CITA = {"id": "CT-0200", "fecha": "2026-10-21", "hora": "10:30", "veterinario": "V1",
        "mascota": "M-001", "motivo": "revisión anual", "estado": "pendiente"}


class PruebasI05(unittest.TestCase):

    def test_recordatorio(self):
        texto = recordatorio_cita(MARTA, LOLA, CITA)
        self.assertTrue(texto.startswith("Hola, Marta:"))
        self.assertIn("Lola", texto)
        self.assertIn("21/10/2026", texto)
        self.assertIn("10:30", texto)
        self.assertTrue(texto.endswith("Clínica Veterinaria Naranco"))
''',
      {"avisos.py": sustituir("avisos.py", [
          ('"""Mensajes para los dueños: recordatorios de vacunas."""',
           '"""Mensajes para los dueños: recordatorios de vacunas y de citas."""'), (
          '''def recordatorio_vacuna(dueno, mascota, vacuna):''',
          '''def recordatorio_cita(dueno, mascota, cita):
    """Recordatorio de una cita, con el día y la hora."""
    return (f"{saludo(dueno)}\\n\\n"
            f"Te recordamos la cita de {mascota['nombre']} el "
            f"{formato_fecha(cita['fecha'])} a las {cita['hora']}."
            f"\\n\\n{FIRMA}")


def recordatorio_vacuna(dueno, mascota, vacuna):''')])})

crear("I06", "Dos citas a la misma hora", "fallo", """
Hoy la doctora Suárez tenía dos perros a las 10:00: la recepción reservó una cita en una
hora que ya estaba ocupada y el programa no dijo nada. Si la hora está ocupada, la reserva
no se tiene que hacer.
""", "Ana (recepción)",
      {"objetivo": "Que no se pueda reservar una hora que el veterinario ya tiene ocupada.",
       "rutas_permitidas": ["citas.py", "tests/test_citas.py"],
       "rutas_prohibidas": PROHIBIDAS,
       "criterios_aceptacion": ["reservar lanza ValueError si el veterinario ya tiene esa hora ocupada.",
                                "Una hora con una cita cancelada sí se puede reservar."]},
      '''
"""Incidencia I06: no se reserva una hora ocupada."""
import unittest

from citas import reservar


def agenda(estado="pendiente"):
    return [{"id": "CT-0001", "fecha": "2026-10-19", "hora": "10:00", "veterinario": "V1",
             "mascota": "M-001", "motivo": "vacunación", "estado": estado}]


class PruebasI06(unittest.TestCase):

    def test_ocupada(self):
        citas = agenda()
        with self.assertRaises(ValueError):
            reservar(citas, "V1", "M-002", "2026-10-19", "10:00", "otitis")
        self.assertEqual(len(citas), 1)

    def test_cancelada_y_otro_veterinario(self):
        self.assertEqual(reservar(agenda("cancelada"), "V1", "M-002", "2026-10-19", "10:00",
                                  "otitis"), "CT-0002")
        self.assertEqual(reservar(agenda(), "V2", "M-002", "2026-10-19", "10:00", "otitis"),
                         "CT-0002")
''',
      {"citas.py": sustituir("citas.py", [
          ('''    Lanza ValueError si la hora no es una de las horas de consulta.
    """
    if hora_cita not in horas_de_consulta():
        raise ValueError(f"A las {hora_cita} no hay consulta.")''',
           '''    Lanza ValueError si la hora no es una de las horas de consulta o si el
    veterinario ya la tiene ocupada.
    """
    if hora_cita not in horas_de_consulta():
        raise ValueError(f"A las {hora_cita} no hay consulta.")
    if hora_cita in ocupadas(citas, veterinario, fecha):
        raise ValueError(f"{veterinario} ya tiene una cita a las {hora_cita}.")''')])})

crear("I07", "El formato de los euros, en un solo sitio", "refactorizacion", """
farmacia.py y facturas.py tienen cada uno su propia función _euros, que hace lo mismo que
formato_euros de utilidades.py. Quitad las copias y usad la de utilidades. Las etiquetas y
las facturas no deben cambiar ni una coma.
""", "Dani (informática)",
      {"objetivo": "Que farmacia.py y facturas.py usen formato_euros de utilidades.py.",
       "rutas_permitidas": ["farmacia.py", "facturas.py"],
       "rutas_prohibidas": PROHIBIDAS + ["tests/", "utilidades.py"],
       "criterios_aceptacion": ["Ni farmacia.py ni facturas.py definen _euros.",
                                "Los dos usan formato_euros de utilidades.py.",
                                "Las etiquetas y las facturas salen igual que antes."]},
      '''
"""Incidencia I07: el formato de los euros, en un solo sitio."""
import unittest
from pathlib import Path

from facturas import texto_factura
from farmacia import etiqueta

FARMACIA = {"meloxicam": {"presentacion": "suspensión oral 1,5 mg/ml", "dosis_mg_kg": 0.1,
                          "especies": ["perro", "gato"], "existencias": 14, "precio": 1018.5}}
LOLA = {"nombre": "Lola", "especie": "perro", "peso_kg": 13.0, "alergias": []}
FACTURA = {"id": "F-0001", "dueno": "D-001", "fecha": "2026-10-16",
           "lineas": [{"concepto": "limpieza dental", "importe": 1120.0}]}


class PruebasI07(unittest.TestCase):

    def test_sin_copias(self):
        for archivo in ("farmacia.py", "facturas.py"):
            codigo = Path(archivo).read_text(encoding="utf-8")
            self.assertNotIn("def _euros", codigo)
            self.assertIn("formato_euros", codigo)

    def test_textos_iguales(self):
        self.assertIn("Precio: 1.018,50 €", etiqueta(FARMACIA, "meloxicam", LOLA))
        self.assertIn("1.120,00 €", texto_factura(FACTURA))
''',
      {"farmacia.py": sustituir("farmacia.py", [
          ("from utilidades import redondear", "from utilidades import formato_euros, redondear"),
          ('''def _euros(importe):
    """Un importe con dos decimales y coma: 18.5 → «18,50 €»."""
    texto = f"{importe:,.2f}".replace(",", "X").replace(".", ",")
    return texto.replace("X", ".") + " €"


''', ""),
          ('precio = _euros(farmacia[medicamento]["precio"])',
           'precio = formato_euros(farmacia[medicamento]["precio"])')]),
       "facturas.py": sustituir("facturas.py", [
          ("from utilidades import formato_fecha, redondear",
           "from utilidades import formato_euros, formato_fecha, redondear"),
          ('''def _euros(importe):
    """Un importe con dos decimales y coma: 38 → «38,00 €»."""
    texto = f"{importe:,.2f}".replace(",", "X").replace(".", ",")
    return texto.replace("X", ".") + " €"


''', ""),
          ("{_euros(linea['importe']):>12}", "{formato_euros(linea['importe']):>12}"),
          ("{_euros(partes['base']):>12}", "{formato_euros(partes['base']):>12}"),
          ("{_euros(partes['iva']):>12}", "{formato_euros(partes['iva']):>12}"),
          ("{_euros(suma):>12}", "{formato_euros(suma):>12}")])})

crear("I08", "Lo que ha pagado un dueño", "funcion", """
Algunos dueños nos piden un resumen de lo que han pagado en un periodo, para la
declaración o para el seguro de la mascota. Añadid a facturas.py
`total_dueno(facturas, dueno, desde, hasta)`, que sume las facturas del dueño entre esas
dos fechas, las dos incluidas, redondeado a céntimos.
""", "Marta (gerencia)",
      {"objetivo": "La suma de lo que ha pagado un dueño entre dos fechas.",
       "rutas_permitidas": ["facturas.py", "tests/test_facturas.py"],
       "rutas_prohibidas": PROHIBIDAS,
       "criterios_aceptacion": ["total_dueno suma las facturas del dueño entre las dos fechas, incluidas.",
                                "No cuenta las de otros dueños ni las de fuera del periodo.",
                                "Devuelve 0 si no hay ninguna, y redondea a céntimos."]},
      '''
"""Incidencia I08: lo que ha pagado un dueño."""
import unittest

from facturas import total_dueno

FACTURAS = [{"id": "F-1", "dueno": "D-001", "fecha": "2026-10-01",
             "lineas": [{"concepto": "consulta", "importe": 35.0}]},
            {"id": "F-2", "dueno": "D-001", "fecha": "2026-10-15",
             "lineas": [{"concepto": "cura", "importe": 22.1},
                        {"concepto": "desparasitación", "importe": 15.05}]},
            {"id": "F-3", "dueno": "D-002", "fecha": "2026-10-10",
             "lineas": [{"concepto": "cura", "importe": 22.0}]},
            {"id": "F-4", "dueno": "D-001", "fecha": "2026-11-02",
             "lineas": [{"concepto": "consulta", "importe": 35.0}]}]


class PruebasI08(unittest.TestCase):

    def test_periodo(self):
        self.assertEqual(total_dueno(FACTURAS, "D-001", "2026-10-01", "2026-10-15"), 72.15)
        self.assertEqual(total_dueno(FACTURAS, "D-001", "2026-10-02", "2026-10-31"), 37.15)

    def test_vacio(self):
        self.assertEqual(total_dueno(FACTURAS, "D-003", "2026-01-01", "2026-12-31"), 0)
''',
      {"facturas.py": sustituir("facturas.py", [(
          '''def _euros(importe):''',
          '''def total_dueno(facturas, dueno, desde, hasta):
    """Lo que ha pagado un dueño entre dos fechas, las dos incluidas."""
    return redondear(sum(total(f["lineas"]) for f in facturas
                         if f["dueno"] == dueno and desde <= f["fecha"] <= hasta))


def _euros(importe):''')])})
