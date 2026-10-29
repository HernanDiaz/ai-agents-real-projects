"""La farmacia de la clínica: dosis, existencias y etiquetas.

Los medicamentos son un diccionario como el de datos/farmacia.json:
{"meloxicam": {"presentacion": "…", "dosis_mg_kg": 0.1, "especies": ["perro", "gato"],
 "existencias": 14, "precio": 18.5}, …}.
"""
from utilidades import redondear


def dosis(farmacia, medicamento, mascota):
    """La dosis de un medicamento para una mascota, en mg, según su peso.

    Lanza ValueError si el medicamento no es para su especie o si la mascota es
    alérgica a él.
    """
    datos = farmacia[medicamento]
    if medicamento in mascota.get("alergias", []):
        raise ValueError(f"{mascota['nombre']} es alérgico al {medicamento}.")
    if mascota["especie"] not in datos["especies"]:
        raise ValueError(f"El {medicamento} no es para un {mascota['especie']}.")
    return {"medicamento": medicamento, "mg": redondear(datos["dosis_mg_kg"]
                                                         * mascota["peso_kg"]),
            "presentacion": datos["presentacion"]}


def disponible(farmacia, medicamento, unidades=1):
    """True si quedan al menos esas unidades del medicamento."""
    return farmacia[medicamento]["existencias"] >= unidades


def _euros(importe):
    """Un importe con dos decimales y coma: 18.5 → «18,50 €»."""
    texto = f"{importe:,.2f}".replace(",", "X").replace(".", ",")
    return texto.replace("X", ".") + " €"


def etiqueta(farmacia, medicamento, mascota):
    """La etiqueta que se pega en el envase: medicamento, mascota, dosis y precio."""
    d = dosis(farmacia, medicamento, mascota)
    precio = _euros(farmacia[medicamento]["precio"])
    return (f"{medicamento.capitalize()} ({d['presentacion']})\n"
            f"Para: {mascota['nombre']}, {mascota['peso_kg']} kg\n"
            f"Dosis: {d['mg']} mg\nPrecio: {precio}")
