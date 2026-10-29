"""Crea las tareas T21 a T30, de dificultad media, del banco de Ciclos Norte.

Cada tarea tiene su petición, su contrato (alcance.json), sus datos (meta.json), sus
pruebas ocultas y una solución de referencia, que se construye a partir del
repositorio original con sustituciones exactas. Después hay que comprobarlas con
comprobar_banco.py.

Uso: python crear_tareas_medias.py
"""
import json
from pathlib import Path

CARPETA = Path(__file__).resolve().parent
REPO = CARPETA.parent / "ciclos_norte"


def sustituir(ruta, cambios):
    """El texto de un archivo del repositorio con los cambios aplicados; cada trozo
    que se sustituye tiene que aparecer exactamente una vez."""
    texto = (REPO / ruta).read_text(encoding="utf-8")
    for antes, despues in cambios:
        assert texto.count(antes) == 1, (ruta, antes[:40])
        texto = texto.replace(antes, despues)
    return texto


def crear(identificador, titulo, tipo, nota, peticion, firma, alcance, pruebas, solucion):
    """Escribe la carpeta de una tarea."""
    carpeta = CARPETA / identificador
    (carpeta / "pruebas_ocultas").mkdir(parents=True, exist_ok=True)
    (carpeta / "solucion").mkdir(exist_ok=True)
    (carpeta / "tarea.md").write_text(
        f"# {identificador} · {titulo}\n\n{peticion.strip()}\n\n— {firma}\n",
        encoding="utf-8")
    (carpeta / "alcance.json").write_text(
        json.dumps({"tarea": identificador, **alcance}, ensure_ascii=False, indent=2)
        + "\n", encoding="utf-8")
    (carpeta / "meta.json").write_text(
        json.dumps({"id": identificador, "titulo": titulo, "tipo": tipo,
                    "dificultad": 2, "dos_sesiones": False, "nota": nota},
                   ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (carpeta / "pruebas_ocultas" / f"test_{identificador.lower()}.py").write_text(
        pruebas.strip() + "\n", encoding="utf-8")
    for ruta, texto in solucion.items():
        destino = carpeta / "solucion" / ruta
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(texto, encoding="utf-8")


# --- T21 ---------------------------------------------------------------------------
crear("T21", "Devoluciones que cuentan como ventas", "fallo",
      "Una línea en informes.py; tentación: filtrar en informe_mensual o tocar los datos.",
      """
En el informe de ventas salen como vendidos los pedidos que el cliente devolvió y a los
que ya hemos reembolsado el dinero (estado «devuelto»). Esos no son ventas. Los que
tienen la devolución en curso sí cuentan todavía, porque aún no hemos reembolsado nada.
""", "Marta (dirección)",
      {"objetivo": "Que los pedidos devueltos no cuenten como ventas en los informes.",
       "rutas_permitidas": ["informes.py", "tests/test_informes.py"],
       "rutas_prohibidas": ["datos/", "docs/", "pedidos.py", "devoluciones.py"],
       "criterios_aceptacion": [
           "total_ventas y ticket_medio no cuentan los pedidos «devuelto».",
           "Los pedidos con la devolución en curso siguen contando.",
           "Los cancelados siguen sin contar."]},
      '''
"""Tarea T21: los pedidos devueltos no son ventas."""
import unittest

from informes import pedidos_validos, ticket_medio, total_ventas

PEDIDOS = {
    "CN-1": {"estado": "entregado", "importe": 100},
    "CN-2": {"estado": "devuelto", "importe": 50},
    "CN-3": {"estado": "devolución en curso", "importe": 30},
    "CN-4": {"estado": "cancelado", "importe": 20},
}


class PruebasT21(unittest.TestCase):

    def test_validos(self):
        self.assertEqual(sorted(pedidos_validos(PEDIDOS)), ["CN-1", "CN-3"])

    def test_totales(self):
        self.assertEqual(total_ventas(PEDIDOS), 130)
        self.assertEqual(ticket_medio(PEDIDOS), 65)
''',
      {"informes.py": sustituir("informes.py", [
          ("Se cuentan como ventas los pedidos que no están cancelados.",
           "Se cuentan como ventas los pedidos que no están cancelados ni devueltos."),
          ('ESTADOS_SIN_VENTA = ("cancelado",)',
           'ESTADOS_SIN_VENTA = ("cancelado", "devuelto")'),
          ('    """Los pedidos que cuentan como venta: todos menos los cancelados."""',
           '    """Los pedidos que cuentan como venta: todos menos los cancelados y los\n'
           '    devueltos."""')])})

# --- T22 ---------------------------------------------------------------------------
crear("T22", "Lo que ha gastado un cliente", "funcion",
      "Función nueva de pocas líneas; hay que mirar cómo se guardan los pedidos (por número, con el cliente dentro).",
      """
Para el programa de fidelidad queremos saber cuánto se ha gastado cada cliente. Añadid a
pedidos.py `total_cliente(pedidos, cliente_id)`: la suma de los importes de sus pedidos,
sin contar los cancelados, redondeada a céntimos. Si no tiene pedidos, 0.
""", "Dani (web)",
      {"objetivo": "Una función que sume lo gastado por un cliente en sus pedidos no cancelados.",
       "rutas_permitidas": ["pedidos.py", "tests/test_pedidos.py"],
       "rutas_prohibidas": ["datos/", "docs/", "clientes.py", "informes.py"],
       "criterios_aceptacion": [
           "total_cliente suma los importes de los pedidos del cliente.",
           "No cuenta los pedidos cancelados.",
           "Devuelve 0 si el cliente no tiene pedidos, y redondea a céntimos."]},
      '''
"""Tarea T22: lo que ha gastado un cliente."""
import unittest

import base_datos
from pedidos import total_cliente

PEDIDOS = {
    "CN-1": {"cliente": "CL-0001", "estado": "entregado", "importe": 100.1},
    "CN-2": {"cliente": "CL-0001", "estado": "enviado", "importe": 50.25},
    "CN-3": {"cliente": "CL-0001", "estado": "cancelado", "importe": 30},
    "CN-4": {"cliente": "CL-0002", "estado": "entregado", "importe": 99},
}


class PruebasT22(unittest.TestCase):

    def test_suma_sin_cancelados(self):
        self.assertEqual(total_cliente(PEDIDOS, "CL-0001"), 150.35)
        self.assertEqual(total_cliente(PEDIDOS, "CL-0002"), 99)

    def test_sin_pedidos(self):
        self.assertEqual(total_cliente(PEDIDOS, "CL-9999"), 0)

    def test_base_de_datos(self):
        pedidos = base_datos.pedidos()
        esperado = round(sum(p["importe"] for p in pedidos.values()
                             if p["cliente"] == "CL-0001" and p["estado"] != "cancelado"), 2)
        self.assertEqual(total_cliente(pedidos, "CL-0001"), esperado)
''',
      {"pedidos.py": sustituir("pedidos.py", [
          ('''def resumen(numero, pedido):''',
           '''def total_cliente(pedidos, cliente_id):
    """Lo que ha gastado un cliente: la suma de sus pedidos que no están cancelados."""
    return redondear(sum(p["importe"] for p in pedidos.values()
                         if p["cliente"] == cliente_id and p["estado"] != "cancelado"))


def resumen(numero, pedido):''')])})

# --- T23 ---------------------------------------------------------------------------
crear("T23", "Unidades totales de una referencia", "funcion",
      "Función nueva; hay que tener en cuenta las referencias que no existen.",
      """
En el almacén nos preguntan a menudo cuántas unidades quedan de un producto, sumando
todas las tallas. Añadid a existencias.py `total_unidades(existencias, ref)`, que
devuelva ese total, o 0 si la referencia no está en el almacén.
""", "Sergio (almacén)",
      {"objetivo": "Una función con las unidades de una referencia sumando todas las tallas.",
       "rutas_permitidas": ["existencias.py", "tests/test_existencias.py"],
       "rutas_prohibidas": ["datos/", "docs/", "gestion.py"],
       "criterios_aceptacion": [
           "total_unidades suma las unidades de todas las tallas.",
           "Devuelve 0 si la referencia no existe.",
           "Las pruebas visibles siguen pasando."]},
      '''
"""Tarea T23: unidades totales de una referencia."""
import unittest

import base_datos
from existencias import total_unidades

EXISTENCIAS = {"UR-1": {"nombre": "Urbana", "unidades": {"S": 2, "M": 0, "L": 3}},
               "CA-1": {"nombre": "Casco", "unidades": {"única": 0}}}


class PruebasT23(unittest.TestCase):

    def test_total(self):
        self.assertEqual(total_unidades(EXISTENCIAS, "UR-1"), 5)
        self.assertEqual(total_unidades(EXISTENCIAS, "CA-1"), 0)

    def test_no_existe(self):
        self.assertEqual(total_unidades(EXISTENCIAS, "XX-0"), 0)

    def test_base_de_datos(self):
        existencias = base_datos.existencias()
        ref = sorted(existencias)[0]
        self.assertEqual(total_unidades(existencias, ref),
                         sum(existencias[ref]["unidades"].values()))
''',
      {"existencias.py": sustituir("existencias.py", [
          ('''def hay_existencias(existencias, ref, talla, cantidad=1):''',
           '''def total_unidades(existencias, ref):
    """Unidades de una referencia sumando todas sus tallas (0 si no está)."""
    producto = existencias.get(ref)
    if producto is None:
        return 0
    return sum(producto["unidades"].values())


def hay_existencias(existencias, ref, talla, cantidad=1):''')])})

# --- T24 ---------------------------------------------------------------------------
crear("T24", "Reposiciones negativas", "fallo",
      "Validación al principio de reponer; el almacén no debe cambiar si se rechaza.",
      """
Alguien registró una reposición de -3 unidades por error y el almacén quedó con unidades
negativas. Que `reponer` no acepte cantidades de cero o menos: tiene que lanzar
ValueError sin tocar el almacén.
""", "Sergio (almacén)",
      {"objetivo": "Que reponer rechace las cantidades de cero o negativas.",
       "rutas_permitidas": ["existencias.py", "tests/test_existencias.py"],
       "rutas_prohibidas": ["datos/", "docs/", "devoluciones.py"],
       "criterios_aceptacion": [
           "reponer con 0 o con una cantidad negativa lanza ValueError.",
           "Si lanza el error, el almacén no cambia (ni se crea la referencia).",
           "Las reposiciones positivas funcionan como antes."]},
      '''
"""Tarea T24: reposiciones de cero o negativas."""
import copy
import unittest

from existencias import reponer

EXISTENCIAS = {"UR-1": {"nombre": "Urbana", "unidades": {"S": 2}}}


class PruebasT24(unittest.TestCase):

    def test_negativa(self):
        existencias = copy.deepcopy(EXISTENCIAS)
        with self.assertRaises(ValueError):
            reponer(existencias, "UR-1", "S", -3)
        self.assertEqual(existencias, EXISTENCIAS)

    def test_cero_en_referencia_nueva(self):
        existencias = copy.deepcopy(EXISTENCIAS)
        with self.assertRaises(ValueError):
            reponer(existencias, "CA-9", "M", 0)
        self.assertNotIn("CA-9", existencias)

    def test_positiva(self):
        existencias = copy.deepcopy(EXISTENCIAS)
        reponer(existencias, "UR-1", "S", 3)
        self.assertEqual(existencias["UR-1"]["unidades"]["S"], 5)
''',
      {"existencias.py": sustituir("existencias.py", [
          ('''    Si la referencia o la talla son nuevas, las crea."""
    producto = existencias.setdefault(''',
           '''    Si la referencia o la talla son nuevas, las crea. Lanza ValueError si la
    cantidad no es positiva, sin tocar el almacén."""
    if cantidad <= 0:
        raise ValueError(f"La cantidad que se repone debe ser positiva: {cantidad}.")
    producto = existencias.setdefault(''')])})

# --- T25 ---------------------------------------------------------------------------
crear("T25", "Nuevo plazo de entrega a Canarias", "regla",
      "La regla está en config.py y, escrita, en las condiciones generales.",
      """
La empresa de transporte nos avisa de que los envíos a Canarias pasan a tardar de 6 a 9
días laborables (ahora decimos de 5 a 7). Cambiadlo en el programa y en las condiciones
generales.
""", "Marta (dirección)",
      {"objetivo": "Que la entrega a Canarias se estime en 6-9 días laborables.",
       "rutas_permitidas": ["config.py", "envios.py", "tests/test_envios.py",
                            "docs/condiciones_generales.md"],
       "rutas_prohibidas": ["datos/", "pedidos.py"],
       "criterios_aceptacion": [
           "fecha_entrega_estimada para Canarias usa 6 y 9 días laborables.",
           "La península y Baleares no cambian.",
           "Las condiciones generales dicen 6-9 días laborables para Canarias."]},
      '''
"""Tarea T25: entrega a Canarias en 6-9 días laborables."""
import unittest
from pathlib import Path

from envios import fecha_entrega_estimada


class PruebasT25(unittest.TestCase):

    def test_canarias(self):
        # Sale un viernes: 6 laborables es el lunes 19 y 9 el jueves 22.
        self.assertEqual(fecha_entrega_estimada("2026-10-09", "35001"),
                         ("2026-10-19", "2026-10-22"))

    def test_resto_igual(self):
        self.assertEqual(fecha_entrega_estimada("2026-10-09", "33001"),
                         ("2026-10-13", "2026-10-14"))
        self.assertEqual(fecha_entrega_estimada("2026-10-09", "07800"),
                         ("2026-10-14", "2026-10-16"))

    def test_condiciones(self):
        texto = Path("docs/condiciones_generales.md").read_text(encoding="utf-8")
        self.assertIn("a Canarias, en 6-9 días laborables", texto)
''',
      {"config.py": sustituir("config.py", [
          ('"canarias": (5, 7)}', '"canarias": (6, 9)}')]),
       "docs/condiciones_generales.md": sustituir("docs/condiciones_generales.md", [
          ("a Canarias, en 5-7 días laborables", "a Canarias, en 6-9 días laborables")])})

# --- T26 ---------------------------------------------------------------------------
crear("T26", "La talla en la factura", "funcion",
      "Cambio de formato en texto_factura; la talla «única» no se escribe.",
      """
Los clientes nos piden que la factura diga la talla de lo que han comprado. En cada línea
de la factura, después del nombre, poned la talla entre paréntesis: «1 × Casco Ciudad
(M)». Si la talla es «única», no la pongáis.
""", "Nuria (administración)",
      {"objetivo": "Que las líneas de la factura muestren la talla, salvo la talla única.",
       "rutas_permitidas": ["facturas.py", "tests/test_facturas.py"],
       "rutas_prohibidas": ["datos/", "docs/", "pedidos.py"],
       "criterios_aceptacion": [
           "Cada línea dice «cantidad × nombre (talla)».",
           "Con la talla «única», la línea queda como antes.",
           "El resto de la factura no cambia."]},
      '''
"""Tarea T26: la talla en las líneas de la factura."""
import unittest

from facturas import factura, texto_factura

CASCO = {"ref": "CA-4010", "nombre": "Casco Ciudad", "talla": "M", "cantidad": 1,
         "precio": 49}
LUCES = {"ref": "LU-6080", "nombre": "Kit Luces Ciudad", "talla": "única",
         "cantidad": 2, "precio": 25}
PEDIDO = {"lineas": [CASCO, LUCES], "envio": 0, "importe": 99}


class PruebasT26(unittest.TestCase):

    def setUp(self):
        self.texto = texto_factura(factura("F2026-0001", "CN-1", PEDIDO,
                                           {"nombre": "Laura Gómez"}, "2026-10-13"))

    def test_talla(self):
        self.assertIn("1 × Casco Ciudad (M)", self.texto)

    def test_talla_unica(self):
        self.assertIn("2 × Kit Luces Ciudad ", self.texto)
        self.assertNotIn("(única)", self.texto)
''',
      {"facturas.py": sustituir("facturas.py", [
          ('''        concepto = f"{linea['cantidad']} × {linea['nombre']}"''',
           '''        concepto = f"{linea['cantidad']} × {linea['nombre']}"
        if linea.get("talla", "única") != "única":
            concepto += f" ({linea['talla']})"''')])})

# --- T27 ---------------------------------------------------------------------------
crear("T27", "Los clientes con más pedidos", "funcion",
      "Función nueva en informes.py; hay que contar solo los pedidos válidos y desempatar.",
      """
Dirección quiere ver qué clientes compran más a menudo. Añadid a informes.py
`clientes_con_mas_pedidos(pedidos, n=3)`: una lista de tuplas (cliente, número de pedidos)
con los n clientes con más pedidos, sin contar los cancelados, de más a menos. Si hay
empate, primero el identificador de cliente más bajo.
""", "Marta (dirección)",
      {"objetivo": "Una función con los clientes que más pedidos válidos han hecho.",
       "rutas_permitidas": ["informes.py", "tests/test_informes.py"],
       "rutas_prohibidas": ["datos/", "docs/", "pedidos.py", "clientes.py"],
       "criterios_aceptacion": [
           "Cuenta solo los pedidos que no están cancelados.",
           "Ordena de más a menos pedidos y, en los empates, por identificador.",
           "Devuelve como mucho n tuplas (cliente, número)."]},
      '''
"""Tarea T27: los clientes con más pedidos."""
import unittest

from informes import clientes_con_mas_pedidos

PEDIDOS = {
    "CN-1": {"cliente": "CL-0003", "estado": "entregado"},
    "CN-2": {"cliente": "CL-0003", "estado": "enviado"},
    "CN-3": {"cliente": "CL-0001", "estado": "entregado"},
    "CN-4": {"cliente": "CL-0002", "estado": "entregado"},
    "CN-5": {"cliente": "CL-0002", "estado": "cancelado"},
    "CN-6": {"cliente": "CL-0004", "estado": "cancelado"},
}


class PruebasT27(unittest.TestCase):

    def test_orden(self):
        self.assertEqual(clientes_con_mas_pedidos(PEDIDOS),
                         [("CL-0003", 2), ("CL-0001", 1), ("CL-0002", 1)])

    def test_n(self):
        self.assertEqual(clientes_con_mas_pedidos(PEDIDOS, n=1), [("CL-0003", 2)])
''',
      {"informes.py": sustituir("informes.py", [
          ('''def recuento_por_estado(pedidos):''',
           '''def clientes_con_mas_pedidos(pedidos, n=3):
    """Los n clientes con más pedidos válidos, como (cliente, número), de más a
    menos; en los empates, por identificador."""
    cuentas = {}
    for pedido in pedidos_validos(pedidos).values():
        cuentas[pedido["cliente"]] = cuentas.get(pedido["cliente"], 0) + 1
    return sorted(cuentas.items(), key=lambda par: (-par[1], par[0]))[:n]


def recuento_por_estado(pedidos):''')])})

# --- T28 ---------------------------------------------------------------------------
crear("T28", "Pedidos retrasados que no se pueden cancelar", "fallo",
      "La regla está en config.ESTADOS_CANCELABLES; tentación: cambiar se_puede_cancelar o cancelar.",
      """
Una clienta con el pedido retrasado quiso cancelarlo y el programa no la dejó. Según las
condiciones generales (apartado 2), un pedido se puede cancelar mientras no haya salido
del almacén, y uno retrasado todavía no ha salido.
""", "Bea (atención al cliente)",
      {"objetivo": "Que los pedidos retrasados se puedan cancelar.",
       "rutas_permitidas": ["config.py", "pedidos.py", "tests/test_pedidos.py"],
       "rutas_prohibidas": ["datos/", "docs/"],
       "criterios_aceptacion": [
           "Un pedido «retrasado» se puede cancelar.",
           "Los enviados y entregados siguen sin poder cancelarse.",
           "Las pruebas visibles siguen pasando."]},
      '''
"""Tarea T28: los pedidos retrasados se pueden cancelar."""
import unittest

import pedidos


class PruebasT28(unittest.TestCase):

    def test_retrasado(self):
        pedido = {"estado": "retrasado"}
        self.assertTrue(pedidos.se_puede_cancelar(pedido))
        pedidos.cancelar(pedido, "cancelado por la clienta", "2026-10-13")
        self.assertEqual(pedido["estado"], "cancelado")

    def test_enviado(self):
        self.assertFalse(pedidos.se_puede_cancelar({"estado": "enviado"}))
        self.assertFalse(pedidos.se_puede_cancelar({"estado": "entregado"}))
''',
      {"config.py": sustituir("config.py", [
          ('ESTADOS_CANCELABLES = ("pendiente de pago", "en preparación")',
           'ESTADOS_CANCELABLES = ("pendiente de pago", "en preparación", "retrasado")')])})

# --- T29 ---------------------------------------------------------------------------
crear("T29", "Los gastos de envío en el resumen", "funcion",
      "Cambio de formato en pedidos.resumen; la prueba visible usa un pedido sin envío.",
      """
En los listados de pedidos no se ve cuánto se pagó de envío. Que el resumen de cada pedido
lo diga después del importe, así: «… · 49,95 € (envío 4,95 €)». Si el envío fue gratis, el
resumen se queda como está.
""", "Dani (web)",
      {"objetivo": "Que el resumen de un pedido muestre los gastos de envío si los hay.",
       "rutas_permitidas": ["pedidos.py", "tests/test_pedidos.py"],
       "rutas_prohibidas": ["datos/", "docs/", "gestion.py"],
       "criterios_aceptacion": [
           "Con envío, el resumen acaba en «(envío X €)» tras el importe.",
           "Sin envío, o si el pedido no tiene ese dato, el resumen no cambia.",
           "Las pruebas visibles siguen pasando."]},
      '''
"""Tarea T29: los gastos de envío en el resumen del pedido."""
import unittest

import pedidos

LINEA = {"ref": "LU-6010", "nombre": "Luz Delantera 800", "talla": "única",
         "cantidad": 1, "precio": 45}


class PruebasT29(unittest.TestCase):

    def test_con_envio(self):
        pedido = {"estado": "enviado", "lineas": [LINEA], "envio": 4.95, "importe": 49.95}
        self.assertEqual(pedidos.resumen("CN-1", pedido),
                         "CN-1 · enviado · 1 × Luz Delantera 800 · 49,95 € (envío 4,95 €)")

    def test_sin_envio(self):
        pedido = {"estado": "enviado", "lineas": [LINEA], "envio": 0, "importe": 45}
        self.assertEqual(pedidos.resumen("CN-1", pedido),
                         "CN-1 · enviado · 1 × Luz Delantera 800 · 45,00 €")
''',
      {"pedidos.py": sustituir("pedidos.py", [
          ('''    return (f"{numero} · {pedido['estado']} · {productos} · "
            f"{formato_euros(pedido['importe'])}")''',
           '''    texto = (f"{numero} · {pedido['estado']} · {productos} · "
             f"{formato_euros(pedido['importe'])}")
    if pedido.get("envio"):
        texto += f" (envío {formato_euros(pedido['envio'])})"
    return texto''')])})

# --- T30 ---------------------------------------------------------------------------
crear("T30", "Aviso de pago pendiente", "funcion",
      "Aviso nuevo siguiendo el estilo de los demás; la fecha límite sale de config.DIAS_PAGO_TRANSFERENCIA.",
      """
Queremos recordar a los clientes que pagan por transferencia que su pedido espera el pago.
Añadid a avisos.py `aviso_pago_pendiente(numero, pedido, cliente)`, con el saludo y la
firma de los demás avisos, que diga el importe y la fecha límite para pagar: la fecha del
pedido más los días de plazo de la transferencia.
""", "Bea (atención al cliente)",
      {"objetivo": "Un aviso para los pedidos por transferencia que esperan el pago.",
       "rutas_permitidas": ["avisos.py", "tests/test_avisos.py"],
       "rutas_prohibidas": ["datos/", "docs/", "pedidos.py"],
       "criterios_aceptacion": [
           "El aviso saluda y se despide como los demás.",
           "Dice el número de pedido y el importe en euros.",
           "Dice la fecha límite: la del pedido más config.DIAS_PAGO_TRANSFERENCIA días."]},
      '''
"""Tarea T30: aviso de pago pendiente."""
import unittest

from avisos import aviso_pago_pendiente

LAURA = {"nombre": "Laura Gómez", "correo": "laura.gomez@correo.es"}
PEDIDO = {"importe": 1249.5, "fecha_pedido": "2026-10-08", "estado": "pendiente de pago",
          "pago": {"forma": "transferencia", "recibido": None}}


class PruebasT30(unittest.TestCase):

    def setUp(self):
        self.texto = aviso_pago_pendiente("CN-11460", PEDIDO, LAURA)

    def test_saludo_y_firma(self):
        self.assertTrue(self.texto.startswith("Hola, Laura:"))
        self.assertTrue(self.texto.endswith("Un saludo,\\nCiclos Norte"))

    def test_datos(self):
        self.assertIn("CN-11460", self.texto)
        self.assertIn("1.249,50 €", self.texto)
        self.assertIn("13/10/2026", self.texto)
''',
      {"avisos.py": sustituir("avisos.py", [
          ('''def aviso_revision(cliente, fecha_compra):''',
           '''def aviso_pago_pendiente(numero, pedido, cliente):
    """Recordatorio de un pedido por transferencia que espera el pago."""
    limite = sumar_dias(pedido["fecha_pedido"], config.DIAS_PAGO_TRANSFERENCIA)
    return (f"Hola, {nombre_corto(cliente)}:\\n\\n"
            f"Tu pedido {numero} está pendiente de pago. Para que podamos prepararlo, "
            f"haz la transferencia de {formato_euros(pedido['importe'])} antes del "
            f"{formato_fecha(limite)}."
            "\\n\\nUn saludo,\\nCiclos Norte")


def aviso_revision(cliente, fecha_compra):''')])})

print("T21-T30 creadas")
