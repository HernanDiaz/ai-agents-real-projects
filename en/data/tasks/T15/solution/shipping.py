"""Shipping zones, costs and delivery times (section 5 of the terms and conditions)."""
import config
from utils import add_business_days


def zone(zip_code):
    """Shipping zone of a ZIP code: "contiguous", "puerto_rico" or "hawaii".

    Puerto Rico ZIP codes start with 006, 007 or 009; Hawaii ones, with 967 or 968.
    """
    code = str(zip_code).strip()
    for name, prefixes in config.ZIP_PREFIXES.items():
        if code.startswith(prefixes):
            return name
    return "contiguous"


def shipping_cost(subtotal, zip_code):
    """Shipping cost of an order from the amount of its products and its destination."""
    shipping_zone = zone(zip_code)
    threshold = config.FREE_SHIPPING_THRESHOLDS.get(shipping_zone)
    if threshold is not None and subtotal > threshold:
        return 0.0
    return config.SHIPPING_RATES[shipping_zone]


def estimated_delivery(ship_date, zip_code):
    """Earliest and latest likely delivery dates, in business days counted from
    the day the order leaves the warehouse."""
    minimum, maximum = config.DELIVERY_DAYS[zone(zip_code)]
    return (add_business_days(ship_date, minimum),
            add_business_days(ship_date, maximum))
