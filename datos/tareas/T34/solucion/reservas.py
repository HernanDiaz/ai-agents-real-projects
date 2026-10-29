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
