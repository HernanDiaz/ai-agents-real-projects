# T12 · Numeración de facturas y rectificativas

La gestoría nos pide numerar las facturas de forma correlativa por año. Dos partes:
1. En facturas.py, `siguiente_numero_factura(emitidas, fecha, serie="F")`: con los números
   ya emitidos (como "F2026-0007") y la fecha, el siguiente de ese año y serie
   ("F2026-0008"); el primero de cada año es el 0001.
2. `factura_rectificativa(original, importe, numero, fecha)` para las devoluciones (serie R):
   campo `rectifica` con el número de la original, y total, base e IVA en negativo.

— Nuria (administración)
