# T13 · Listado de existencias bajas

Queremos saber qué está a punto de agotarse. Añadid a existencias.py una función
`existencias_bajas(existencias)` que devuelva una lista de tuplas (ref, talla, unidades)
con las tallas que tienen entre 1 y 2 unidades, ordenada por referencia y, dentro de
cada referencia, en el orden de las tallas del almacén. El 2 debe estar en config.py
(MINIMO_EXISTENCIAS). Las tallas a 0 no salen: ya están en el informe de agotados.

— Sergio (almacén)
