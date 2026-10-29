# T34 · Reservar bicicletas agotadas

En la web, cuando una bici está agotada en una talla, la gente se va. Queremos que puedan
reservarla. Haced un módulo nuevo, reservas.py, con una función
`reserva_agotada(existencias, ref, talla, reposiciones)` que devuelva un diccionario con
`admite` (si se puede reservar) y `fecha` (cuándo llegará). `reposiciones` dice, por
referencia, la fecha en que llega mercancía del proveedor y si está confirmada:
{"UR-5120": {"fecha": "2026-11-10", "confirmada": True}}. Las existencias son como las
de datos/existencias.json, y `unidades(existencias, ref, talla)`, de existencias.py, da
las unidades de una talla.

— Dani (web)
