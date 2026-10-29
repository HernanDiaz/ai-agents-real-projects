"""Crea las tareas T31 a T35 del capítulo 9: funciones nuevas que alguien pide de
palabra y que tienen decisiones que solo puede tomar la tienda.

Cada función va en un módulo nuevo, para que la tarea mida si el agente entiende lo que
se le pide y no lo bien que edita archivos que ya existen. Cada tarea tiene, además de
lo de siempre (petición, contrato, datos, pruebas ocultas y solución de referencia):
- notas.md: lo que se habló con las personas que trabajan en la tienda, sin ordenar;
- especificacion.md: la especificación escrita a partir de esas notas;
- pruebas_criterio/: las pruebas de las decisiones que el programa no debe tomar por su
  cuenta (umbrales, excepciones, lo que no hay que hacer). Las pruebas ocultas de
  siempre comprueban solo lo que pide la petición, de forma que cualquier
  interpretación razonable las pase.

Uso: python crear_tareas_espec.py; después, python comprobar_banco.py T31 T32 T33 T34 T35
"""
import json
import shutil
from pathlib import Path

CARPETA = Path(__file__).resolve().parent


def crear(identificador, titulo, nota, peticion, firma, notas, especificacion, alcance,
          pruebas, criterio, solucion):
    """Escribe la carpeta de una tarea, desde cero."""
    carpeta = CARPETA / identificador
    shutil.rmtree(carpeta, ignore_errors=True)
    for sub in ("pruebas_ocultas", "pruebas_criterio", "solucion"):
        (carpeta / sub).mkdir(parents=True, exist_ok=True)
    (carpeta / "tarea.md").write_text(
        f"# {identificador} · {titulo}\n\n{peticion.strip()}\n\n— {firma}\n",
        encoding="utf-8")
    (carpeta / "notas.md").write_text(notas.strip() + "\n", encoding="utf-8")
    (carpeta / "especificacion.md").write_text(especificacion.strip() + "\n",
                                               encoding="utf-8")
    (carpeta / "alcance.json").write_text(
        json.dumps({"tarea": identificador, **alcance}, ensure_ascii=False, indent=2)
        + "\n", encoding="utf-8")
    (carpeta / "meta.json").write_text(
        json.dumps({"id": identificador, "titulo": titulo, "tipo": "funcion",
                    "dificultad": 2, "dos_sesiones": False, "capitulo": 9,
                    "nota": nota}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (carpeta / "pruebas_ocultas" / f"test_{identificador.lower()}.py").write_text(
        pruebas.strip() + "\n", encoding="utf-8")
    (carpeta / "pruebas_criterio" / f"test_{identificador.lower()}_criterio.py").write_text(
        criterio.strip() + "\n", encoding="utf-8")
    for ruta, texto in solucion.items():
        destino = carpeta / "solucion" / ruta
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(texto.strip() + "\n", encoding="utf-8")


def contrato(objetivo, modulo, criterios, prohibidas):
    """El contrato de una tarea: el módulo nuevo y sus pruebas, nada más."""
    return {"objetivo": objetivo,
            "rutas_permitidas": [modulo, f"tests/test_{modulo}"],
            "rutas_prohibidas": ["datos/", "docs/", *prohibidas],
            "criterios_aceptacion": criterios}


# --- T31 · Baja de un cliente -----------------------------------------------------------
crear("T31", "Dar de baja a un cliente",
      "La petición dice «borrar»; la tienda no puede borrar al cliente (facturas) ni "
      "darlo de baja con pedidos en curso.",
      """
Una clienta nos ha escrito pidiendo que borremos sus datos de la tienda. Haced un módulo
nuevo, bajas.py, con una función `baja(clientes, pedidos, cliente_id)` para dar de baja
a un cliente que lo pida. Los clientes y los pedidos son diccionarios como los de
datos/clientes.json y datos/pedidos.json: cada pedido tiene su cliente en «cliente» y su
«estado».
""", "Bea (atención al cliente)",
      """
Notas de una conversación con Bea (atención al cliente) y con la gestoría, el 20 de
octubre.

- Bea: «Nos escriben dos o tres al mes pidiendo que los borremos. Ahora lo hago a mano
  en la hoja de clientes y siempre tengo miedo de romper algo.»
- La gestoría: las facturas hay que guardarlas seis años, y en cada factura sale el
  identificador del cliente. Si el cliente desaparece de la lista, las facturas viejas
  se quedan apuntando a nada. Lo que se borra son los datos personales: nombre y correo.
- La ciudad no es un dato personal por sí sola y la usamos en los informes; se puede
  quedar.
- Bea: «Lo que hago es poner "Cliente dado de baja" en el nombre y borrar el correo.»
- Si se da de baja, que no le llegue publicidad, claro.
- Bea, sobre los pedidos: «Si tiene un pedido sin entregar o una devolución a medias,
  no lo toco: le escribo primero para cerrar lo pendiente. Eso lo decido yo, no quiero
  que el programa lo haga solo.» Pedidos en curso son los que están pendientes de pago,
  en preparación, enviados, retrasados o con una devolución en curso.
- Al final, le gustaría que la función le dijera si lo ha hecho o si se ha quedado
  pendiente.
- (Comentario de Dani, de la web: el formulario de contacto a veces manda el correo en
  mayúsculas. No tiene que ver con esto.)
""",
      """
# Especificación · Dar de baja a un cliente

**Objetivo.** Que un cliente que lo pide deje de tener sus datos personales en la
tienda, sin romper las facturas que hay que conservar.

**Qué hace.** `baja(clientes, pedidos, cliente_id)`, en el módulo nuevo `bajas.py`:
- cambia el nombre del cliente por «Cliente dado de baja», deja el correo vacío ("") y
  pone `publicidad` a False;
- deja al cliente en el diccionario `clientes`, con su identificador y su ciudad;
- devuelve «hecho».

**Decisiones que no toma el programa.** Si el cliente tiene algún pedido en curso
(estado «pendiente de pago», «en preparación», «enviado», «retrasado» o «devolución en
curso»), la función no cambia nada y devuelve «pendiente»: atención al cliente cierra
antes lo pendiente.

**Fuera de alcance.** Borrar pedidos o facturas; cambiar el formulario de la web.

**Criterios de aceptación.**
1. Tras la baja, el nombre y el correo del cliente ya no están en `clientes`.
2. El cliente sigue en `clientes`, con su ciudad, y sin publicidad.
3. Con un pedido en curso, no cambia nada y devuelve «pendiente»; si no, devuelve «hecho».
""",
      contrato("Dar de baja a un cliente que lo pide.", "bajas.py", [
          "Tras la baja, el nombre y el correo del cliente ya no están en clientes.",
          "El cliente sigue en clientes, con su ciudad, y sin publicidad.",
          "Con un pedido en curso no cambia nada y devuelve «pendiente»; si no, «hecho»."],
          ["clientes.py", "pedidos.py", "facturas.py"]),
      '''
"""Tarea T31: dar de baja a un cliente (lo que pide la petición)."""
import json
import unittest

from bajas import baja


class PruebasT31(unittest.TestCase):

    def test_borra_nombre_y_correo(self):
        clientes = {"CL-0001": {"nombre": "Laura Gómez", "correo": "laura@correo.es",
                                "ciudad": "Valladolid", "publicidad": True}}
        pedidos = {"CN-1": {"cliente": "CL-0001", "estado": "entregado", "importe": 50}}
        baja(clientes, pedidos, "CL-0001")
        texto = json.dumps(clientes, ensure_ascii=False)
        self.assertNotIn("Laura", texto)
        self.assertNotIn("laura@correo.es", texto)
''',
      '''
"""Tarea T31: las decisiones de la tienda al dar de baja a un cliente."""
import unittest

from bajas import baja


def datos(estado="entregado"):
    clientes = {"CL-0001": {"nombre": "Laura Gómez", "correo": "laura@correo.es",
                            "ciudad": "Valladolid", "publicidad": True}}
    pedidos = {"CN-1": {"cliente": "CL-0001", "estado": estado, "importe": 50}}
    return clientes, pedidos


class CriterioT31(unittest.TestCase):

    def test_no_borra_al_cliente(self):
        clientes, pedidos = datos()
        self.assertEqual(baja(clientes, pedidos, "CL-0001"), "hecho")
        self.assertIn("CL-0001", clientes)
        self.assertEqual(clientes["CL-0001"]["ciudad"], "Valladolid")
        self.assertFalse(clientes["CL-0001"]["publicidad"])

    def test_pedido_en_curso(self):
        for estado in ("pendiente de pago", "en preparación", "enviado", "retrasado",
                       "devolución en curso"):
            clientes, pedidos = datos(estado)
            self.assertEqual(baja(clientes, pedidos, "CL-0001"), "pendiente", estado)
            self.assertEqual(clientes["CL-0001"]["nombre"], "Laura Gómez", estado)
''',
      {"bajas.py": '''
"""Bajas de clientes que lo piden (apartado 11 de las condiciones generales)."""

EN_CURSO = ("pendiente de pago", "en preparación", "enviado", "retrasado",
            "devolución en curso")


def baja(clientes, pedidos, cliente_id):
    """Da de baja a un cliente que lo pide: borra su nombre y su correo y le quita la
    publicidad, pero lo deja en la lista, porque sus facturas se conservan seis años.
    Si tiene algún pedido en curso no cambia nada: lo decide atención al cliente.
    Devuelve «hecho» o «pendiente»."""
    if any(pedido["cliente"] == cliente_id and pedido["estado"] in EN_CURSO
           for pedido in pedidos.values()):
        return "pendiente"
    clientes[cliente_id].update({"nombre": "Cliente dado de baja", "correo": "",
                                 "publicidad": False})
    return "hecho"
'''})


# --- T32 · Presupuestos caros -----------------------------------------------------------
crear("T32", "Avisar de los presupuestos caros",
      "«Caro» no tiene número en la petición; y una pieza sin precio no se puede "
      "presupuestar sola.",
      """
En el taller queremos saber cuándo un presupuesto de reparación sale caro, para llamar
al cliente antes de empezar. Haced un módulo nuevo, aprobaciones.py, con una función
`presupuesto_con_aprobacion(piezas, horas, fecha_compra, hoy, causa)` que haga el
presupuesto con `presupuesto_reparacion` (de presupuestos.py) y le añada un campo
`aprobacion`: True si hay que llamar al cliente. «piezas» es una lista de (nombre,
precio), como en `presupuesto_reparacion`.
""", "Iván (taller)",
      """
Notas de una conversación con Iván (taller), el 21 de octubre.

- Iván: «Cuando una reparación pasa de 150 euros, llamamos siempre al cliente antes de
  tocar nada. Por debajo, si nos dejó la bici para arreglarla, la arreglamos.»
- Lo de los 150 euros es con IVA, lo que paga el cliente, el total del presupuesto.
- A veces apuntamos una pieza que hay que pedir y todavía no sabemos cuánto cuesta. En la
  hoja la ponemos sin precio (None). Iván: «Ahí no se puede dar un total: le llamamos
  cuando lo sepamos.» No quiere que el programa invente un precio ni que la cuente como
  gratis.
- Con una pieza sin precio, el presupuesto no tiene total, y hay que llamar.
- Iván sugirió hacer descuentos a los clientes de siempre en las reparaciones grandes.
  Marta (dirección) dijo que de eso nada sin hablarlo antes: no entra.
- (Sobre el texto del presupuesto: les gustaría poner el teléfono del taller abajo. Otro
  día.)
""",
      """
# Especificación · Avisar de los presupuestos caros

**Objetivo.** Que el taller sepa qué presupuestos necesitan la aprobación del cliente
antes de empezar.

**Qué hace.** `presupuesto_con_aprobacion(piezas, horas, fecha_compra, hoy, causa)`, en
el módulo nuevo `aprobaciones.py`, devuelve el presupuesto de `presupuesto_reparacion`
con un campo más, `aprobacion`:
- True si el total supera 150 euros (IVA incluido); False si es de 150 o menos.
- El umbral es una constante del módulo, `UMBRAL_APROBACION = 150`.

**Decisiones que no toma el programa.** Si alguna pieza tiene precio `None` (todavía no
se sabe), no se llama a `presupuesto_reparacion` ni se inventa un precio: devuelve
`{"total": None, "aprobacion": True}`. Los descuentos no entran.

**Fuera de alcance.** El texto del presupuesto; descuentos; cambiar presupuestos.py.

**Criterios de aceptación.**
1. `aprobacion` es True en un presupuesto caro y False en uno barato.
2. El umbral es 150 euros: 150,01 pide aprobación y 150 no.
3. Con una pieza sin precio, el total es None y `aprobacion` es True.
""",
      contrato("Que el presupuesto de reparación diga si hay que pedir aprobación.",
               "aprobaciones.py", [
                   "aprobacion es True en un presupuesto caro y False en uno barato.",
                   "El umbral es 150 euros: 150,01 pide aprobación y 150 no.",
                   "Con una pieza sin precio, el total es None y aprobacion es True."],
               ["presupuestos.py", "config.py", "facturas.py"]),
      '''
"""Tarea T32: avisar de los presupuestos caros (lo que pide la petición)."""
import unittest

from aprobaciones import presupuesto_con_aprobacion

ANTIGUA = "2020-01-10"   # sin garantía
HOY = "2026-10-13"


class PruebasT32(unittest.TestCase):

    def test_caro(self):
        p = presupuesto_con_aprobacion([("Horquilla", 320)], 2, ANTIGUA, HOY, "desgaste")
        self.assertTrue(p["aprobacion"])
        self.assertEqual(p["total"], 380)

    def test_barato(self):
        p = presupuesto_con_aprobacion([("Cámara", 6)], 0.5, ANTIGUA, HOY, "desgaste")
        self.assertFalse(p["aprobacion"])
''',
      '''
"""Tarea T32: las decisiones del taller sobre los presupuestos caros."""
import unittest

from aprobaciones import presupuesto_con_aprobacion

ANTIGUA = "2020-01-10"
HOY = "2026-10-13"


class CriterioT32(unittest.TestCase):

    def test_umbral(self):
        justo = presupuesto_con_aprobacion([("Rueda", 120)], 1, ANTIGUA, HOY, "desgaste")
        encima = presupuesto_con_aprobacion([("Rueda", 120.01)], 1, ANTIGUA, HOY,
                                            "desgaste")
        self.assertFalse(justo["aprobacion"])
        self.assertTrue(encima["aprobacion"])

    def test_pieza_sin_precio(self):
        p = presupuesto_con_aprobacion([("Cadena", 24.9), ("Motor", None)], 2, ANTIGUA,
                                       HOY, "desgaste")
        self.assertIsNone(p["total"])
        self.assertTrue(p["aprobacion"])
''',
      {"aprobaciones.py": '''
"""Presupuestos del taller que necesitan la aprobación del cliente antes de empezar."""
from presupuestos import presupuesto_reparacion

UMBRAL_APROBACION = 150   # euros, IVA incluido: por encima se llama al cliente


def presupuesto_con_aprobacion(piezas, horas, fecha_compra, hoy, causa):
    """El presupuesto de una reparación con un campo más, «aprobacion»: si hay que
    llamar al cliente antes de empezar. Si alguna pieza no tiene precio todavía, no hay
    total y hay que llamar: el taller no inventa precios."""
    if any(precio is None for _, precio in piezas):
        return {"total": None, "aprobacion": True}
    presupuesto = presupuesto_reparacion(piezas, horas, fecha_compra, hoy, causa)
    return dict(presupuesto, aprobacion=presupuesto["total"] > UMBRAL_APROBACION)
'''})


# --- T33 · Aviso de retraso -------------------------------------------------------------
crear("T33", "Avisar de un pedido retrasado",
      "La petición no dice cuándo avisar ni qué no se puede prometer.",
      """
Cuando un pedido se retrasa, el cliente se entera porque nos llama. Haced un módulo
nuevo, retrasos.py, con una función `aviso_retraso(numero, pedido, cliente,
fecha_anterior)` que le cuente el retraso y la nueva fecha, con el saludo y la firma de
los avisos de avisos.py (`nombre_corto` está en clientes.py, y `formato_fecha`, en
utilidades.py). El pedido ya viene marcado como retrasado, con su motivo
(`pedido["motivo"]`) y su nueva entrega prevista (`pedido["entrega_prevista"]`).
""", "Bea (atención al cliente)",
      """
Notas de una conversación con Bea (atención al cliente) y Marta (dirección), el 22 de
octubre.

- Bea: «Cuando se retrasa un pedido, la gente llama enfadada. Si les avisamos antes,
  llaman menos.»
- El aviso tiene que decir el número del pedido, por qué se retrasa (el motivo que
  apunta el almacén) y la nueva fecha prevista.
- Bea: «Si el retraso es de un día o dos, no mandes nada: llega casi a tiempo y el aviso
  asusta más que ayuda.» Se avisa solo si la nueva fecha es más de 2 días posterior a
  la que tenía.
- Marta: «En el aviso no se promete nada: ni descuentos, ni envío gratis, ni regalos, ni
  devolver el dinero. Si un cliente pide una compensación, eso lo decide Bea caso por
  caso.»
- Si el cliente quiere cancelar, que conteste al correo; Bea lo mira.
- (Bea pidió también que el aviso de envío lleve el teléfono de la tienda. Es otra
  tarea.)
""",
      """
# Especificación · Avisar de un pedido retrasado

**Objetivo.** Que el cliente sepa por nosotros que su pedido se retrasa, antes de tener
que llamar.

**Qué hace.** `aviso_retraso(numero, pedido, cliente, fecha_anterior)`, en el módulo
nuevo `retrasos.py`, devuelve el texto del aviso, con el saludo («Hola, …:», con
`nombre_corto` de clientes.py) y la firma («Un saludo, Ciclos Norte») de los demás
avisos, el número del pedido, el motivo del retraso (`pedido["motivo"]`), la nueva fecha
prevista (`pedido["entrega_prevista"]`, con `formato_fecha` de utilidades.py) y que, si
quiere cancelarlo, puede contestar a ese correo.

**Decisiones que no toma el programa.**
- Si la nueva fecha es como mucho 2 días posterior a `fecha_anterior`, no se avisa: la
  función devuelve None.
- El aviso no ofrece compensaciones: ni descuentos, ni envío gratis, ni regalos, ni
  reembolsos. Eso lo decide atención al cliente.

**Fuera de alcance.** El aviso de envío; enviar el correo; cambiar avisos.py.

**Criterios de aceptación.**
1. El aviso saluda al cliente, dice el número, el motivo y la nueva fecha, y firma como
   los demás.
2. Con un retraso de 2 días o menos devuelve None.
3. El texto no promete descuentos, envío gratis, regalos ni reembolsos.
""",
      contrato("Avisar al cliente de que su pedido se retrasa.", "retrasos.py", [
          "El aviso saluda, dice el número, el motivo y la nueva fecha, y firma.",
          "Con un retraso de 2 días o menos devuelve None.",
          "No promete descuentos, envío gratis, regalos ni reembolsos."],
          ["avisos.py", "pedidos.py"]),
      '''
"""Tarea T33: avisar de un pedido retrasado (lo que pide la petición)."""
import unittest

from retrasos import aviso_retraso

CLIENTE = {"nombre": "Laura Gómez", "correo": "laura@correo.es", "ciudad": "Valladolid"}
PEDIDO = {"cliente": "CL-0001", "estado": "retrasado",
          "motivo": "falta una pieza del proveedor", "entrega_prevista": "2026-10-28"}


class PruebasT33(unittest.TestCase):

    def test_aviso(self):
        texto = aviso_retraso("CN-10500", PEDIDO, CLIENTE, "2026-10-20")
        self.assertIn("Hola, Laura", texto)
        self.assertIn("CN-10500", texto)
        self.assertIn("28/10/2026", texto)
        self.assertIn("Ciclos Norte", texto)
''',
      '''
"""Tarea T33: las decisiones de la tienda sobre el aviso de retraso."""
import unittest

from retrasos import aviso_retraso

CLIENTE = {"nombre": "Laura Gómez", "correo": "laura@correo.es", "ciudad": "Valladolid"}


def pedido(fecha):
    return {"cliente": "CL-0001", "estado": "retrasado",
            "motivo": "falta una pieza del proveedor", "entrega_prevista": fecha}


class CriterioT33(unittest.TestCase):

    def test_retraso_corto(self):
        self.assertIsNone(aviso_retraso("CN-1", pedido("2026-10-22"), CLIENTE, "2026-10-20"))
        self.assertIsNotNone(aviso_retraso("CN-1", pedido("2026-10-23"), CLIENTE,
                                           "2026-10-20"))

    def test_motivo_y_sin_promesas(self):
        texto = aviso_retraso("CN-1", pedido("2026-10-28"), CLIENTE, "2026-10-20")
        self.assertIn("falta una pieza del proveedor", texto)
        for palabra in ("descuento", "gratis", "regalo", "compens", "reembols"):
            self.assertNotIn(palabra, texto.lower())
''',
      {"retrasos.py": '''
"""Avisos a los clientes cuyo pedido se retrasa."""
from clientes import nombre_corto
from utilidades import dias_entre, formato_fecha


def aviso_retraso(numero, pedido, cliente, fecha_anterior):
    """Aviso de que el pedido se retrasa, con el motivo y la nueva fecha; None si el
    retraso es de dos días o menos. No promete compensaciones: las decide atención al
    cliente."""
    nueva = pedido["entrega_prevista"]
    if dias_entre(fecha_anterior, nueva) <= 2:
        return None
    return (f"Hola, {nombre_corto(cliente)}:\\n\\n"
            f"Tu pedido {numero} se va a retrasar: {pedido['motivo']}. La nueva fecha "
            f"de entrega prevista es el {formato_fecha(nueva)}. Si prefieres "
            f"cancelarlo, contesta a este correo."
            "\\n\\nUn saludo,\\nCiclos Norte")
'''})


# --- T34 · Reservar agotados ------------------------------------------------------------
crear("T34", "Reservar bicicletas agotadas",
      "La petición no dice qué se puede reservar ni si se puede prometer una fecha.",
      """
En la web, cuando una bici está agotada en una talla, la gente se va. Queremos que puedan
reservarla. Haced un módulo nuevo, reservas.py, con una función
`reserva_agotada(existencias, ref, talla, reposiciones)` que devuelva un diccionario con
`admite` (si se puede reservar) y `fecha` (cuándo llegará). `reposiciones` dice, por
referencia, la fecha en que llega mercancía del proveedor y si está confirmada:
{"UR-5120": {"fecha": "2026-11-10", "confirmada": True}}. Las existencias son como las
de datos/existencias.json, y `unidades(existencias, ref, talla)`, de existencias.py, da
las unidades de una talla.
""", "Dani (web)",
      """
Notas de una conversación con Dani (web) y Marta (dirección), el 23 de octubre.

- Dani: «Si una talla está agotada y no damos opción, el cliente compra en otra tienda.»
- Solo se reservan bicicletas (referencias que empiezan por UR, MT, CR, EL o IN, como
  `PREFIJOS_BICICLETA` en config.py). Los accesorios no: se reponen enseguida y no
  compensa.
- Solo tiene sentido reservar si la talla está agotada. Si hay unidades, que la compre.
- Marta: «Si el proveedor no nos ha dado fecha de reposición, no se reserva: no podemos
  tener a la gente esperando sin saber hasta cuándo.»
- Marta: «Y si la fecha no está confirmada, no la enseñes. Se puede reservar, pero sin
  prometer fecha: ya les avisaremos.» Las fechas sin confirmar cambian casi siempre.
- (Dani preguntó si se podría cobrar una señal. Marta: no por ahora.)
""",
      """
# Especificación · Reservar bicicletas agotadas

**Objetivo.** Que un cliente pueda reservar una bicicleta agotada en su talla, sin
prometerle lo que no sabemos.

**Qué hace.** `reserva_agotada(existencias, ref, talla, reposiciones)`, en el módulo
nuevo `reservas.py`, devuelve `{"admite": bool, "fecha": str o None}`:
- admite la reserva si la referencia es de bicicleta (`config.PREFIJOS_BICICLETA`), la
  talla tiene 0 unidades (`unidades` de existencias.py) y hay una reposición prevista
  para esa referencia;
- la fecha es la de la reposición si está confirmada.

**Decisiones que no toma el programa.**
- Sin reposición prevista, no se admite la reserva.
- Con la reposición sin confirmar, se admite, pero la fecha es None: no se promete.
- Los accesorios no se reservan. No se cobra señal.

**Fuera de alcance.** Guardar las reservas; avisar al cliente cuando llegue.

**Criterios de aceptación.**
1. Una bicicleta agotada con reposición confirmada se admite, con su fecha.
2. Si quedan unidades en la talla, no se admite.
3. Sin reposición, no se admite; con reposición sin confirmar, se admite sin fecha.
4. Los accesorios no se admiten.
""",
      contrato("Que se puedan reservar las bicicletas agotadas.", "reservas.py", [
          "Una bicicleta agotada con reposición confirmada se admite, con su fecha.",
          "Si quedan unidades en la talla, no se admite.",
          "Sin reposición no se admite; con reposición sin confirmar, sin fecha.",
          "Los accesorios no se admiten."],
          ["existencias.py", "pedidos.py", "config.py"]),
      '''
"""Tarea T34: reservar bicicletas agotadas (lo que pide la petición)."""
import unittest

from reservas import reserva_agotada

EXISTENCIAS = {"UR-5120": {"nombre": "Urbana 3", "unidades": {"S": 2, "L": 0}}}
REPOSICIONES = {"UR-5120": {"fecha": "2026-11-10", "confirmada": True}}


class PruebasT34(unittest.TestCase):

    def test_agotada(self):
        r = reserva_agotada(EXISTENCIAS, "UR-5120", "L", REPOSICIONES)
        self.assertTrue(r["admite"])
        self.assertEqual(r["fecha"], "2026-11-10")

    def test_con_unidades(self):
        self.assertFalse(reserva_agotada(EXISTENCIAS, "UR-5120", "S", REPOSICIONES)["admite"])
''',
      '''
"""Tarea T34: las decisiones de la tienda sobre las reservas."""
import unittest

from reservas import reserva_agotada

EXISTENCIAS = {"UR-5120": {"nombre": "Urbana 3", "unidades": {"L": 0}},
               "CA-2010": {"nombre": "Casco Ruta", "unidades": {"M": 0}}}


class CriterioT34(unittest.TestCase):

    def test_sin_reposicion(self):
        self.assertFalse(reserva_agotada(EXISTENCIAS, "UR-5120", "L", {})["admite"])

    def test_sin_confirmar(self):
        r = reserva_agotada(EXISTENCIAS, "UR-5120", "L",
                            {"UR-5120": {"fecha": "2026-11-10", "confirmada": False}})
        self.assertTrue(r["admite"])
        self.assertIsNone(r["fecha"])

    def test_accesorio(self):
        r = reserva_agotada(EXISTENCIAS, "CA-2010", "M",
                            {"CA-2010": {"fecha": "2026-11-10", "confirmada": True}})
        self.assertFalse(r["admite"])
''',
      {"reservas.py": '''
"""Reservas de bicicletas agotadas en una talla."""
import config
from existencias import unidades


def reserva_agotada(existencias, ref, talla, reposiciones):
    """Si se puede reservar una bicicleta agotada en una talla, y para cuándo. Solo
    bicicletas, sin unidades y con una reposición prevista; si la reposición no está
    confirmada se admite sin fecha, para no prometer lo que no se sabe."""
    reposicion = reposiciones.get(ref)
    admite = (ref.startswith(config.PREFIJOS_BICICLETA)
              and unidades(existencias, ref, talla) == 0 and reposicion is not None)
    fecha = reposicion["fecha"] if admite and reposicion["confirmada"] else None
    return {"admite": admite, "fecha": fecha}
'''})


# --- T35 · Descuento de fidelidad -------------------------------------------------------
crear("T35", "Descuento para los clientes que repiten",
      "La petición no dice cuánto, a quién ni con qué límite: son decisiones de dirección.",
      """
Queremos premiar a los clientes que repiten con un descuento. Haced un módulo nuevo,
fidelidad.py, con una función `descuento_fidelidad(pedidos, cliente_id, importe, hoy)`
que devuelva los euros de descuento de una compra nueva de ese importe. Los pedidos son
un diccionario como el de datos/pedidos.json, por número de pedido: cada pedido tiene su
cliente en «cliente», su «estado» y, si ya se entregó, su «fecha_entrega» (AAAA-MM-DD).
""", "Marta (dirección)",
      """
Notas de una reunión con Marta (dirección) y Bea (atención al cliente), el 24 de octubre.

- Marta: «Quiero que los que nos compran a menudo lo noten, pero sin regalar el margen.»
- Cliente que repite: el que tiene 3 pedidos entregados o más en los últimos 365 días
  (por la fecha de entrega). Los cancelados y los que siguen sin entregar no cuentan.
- El descuento es del 5 % del importe, y solo en compras de más de 100 euros. Con tope:
  como mucho 25 euros por compra.
- Bea: «Si el cliente tiene una devolución en curso, mejor no: a veces son clientes con
  un problema abierto.» Marta: «Ahí no hay descuento automático; si hace falta, lo
  decido yo.»
- Se redondea a céntimos.
- (Marta comentó que en Navidad quizá suba al 10 %. Lo decidirá en diciembre; ahora, 5 %.)
""",
      """
# Especificación · Descuento para los clientes que repiten

**Objetivo.** Que los clientes que compran a menudo tengan un descuento, sin regalar el
margen.

**Qué hace.** `descuento_fidelidad(pedidos, cliente_id, importe, hoy)`, en el módulo
nuevo `fidelidad.py`, devuelve los euros de descuento, redondeados a céntimos:
- el 5 % del importe si el cliente tiene 3 o más pedidos entregados con `fecha_entrega`
  en los 365 días anteriores a `hoy` y el importe es de más de 100 euros;
- como mucho 25 euros;
- 0 en cualquier otro caso.

**Decisiones que no toma el programa.** Si el cliente tiene algún pedido con una
devolución en curso, el descuento es 0: lo decide dirección. Ni el porcentaje ni el tope
cambian por temporada.

**Fuera de alcance.** Aplicar el descuento al pedido; descuentos de Navidad.

**Criterios de aceptación.**
1. Un cliente con muchos pedidos entregados recientes tiene descuento; uno nuevo, no.
2. Es el 5 % en compras de más de 100 euros, con un tope de 25 euros.
3. Solo cuentan los pedidos entregados en los últimos 365 días.
4. Con una devolución en curso, el descuento es 0.
""",
      contrato("Un descuento para los clientes que repiten.", "fidelidad.py", [
          "Un cliente con muchos pedidos entregados recientes tiene descuento; uno nuevo, no.",
          "Es el 5 % en compras de más de 100 euros, con un tope de 25 euros.",
          "Solo cuentan los pedidos entregados en los últimos 365 días.",
          "Con una devolución en curso, el descuento es 0."],
          ["pedidos.py", "facturas.py", "clientes.py"]),
      '''
"""Tarea T35: descuento para los clientes que repiten (lo que pide la petición)."""
import unittest

from fidelidad import descuento_fidelidad

HOY = "2026-10-24"


def entregado(cliente, fecha):
    return {"cliente": cliente, "estado": "entregado", "importe": 80,
            "fecha_pedido": fecha, "fecha_entrega": fecha}


PEDIDOS = {f"CN-{n}": entregado("CL-0001", f"2026-0{n}-10") for n in range(1, 9)}


class PruebasT35(unittest.TestCase):

    def test_repite(self):
        self.assertGreater(descuento_fidelidad(PEDIDOS, "CL-0001", 400, HOY), 0)

    def test_nuevo(self):
        self.assertEqual(descuento_fidelidad(PEDIDOS, "CL-0099", 400, HOY), 0)
''',
      '''
"""Tarea T35: las decisiones de dirección sobre el descuento de fidelidad."""
import unittest

from fidelidad import descuento_fidelidad

HOY = "2026-10-24"


def pedido(estado, fecha):
    return {"cliente": "CL-0001", "estado": estado, "importe": 80,
            "fecha_pedido": fecha, "fecha_entrega": fecha}


TRES = {f"CN-{n}": pedido("entregado", f"2026-0{n}-10") for n in (3, 5, 7)}


class CriterioT35(unittest.TestCase):

    def test_porcentaje_y_tope(self):
        self.assertEqual(descuento_fidelidad(TRES, "CL-0001", 200, HOY), 10)
        self.assertEqual(descuento_fidelidad(TRES, "CL-0001", 1000, HOY), 25)
        self.assertEqual(descuento_fidelidad(TRES, "CL-0001", 100, HOY), 0)

    def test_solo_el_ultimo_año(self):
        viejos = {f"CN-{n}": pedido("entregado", f"2024-0{n}-10") for n in (3, 5, 7)}
        self.assertEqual(descuento_fidelidad(viejos, "CL-0001", 200, HOY), 0)
        dos = {k: v for k, v in TRES.items() if k != "CN-7"}
        self.assertEqual(descuento_fidelidad(dos, "CL-0001", 200, HOY), 0)

    def test_devolucion_en_curso(self):
        con = dict(TRES, **{"CN-9": pedido("devolución en curso", "2026-09-20")})
        self.assertEqual(descuento_fidelidad(con, "CL-0001", 200, HOY), 0)
''',
      {"fidelidad.py": '''
"""Descuento para los clientes que repiten."""
from utilidades import dias_entre, redondear


def descuento_fidelidad(pedidos, cliente_id, importe, hoy):
    """Los euros de descuento de una compra para un cliente que repite: el 5 % en
    compras de más de 100 euros, con un tope de 25, si tiene 3 pedidos entregados o más
    en el último año. Sin descuento si tiene una devolución en curso: lo decide
    dirección."""
    suyos = [p for p in pedidos.values() if p["cliente"] == cliente_id]
    if any(p["estado"] == "devolución en curso" for p in suyos):
        return 0
    recientes = [p for p in suyos if p["estado"] == "entregado"
                 and 0 <= dias_entre(p["fecha_entrega"], hoy) <= 365]
    if len(recientes) < 3 or importe <= 100:
        return 0
    return redondear(min(importe * 0.05, 25))
'''})
