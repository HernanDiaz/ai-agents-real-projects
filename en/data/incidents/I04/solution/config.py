"""Rules of Northside Veterinary Clinic, gathered in one place.

Prices are in US dollars and include sales tax, like those of the price list
(docs/price_list.md).
"""

SALES_TAX = 0.10

# --- Appointments ---
OPENING = "09:00"            # first appointment of the day
CLOSING = "14:00"            # the last appointment starts half an hour before
APPOINTMENT_MINUTES = 30     # minutes
OPEN_DAYS = (0, 1, 2, 3, 4)  # from Monday (0) to Friday (4)

# --- Vaccines ---
VACCINE_NOTICE_DAYS = 30     # notices for the vaccines due in the next 30 days

# --- Prices ---
PRICES = {
    "consultation": 35.0,
    "emergency visit": 70.0,
    "annual checkup": 30.0,
    "rabies vaccine": 30.0,
    "DHPP vaccine": 38.0,
    "leptospirosis vaccine": 45.0,
    "FVRCP vaccine": 36.0,
    "feline leukemia vaccine": 40.0,
    "deworming": 15.0,
    "dental cleaning": 120.0,
    "wound care": 22.0,
    "blood test": 65.0,
}
