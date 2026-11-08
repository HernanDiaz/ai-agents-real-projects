"""Business rules of North Cycles, gathered in one place.

The values come from the terms and conditions of sale (docs/terms_and_conditions.md).
Amounts are in dollars and include sales tax, like the prices on the website.
"""

SALES_TAX = 0.10

# --- Shipping (section 5) ---
SHIPPING_RATES = {"contiguous": 4.95, "puerto_rico": 9.95, "hawaii": 14.95}
FREE_SHIPPING_THRESHOLDS = {"contiguous": 60, "puerto_rico": 150}  # free above
ZIP_PREFIXES = {"puerto_rico": ("006", "007", "009"), "hawaii": ("967", "968")}
DELIVERY_DAYS = {"contiguous": (2, 3), "puerto_rico": (3, 5), "hawaii": (5, 7)}

# --- Orders and payments (sections 2 and 4) ---
PAYMENT_METHODS = ("card", "paypal", "apple_pay", "transfer")
CANCELABLE_STATUSES = ("awaiting payment", "processing")
TRANSFER_PAYMENT_DAYS = 5
INSTALLMENTS_MIN_AMOUNT = 300  # installments only on purchases over $300
INSTALLMENT_OPTIONS = (3, 6, 12)

# --- Returns (section 7) ---
RETURN_DAYS = 30
MAX_BIKE_MILES = 6
BIKE_PREFIXES = ("UR", "MT", "CR", "EL", "IN")  # product references of bikes
HYGIENE_REFS = ("RO-2050",)  # bib shorts: not accepted once unsealed
REFUND_DAYS = 14

# --- Repair shop and warranty (sections 9 and 10) ---
BASIC_TUNE_UP = 35
FREE_TUNE_UP_MONTHS = 6
SHOP_HOURLY_RATE = 30
WARRANTY_MONTHS = 24
MIN_BATTERY_CAPACITY = 0.70  # batteries must keep 70% of capacity under warranty
WEAR_PARTS = ("tire", "tube", "brake pads", "chain", "cog", "cable")
