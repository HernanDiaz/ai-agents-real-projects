"""Backorders for bikes that are sold out in a size."""
import config
from stock import units


def backorder(stock, ref, size, restocks):
    """Whether a bike that is sold out in a size can be backordered, and for when.
    Only bikes, with no units and with an expected restock; if the restock is not
    confirmed it is accepted without a date, so as not to promise what we don't know."""
    restock = restocks.get(ref)
    accepts = (ref.startswith(config.BIKE_PREFIXES)
               and units(stock, ref, size) == 0 and restock is not None)
    date = restock["date"] if accepts and restock["confirmed"] else None
    return {"accepts": accepts, "date": date}
