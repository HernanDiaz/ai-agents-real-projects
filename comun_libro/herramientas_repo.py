"""Herramientas del agente de programación sobre una copia del repositorio.

Son las del capítulo 12 del libro anterior, crecidas para un repositorio de verdad:
el agente lista los archivos, lee por rangos de líneas, busca con expresiones
regulares, edita por sustitución exacta, ejecuta las pruebas visibles y unas pocas
órdenes permitidas. Todo ocurre en una copia temporal del repositorio, que se crea
para cada intento y se borra al final: nada de lo que haga el agente sale de ella.

Además, el módulo sabe evaluar un intento terminado: pasa las pruebas ocultas de la
tarea, calcula el diff frente al original y lista los archivos tocados fuera del
alcance. Para comprobar que todo funciona, sin ningún modelo:

    python herramientas_repo.py --prueba
"""
import difflib
import fnmatch
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

LIBRO = Path(__file__).resolve().parent.parent
REPO = LIBRO / "datos" / "ciclos_norte"
TAREAS = LIBRO / "datos" / "tareas"

SEGUNDOS_PRUEBAS = 60          # tiempo máximo para ejecutar las pruebas
SEGUNDOS_ORDEN = 30            # tiempo máximo para una orden permitida
MAX_LINEAS_LECTURA = 150       # líneas por lectura: el contexto del modelo es corto
MAX_RESULTADOS = 40            # resultados por búsqueda
MAX_SALIDA = 2500              # caracteres de salida que se devuelven al modelo
CARPETAS_IGNORADAS = {"__pycache__", ".git", "_ocultas", ".agente"}  # .agente: notas del agente
ORDEN_PRUEBAS = ["-m", "unittest", "discover", "-s", "tests"]
ORDENES_PERMITIDAS = (         # la orden debe empezar por uno de estos prefijos
    ("python", "gestion.py"),
    ("python", "-m", "unittest"),
    ("python", "-m", "py_compile"),
)


# --- La copia del repositorio ------------------------------------------------

class Espacio:
    """Una copia del repositorio en una carpeta temporal.

    «protegidos» son rutas (o carpetas acabadas en /) que el agente puede leer
    pero no editar, por ejemplo ("tests/",).
    """

    def __init__(self, origen=REPO, protegidos=()):
        """Copia el repositorio «origen» en una carpeta temporal nueva."""
        self.origen = Path(origen).resolve()
        self.carpeta = Path(tempfile.mkdtemp(prefix="ciclos_norte_")).resolve()
        shutil.copytree(self.origen, self.carpeta, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns(*CARPETAS_IGNORADAS))
        self.protegidos = tuple(protegidos)

    def ruta(self, nombre):
        """La ruta absoluta de un archivo de la copia; ValueError si intenta salir."""
        ruta = (self.carpeta / str(nombre).strip()).resolve()
        if ruta != self.carpeta and not ruta.is_relative_to(self.carpeta):
            raise ValueError(f"«{nombre}» está fuera del repositorio.")
        return ruta

    def relativa(self, ruta):
        """La ruta de un archivo relativa a la copia, con barras normales."""
        return Path(ruta).relative_to(self.carpeta).as_posix()

    def protegido(self, relativa):
        """True si la ruta (relativa) no se puede editar."""
        return coincide(relativa, self.protegidos)

    def borrar(self):
        """Borra la copia del disco."""
        shutil.rmtree(self.carpeta, ignore_errors=True)

    def __enter__(self):
        """Permite usar el espacio con «with»: se borra al salir."""
        return self

    def __exit__(self, *excepcion):
        """Borra la copia al salir del bloque «with»."""
        self.borrar()


def coincide(relativa, rutas):
    """True si la ruta relativa es una de «rutas» o está dentro de una carpeta suya
    (las carpetas acaban en /)."""
    return any(relativa == r or (r.endswith("/") and relativa.startswith(r))
               for r in rutas)


def archivos_de(carpeta):
    """Las rutas relativas de todos los archivos de una carpeta, ordenadas."""
    carpeta = Path(carpeta)
    return sorted(p.relative_to(carpeta).as_posix() for p in carpeta.rglob("*")
                  if p.is_file() and not CARPETAS_IGNORADAS & set(p.parts))


def recortar(texto, maximo=MAX_SALIDA):
    """Deja el final de un texto largo, que es donde suelen estar los errores."""
    texto = texto.strip()
    if len(texto) <= maximo:
        return texto
    return f"[… {len(texto) - maximo} caracteres omitidos …]\n" + texto[-maximo:]


def ejecutar_python(argumentos, carpeta, segundos):
    """Ejecuta el Python actual con unos argumentos dentro de una carpeta.
    Devuelve (código de salida, salida) o (None, aviso) si se pasa de tiempo."""
    entorno = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
    try:
        r = subprocess.run([sys.executable, *argumentos], cwd=carpeta, env=entorno,
                           capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=segundos)
    except subprocess.TimeoutExpired:
        return None, f"La orden ha tardado más de {segundos} segundos y se ha parado."
    return r.returncode, r.stdout + r.stderr


def resumen_unittest(salida):
    """La línea final de unittest («OK» o «FAILED (failures=1)») y el número de
    pruebas ejecutadas."""
    ejecutadas = re.search(r"Ran (\d+) tests?", salida)
    final = re.search(r"^(OK.*|FAILED.*)$", salida, re.M)
    return {"ejecutadas": int(ejecutadas.group(1)) if ejecutadas else 0,
            "resultado": final.group(1) if final else "sin resumen"}


# --- Las herramientas ---------------------------------------------------------

class Herramientas:
    """Las herramientas que el agente puede llamar, sobre un Espacio.

    Cada herramienta devuelve un diccionario que se puede pasar a JSON. Si algo
    falla, el diccionario lleva «error» y, cuando ayuda, una «pista». Todas las
    llamadas quedan en self.registro, con su resultado y su duración.
    """

    def __init__(self, espacio):
        """Prepara las herramientas sobre un espacio, con el registro vacío."""
        self.espacio = espacio
        self.registro = []

    def llamar(self, nombre, argumentos=None):
        """Ejecuta una herramienta por su nombre, como la pediría el modelo."""
        inicio = time.time()
        funcion = getattr(self, nombre, None) if nombre in NOMBRES else None
        if funcion is None:
            resultado = {"error": f"No existe la herramienta «{nombre}».",
                         "pista": "Herramientas: " + ", ".join(sorted(NOMBRES)) + "."}
        else:
            try:
                resultado = funcion(**(argumentos or {}))
            except TypeError as e:
                resultado = {"error": f"Argumentos no válidos: {e}"}
            except ValueError as e:
                resultado = {"error": str(e)}
        self.registro.append({"herramienta": nombre, "argumentos": argumentos or {},
                              "ok": "error" not in resultado,
                              "segundos": round(time.time() - inicio, 2),
                              "resultado": resultado})
        return resultado

    def listar_archivos(self, carpeta="."):
        """Los archivos de una carpeta del repositorio, con su número de líneas."""
        ruta = self.espacio.ruta(carpeta)
        if not ruta.is_dir():
            return {"error": f"No existe la carpeta «{carpeta}».",
                    "pista": "Usa «.» para la raíz del repositorio."}
        filas = []
        for relativa in archivos_de(ruta):
            texto = (ruta / relativa).read_text(encoding="utf-8", errors="replace")
            filas.append(f"{relativa} ({len(texto.splitlines())} líneas)")
        return {"carpeta": carpeta, "archivos": filas}

    def leer_archivo(self, ruta, desde=1, hasta=None):
        """Las líneas «desde»-«hasta» de un archivo, numeradas (como mucho 150)."""
        archivo = self.espacio.ruta(ruta)
        if not archivo.is_file():
            return {"error": f"No existe el archivo «{ruta}».",
                    "pista": "Usa listar_archivos para ver las rutas."}
        lineas = archivo.read_text(encoding="utf-8", errors="replace").splitlines()
        desde = max(1, int(desde))
        hasta = len(lineas) if hasta is None else min(int(hasta), len(lineas))
        if desde > len(lineas):
            return {"error": f"«{ruta}» solo tiene {len(lineas)} líneas."}
        hasta = min(hasta, desde + MAX_LINEAS_LECTURA - 1)
        numeradas = (f"{i:4d}| {lineas[i - 1]}" for i in range(desde, hasta + 1))
        contenido = "\n".join(numeradas)
        resultado = {"ruta": ruta, "lineas": f"{desde}-{hasta} de {len(lineas)}",
                     "contenido": contenido}
        if hasta < len(lineas):
            resultado["sigue"] = f"Quedan líneas: lee con desde={hasta + 1}."
        return resultado

    def buscar(self, patron, carpeta=".", archivos="*.py"):
        """Las líneas que cumplen una expresión regular, como «ruta:línea: texto»."""
        try:
            expresion = re.compile(patron)
        except re.error as e:
            return {"error": f"Expresión regular no válida: {e}.",
                    "pista": "Para buscar un texto literal, escapa ( ) [ ] . * con \\."}
        base = self.espacio.ruta(carpeta)
        if base.is_file():                     # también se puede buscar en un archivo
            base, archivos = base.parent, base.name
        if not base.is_dir():
            return {"error": f"No existe la carpeta «{carpeta}»."}
        encontradas = []
        for relativa in archivos_de(base):
            if not fnmatch.fnmatch(Path(relativa).name, archivos):
                continue
            texto = (base / relativa).read_text(encoding="utf-8", errors="replace")
            ruta = self.espacio.relativa(base / relativa)
            for numero, linea in enumerate(texto.splitlines(), 1):
                if expresion.search(linea):
                    encontradas.append(f"{ruta}:{numero}: {linea.strip()}")
        resultado = {"patron": patron, "total": len(encontradas),
                     "resultados": encontradas[:MAX_RESULTADOS]}
        if len(encontradas) > MAX_RESULTADOS:
            resultado["pista"] = "Hay más resultados: afina el patrón o la carpeta."
        return resultado

    def crear_archivo(self, ruta, contenido):
        """Crea un archivo nuevo con el contenido dado; no sobrescribe ninguno."""
        archivo = self.espacio.ruta(ruta)
        relativa = self.espacio.relativa(archivo)
        if self.espacio.protegido(relativa):
            return {"error": f"«{relativa}» está protegido: no se puede crear."}
        if archivo.exists():
            return {"error": f"«{relativa}» ya existe.",
                    "pista": "Para cambiarlo, usa editar."}
        fallo = error_de_sintaxis(relativa, contenido)
        if fallo:
            return fallo
        archivo.parent.mkdir(parents=True, exist_ok=True)
        archivo.write_text(contenido, encoding="utf-8", newline="\n")
        return {"creado": relativa, "lineas": len(contenido.splitlines())}

    def editar(self, ruta, buscar, poner):
        """Sustituye un trozo exacto de un archivo, que debe aparecer una sola vez."""
        archivo = self.espacio.ruta(ruta)
        relativa = self.espacio.relativa(archivo)
        if self.espacio.protegido(relativa):
            return {"error": f"«{relativa}» está protegido: no se puede modificar."}
        if not archivo.is_file():
            return {"error": f"No existe el archivo «{ruta}».",
                    "pista": "Usa listar_archivos para ver las rutas, o crear_archivo "
                             "para uno nuevo."}
        if buscar == "":
            return {"error": "«buscar» está vacío.",
                    "pista": "Copia el trozo exacto que quieres sustituir."}
        if re.search(r"^\s*\d+\| ", buscar, re.M):
            return {"error": "El texto a buscar lleva números de línea.",
                    "pista": "Copia el código sin el prefijo «  12| »."}
        texto = archivo.read_text(encoding="utf-8")
        veces = texto.count(buscar)
        if veces == 0:
            return {"error": "El texto a buscar no aparece en el archivo.",
                    **pista_parecido(texto, buscar)}
        if veces > 1:
            lineas = [texto[:m.start()].count("\n") + 1
                      for m in re.finditer(re.escape(buscar), texto)]
            return {"error": f"El texto a buscar aparece {veces} veces "
                             f"(líneas {', '.join(map(str, lineas))}).",
                    "pista": "Añade líneas de alrededor para que sea único."}
        inicio = texto[:texto.index(buscar)].count("\n") + 1
        nuevo = texto.replace(buscar, poner)
        fallo = error_de_sintaxis(relativa, nuevo)
        if fallo:
            return fallo
        archivo.write_text(nuevo, encoding="utf-8", newline="\n")
        return {"editado": relativa,
                "lineas": f"{inicio}-{inicio + poner.count(chr(10))}"}

    def ejecutar_pruebas(self):
        """Ejecuta las pruebas visibles (carpeta tests/) y resume el resultado."""
        codigo, salida = ejecutar_python(ORDEN_PRUEBAS, self.espacio.carpeta,
                                         SEGUNDOS_PRUEBAS)
        return {"todas_pasan": codigo == 0, **resumen_unittest(salida),
                "salida": recortar(salida)}

    def ejecutar_orden(self, orden):
        """Ejecuta una orden de la lista permitida, sin shell y dentro de la copia."""
        try:
            partes = shlex.split(orden)
        except ValueError as e:
            return {"error": f"No se entiende la orden: {e}."}
        if not any(tuple(partes[:len(p)]) == p for p in ORDENES_PERMITIDAS):
            permitidas = "; ".join(" ".join(p) + " …" for p in ORDENES_PERMITIDAS)
            return {"error": "Orden no permitida.",
                    "pista": f"Permitidas: {permitidas}"}
        for argumento in partes[1:]:
            if ".." in argumento or Path(argumento).is_absolute():
                return {"error": f"Argumento no permitido: «{argumento}».",
                        "pista": "Usa rutas relativas dentro del repositorio."}
        codigo, salida = ejecutar_python(partes[1:], self.espacio.carpeta,
                                         SEGUNDOS_ORDEN)
        return {"codigo_salida": codigo, "salida": recortar(salida)}


NOMBRES = {"listar_archivos", "leer_archivo", "buscar", "crear_archivo", "editar",
           "ejecutar_pruebas", "ejecutar_orden"}


def error_de_sintaxis(relativa, texto):
    """Si un archivo de Python quedaría con un error de sintaxis, el error con las
    líneas de alrededor tal como quedarían; None si está bien o no es Python. Así una
    edición mal sangrada no rompe el archivo: se rechaza y el archivo no cambia."""
    if not relativa.endswith(".py"):
        return None
    try:
        compile(texto, relativa, "exec")
    except SyntaxError as e:
        lineas = texto.splitlines()
        numero = e.lineno or 1
        cerca = range(max(1, numero - 3), min(len(lineas), numero + 2) + 1)
        return {"error": f"La edición dejaría «{relativa}» con un error de sintaxis "
                         f"en la línea {numero}: {e.msg}. No se ha cambiado nada.",
                "pista": "Revisa la sangría de «poner»: debe encajar con la de las "
                         "líneas de alrededor.",
                "quedaria": "\n".join(f"{i:4d}| {lineas[i - 1]}" for i in cerca)}
    return None


def pista_parecido(texto, buscar):
    """Una pista cuando el texto a buscar no aparece. Busca la línea del archivo más
    parecida a la primera línea buscada y, desde ella, la primera línea que no
    coincide, que suele delatar un espacio o una comilla distintos. Devuelve también
    el trozo real del archivo, para copiarlo tal cual."""
    if "\\n" in buscar and buscar.replace("\\n", "\n") in texto:
        return {"pista": "Has escrito «\\n» como dos caracteres: usa saltos de "
                         "línea de verdad."}
    buscadas = buscar.splitlines()
    primera = next((l for l in buscadas if l.strip()), "")
    lineas = texto.splitlines()
    parecidas = difflib.get_close_matches(primera, lineas, n=1, cutoff=0.6)
    if not parecidas:
        return {"pista": "Lee el archivo y copia el trozo exacto."}
    inicio = lineas.index(parecidas[0])
    inicio -= buscadas.index(primera)          # por si empieza con líneas vacías
    reales = lineas[max(inicio, 0):inicio + len(buscadas)]
    for k, (buscada, real) in enumerate(zip(buscadas, reales)):
        if buscada != real:
            return {"pista": f"La línea {inicio + k + 1} del archivo no coincide con "
                             f"la línea {k + 1} de tu texto: en el archivo es "
                             f"«{real}» y tú has escrito «{buscada}». Copia el trozo "
                             "real, con sus espacios.",
                    "trozo_real": "\n".join(reales)}
    return {"pista": f"El trozo empieza en la línea {inicio + 1}, pero el archivo "
                     "termina antes o sigue de otra forma. Léelo y copia el trozo "
                     "exacto."}


# --- Esquemas para el modelo --------------------------------------------------

def esquema(nombre, descripcion, parametros=None, obligatorios=()):
    """El esquema JSON de una herramienta, en el formato de las plantillas de chat.
    «parametros» es {nombre: (tipo JSON, descripción)}."""
    propiedades = {p: {"type": tipo, "description": texto}
                   for p, (tipo, texto) in (parametros or {}).items()}
    return {"type": "function", "function": {
        "name": nombre, "description": descripcion,
        "parameters": {"type": "object", "properties": propiedades,
                       "required": list(obligatorios)}}}


ESQUEMAS = [
    esquema("listar_archivos",
            "Lista los archivos de una carpeta del repositorio (y sus subcarpetas), "
            "con el número de líneas de cada uno.",
            {"carpeta": ("string", "Carpeta relativa a la raíz; «.» por defecto.")}),
    esquema("leer_archivo",
            "Lee un rango de líneas de un archivo, como mucho 150 cada vez. Cada línea "
            "lleva delante su número y una barra, que no forman parte del código.",
            {"ruta": ("string", "Ruta del archivo, por ejemplo envios.py."),
             "desde": ("integer", "Primera línea (1 por defecto)."),
             "hasta": ("integer", "Última línea (por defecto, hasta el final).")},
            ["ruta"]),
    esquema("buscar",
            "Busca una expresión regular de Python en los archivos y devuelve "
            "«ruta:línea: texto» por cada coincidencia.",
            {"patron": ("string", "Expresión regular, por ejemplo def zona."),
             "carpeta": ("string", "Carpeta o archivo donde buscar; «.» por defecto."),
             "archivos": ("string", "Patrón de nombres; *.py por defecto.")},
            ["patron"]),
    esquema("crear_archivo",
            "Crea un archivo nuevo con el contenido dado. No sobrescribe archivos que "
            "ya existen.",
            {"ruta": ("string", "Ruta del archivo nuevo, por ejemplo tests/test_x.py."),
             "contenido": ("string", "Texto completo del archivo.")},
            ["ruta", "contenido"]),
    esquema("editar",
            "Edita un archivo sustituyendo un trozo exacto, que debe aparecer una sola "
            "vez, por otro. Copia el trozo sin los números de línea.",
            {"ruta": ("string", "Ruta del archivo."),
             "buscar": ("string", "Texto exacto que se sustituye."),
             "poner": ("string", "Texto nuevo.")},
            ["ruta", "buscar", "poner"]),
    esquema("ejecutar_pruebas",
            "Ejecuta las pruebas del repositorio (carpeta tests/) y devuelve si pasan "
            "todas, el resumen y el final de la salida."),
    esquema("ejecutar_orden",
            "Ejecuta una orden permitida en la raíz del repositorio: python gestion.py "
            "…, python -m unittest … o python -m py_compile ….",
            {"orden": ("string", "La orden completa, por ejemplo "
                                 "python gestion.py agotados 2026-10-13.")},
            ["orden"]),
]


# --- Evaluar un intento ---------------------------------------------------------

def leer_tarea(identificador):
    """La petición, el alcance y los datos de una tarea del banco (T01…T20)."""
    carpeta = TAREAS / identificador

    def leer(nombre):
        """El texto de un archivo de la carpeta de la tarea."""
        return (carpeta / nombre).read_text(encoding="utf-8")

    return {"id": identificador, "carpeta": carpeta, "peticion": leer("tarea.md"),
            "alcance": json.loads(leer("alcance.json")),
            "meta": json.loads(leer("meta.json"))}


def diferencias(original, copia):
    """Qué ha cambiado en la copia: archivos modificados, nuevos y borrados, y el
    diff unificado de todos ellos."""
    antes, despues = set(archivos_de(original)), set(archivos_de(copia))
    modificados = sorted(r for r in antes & despues
                         if (Path(original) / r).read_bytes()
                         != (Path(copia) / r).read_bytes())
    nuevos, borrados = sorted(despues - antes), sorted(antes - despues)
    partes = []
    for relativa in modificados + nuevos + borrados:
        partes += difflib.unified_diff(lineas_de(Path(original) / relativa),
                                       lineas_de(Path(copia) / relativa),
                                       f"a/{relativa}", f"b/{relativa}")
    return {"modificados": modificados, "nuevos": nuevos, "borrados": borrados,
            "cambiados": modificados + nuevos + borrados, "diff": "".join(partes)}


def lineas_de(ruta):
    """Las líneas de un archivo, con su salto de línea; ninguna si no existe."""
    return ruta.read_text(encoding="utf-8").splitlines(True) if ruta.exists() else []


def comprobar_alcance(cambiados, alcance):
    """Los archivos cambiados que no están entre las rutas permitidas y los que
    están entre las prohibidas."""
    return {"fuera_de_alcance": [r for r in cambiados
                                 if not coincide(r, alcance["rutas_permitidas"])],
            "prohibidos": [r for r in cambiados
                           if coincide(r, alcance["rutas_prohibidas"])]}


def pasar_ocultas(carpeta, tarea):
    """Ejecuta las pruebas ocultas de una tarea dentro de una copia. Las copia en una
    carpeta aparte, las ejecuta y las borra, pase lo que pase."""
    destino = Path(carpeta) / "_ocultas"
    shutil.copytree(tarea["carpeta"] / "pruebas_ocultas", destino, dirs_exist_ok=True)
    try:
        codigo, salida = ejecutar_python(
            ["-m", "unittest", "discover", "-s", "_ocultas"], carpeta, SEGUNDOS_PRUEBAS)
    finally:
        shutil.rmtree(destino, ignore_errors=True)
    return {"pasan": codigo == 0, **resumen_unittest(salida),
            "salida": recortar(salida)}


def evaluar_intento(espacio, tarea):
    """Evalúa un intento terminado sobre su copia del repositorio.

    Una tarea está resuelta si pasan las pruebas ocultas y las visibles y no se ha
    tocado ninguna ruta prohibida. Los cambios fuera de las rutas permitidas se
    cuentan aparte: no invalidan la tarea, pero son trabajo que alguien revisará.
    """
    if isinstance(tarea, str):
        tarea = leer_tarea(tarea)
    cambios = diferencias(espacio.origen, espacio.carpeta)
    alcance = comprobar_alcance(cambios["cambiados"], tarea["alcance"])
    visibles = Herramientas(espacio).ejecutar_pruebas()
    ocultas = pasar_ocultas(espacio.carpeta, tarea)
    return {"tarea": tarea["id"],
            "resuelta": ocultas["pasan"] and visibles["todas_pasan"]
                        and not alcance["prohibidos"],
            "ocultas": ocultas["pasan"], "visibles": visibles["todas_pasan"],
            "pruebas_tocadas": [r for r in cambios["cambiados"]
                                if r.startswith("tests/")],
            **alcance, "cambiados": cambios["cambiados"], "diff": cambios["diff"],
            "salida_ocultas": ocultas["salida"]}


# --- Aplicar una solución con las propias herramientas -----------------------------

def sustituciones(antes, despues):
    """Convierte el cambio de un archivo en sustituciones (buscar, poner) que se
    pueden aplicar con la herramienta editar: un trozo por grupo de cambios, con
    las líneas de contexto justas para que el trozo buscado sea único."""
    viejas, nuevas = antes.splitlines(True), despues.splitlines(True)
    comparador = difflib.SequenceMatcher(None, viejas, nuevas, autojunk=False)
    for contexto in (1, 2, 3, 5, 8, 13):
        trozos = []
        for grupo in comparador.get_grouped_opcodes(contexto):
            i1, i2 = grupo[0][1], grupo[-1][2]
            j1, j2 = grupo[0][3], grupo[-1][4]
            trozos.append(("".join(viejas[i1:i2]), "".join(nuevas[j1:j2])))
        if all(buscar and antes.count(buscar) == 1 for buscar, _ in trozos):
            return trozos
    return [(antes, despues)]  # último recurso: el archivo entero


def aplicar_solucion(herramientas, carpeta_solucion):
    """Aplica una solución de referencia (los archivos cambiados) con la herramienta
    editar, trozo a trozo, como lo haría el agente. Devuelve los resultados."""
    resultados = []
    for relativa in archivos_de(carpeta_solucion):
        despues = (Path(carpeta_solucion) / relativa).read_text(encoding="utf-8")
        actual = herramientas.espacio.ruta(relativa)
        if not actual.exists():
            resultados.append(herramientas.llamar(
                "crear_archivo", {"ruta": relativa, "contenido": despues}))
            continue
        antes = actual.read_text(encoding="utf-8")
        for buscar, poner in sustituciones(antes, despues):
            resultados.append(herramientas.llamar(
                "editar", {"ruta": relativa, "buscar": buscar, "poner": poner}))
    return resultados


# --- Autocomprobación -----------------------------------------------------------------

def comprobar(condicion, descripcion):
    """Muestra una comprobación de la autoprueba y devuelve si se cumple."""
    print(("  bien  " if condicion else "  MAL   ") + descripcion)
    return condicion


def autoprueba():
    """Prueba las herramientas sin modelo: errores típicos, la solución de una tarea
    aplicada con editar, y un intento que toca una ruta prohibida."""
    bien = True
    print("Herramientas")
    with Espacio() as espacio:
        h = Herramientas(espacio)
        archivos = " ".join(h.llamar("listar_archivos")["archivos"])
        bien &= comprobar("envios.py (" in archivos, "listar_archivos ve envios.py")
        lectura = h.llamar("leer_archivo",
                           {"ruta": "pedidos.py", "desde": 5, "hasta": 8})
        bien &= comprobar(lectura["lineas"].startswith("5-8"), "leer_archivo por rango")
        bien &= comprobar("error" in h.llamar("leer_archivo", {"ruta": "../INDICE.md"}),
                          "leer_archivo no sale del repositorio")
        busqueda = h.llamar("buscar", {"patron": r"def zona\("})
        bien &= comprobar(busqueda["resultados"][0].startswith("envios.py:"),
                          "buscar encuentra def zona")
        repetido = h.llamar("editar", {"ruta": "avisos.py", "buscar": "Un saludo",
                                       "poner": "Saludos"})
        bien &= comprobar("veces" in repetido.get("error", ""),
                          "editar rechaza un trozo repetido")
        parecido = h.llamar("editar", {"ruta": "envios.py",
                                       "buscar": "def zona(codigo):", "poner": "x"})
        bien &= comprobar("def zona" in parecido.get("pista", ""),
                          "editar señala la línea más parecida")
        bien &= comprobar("error" in h.llamar("ejecutar_orden", {"orden": "rm -rf ."}),
                          "ejecutar_orden rechaza órdenes no permitidas")
        orden = h.llamar("ejecutar_orden",
                         {"orden": "python gestion.py agotados 2026-10-13"})
        bien &= comprobar(orden["codigo_salida"] == 0 and "E-Urbana 600" in
                          orden["salida"], "ejecutar_orden con gestion.py")
        bien &= comprobar(h.llamar("ejecutar_pruebas")["todas_pasan"],
                          "las pruebas visibles pasan en el original")
        bien &= comprobar(len(h.registro) == 9, "el registro guarda cada llamada")

    print("Solución de referencia de T16 aplicada con editar")
    with Espacio() as espacio:
        h = Herramientas(espacio)
        tarea = leer_tarea("T16")
        bien &= comprobar(not evaluar_intento(espacio, tarea)["ocultas"],
                          "antes, las pruebas ocultas fallan")
        ediciones = aplicar_solucion(h, tarea["carpeta"] / "solucion")
        bien &= comprobar(all("editado" in e for e in ediciones),
                          f"{len(ediciones)} ediciones sin error")
        evaluacion = evaluar_intento(espacio, tarea)
        bien &= comprobar(evaluacion["resuelta"], "después, la tarea queda resuelta")
        bien &= comprobar(not evaluacion["fuera_de_alcance"],
                          "sin cambios fuera de alcance")

    print("Un intento que arregla el dato en lugar del código (T02)")
    with Espacio() as espacio:
        h = Herramientas(espacio)
        h.llamar("editar", {"ruta": "datos/pedidos.json",
                            "buscar": '"codigo_postal": 7002',
                            "poner": '"codigo_postal": "07002"'})
        evaluacion = evaluar_intento(espacio, "T02")
        bien &= comprobar(not evaluacion["resuelta"], "no cuenta como resuelta")
        bien &= comprobar(evaluacion["prohibidos"] == ["datos/pedidos.json"],
                          "detecta la ruta prohibida")
    print("Todo bien." if bien else "Hay comprobaciones que fallan.")
    return bien


if __name__ == "__main__":
    if sys.argv[1:] == ["--prueba"]:
        sys.exit(0 if autoprueba() else 1)
    print(__doc__)
