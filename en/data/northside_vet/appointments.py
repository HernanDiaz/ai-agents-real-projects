"""The clinic's appointments: free slots, bookings and cancellations.

Appointments are a list of dictionaries like those of data/appointments.json:
{"id": "AP-0001", "date": "2026-10-19", "time": "11:00", "vet": "V1",
 "pet": "P-008", "reason": "annual checkup", "status": "scheduled"}.
"""
import config
from utils import to_minutes, to_time


def opening_slots():
    """The times at which an appointment can start: from opening to half an hour
    before closing, every half hour."""
    return [to_time(m) for m in range(to_minutes(config.OPENING),
                                      to_minutes(config.CLOSING),
                                      config.APPOINTMENT_MINUTES)]


def taken(appointments, vet, date):
    """The times of that day at which the vet already has an appointment that is not
    canceled."""
    return {a["time"] for a in appointments
            if a["vet"] == vet and a["date"] == date and a["status"] != "canceled"}


def free_slots(appointments, vet, date):
    """The free times of a vet on a day the clinic is open."""
    busy = taken(appointments, vet, date)
    return [t for t in opening_slots() if t not in busy]


def next_id(appointments):
    """The id of the next appointment: AP- and a sequential number."""
    highest = max((int(a["id"].removeprefix("AP-")) for a in appointments), default=0)
    return f"AP-{highest + 1:04d}"


def book(appointments, vet, pet, date, time, reason):
    """Adds a scheduled appointment and returns its id.

    Raises ValueError if the time is not one of the opening slots.
    """
    if time not in opening_slots():
        raise ValueError(f"There are no appointments at {time}.")
    appointment = {"id": next_id(appointments), "date": date, "time": time,
                   "vet": vet, "pet": pet, "reason": reason, "status": "scheduled"}
    appointments.append(appointment)
    return appointment["id"]


def cancel(appointments, appointment_id):
    """Cancels a scheduled appointment. Raises ValueError if it already took place
    or does not exist."""
    for appointment in appointments:
        if appointment["id"] == appointment_id:
            if appointment["status"] != "scheduled":
                raise ValueError(
                    f'A "{appointment["status"]}" appointment cannot be canceled.')
            appointment["status"] = "canceled"
            return appointment
    raise ValueError(f"There is no appointment {appointment_id}.")


def day_appointments(appointments, date, vet=None):
    """The appointments of a day that are not canceled, by time; of every vet or of
    one."""
    of_day = [a for a in appointments if a["date"] == date and a["status"] != "canceled"
              and (vet is None or a["vet"] == vet)]
    return sorted(of_day, key=lambda a: a["time"])
