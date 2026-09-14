"""
CSC-128 Assignment 4: Slot filling conversation logic
Calvin A. Prepetit

- This file contains the conversation logic for the auto shop appointment bot.
- It is kept separate from Streamlit so it can be tested on its own.
"""
import re

from extractors import extract_all, has_relative_date

REQUIRED = ["department", "day", "time"]
PROMPTS = {
    "department": "What type of service do you need: electrical, drivability, interior, exterior, or maintenance?",
    "day": "What day works for your appointment? Please use a weekday name.",
    "time": "What time works for you? You can enter 3pm, 3:30pm, or 15:00.",
}
LABELS = {"department": "Service", "day": "Day", "time": "Time", "vehicle_count": "Vehicles"}
CORRECTION_WORDS = ["actually", "no wait", "change that", "instead", "oops", "i meant",
                    "make it", "let s do", "lets do", "switch to", "change it to", "prefer"]
GREETING = (
    "Welcome to the Auto Shop Appointment Bot.\n\n"
    "What type of service do you need: electrical, drivability, interior, exterior, or maintenance?\n\n"
    "You can also give:\n\n"
    "- Your preferred day and time\n"
    "- The number of vehicles to be serviced\n\n"
    "Note: You may also change the appointment details as we go. For example 'Actually, Wednesday is better for me' or '9am instead.'"
)


def normalize(text):
    return " ".join(re.sub(r"[^a-z0-9\s]", " ", text.lower()).split())


def new_state():
    return {"stage": "collect", "department": None, "day": None,
            "time": None, "vehicle_count": None}


def next_missing(booking):
    for slot in REQUIRED:
        if booking[slot] is None:
            return slot
    return None


def is_correction(text):
    clean_text = normalize(text)
    return any(re.search(r"\b" + phrase + r"\b", clean_text)
               for phrase in CORRECTION_WORDS)


def booking_summary(booking):
    summary = f"{booking['department']} service on {booking['day']} at {booking['time']}"
    if booking["vehicle_count"] is not None:
        vehicles = "vehicle" if booking["vehicle_count"] == 1 else "vehicles"
        summary += f" for {booking['vehicle_count']} {vehicles}"
    return summary


def handle(text, state):
    """Return (reply, updated_state) without changing the caller's state."""
    booking = dict(state) if state else new_state()
    clean_text = normalize(text)
    if clean_text in ["restart", "start over", "cancel"]:
        return "Okay, starting over. " + GREETING, new_state()

    correction = is_correction(text)
    stage = booking["stage"]
    found = extract_all(text)

    if found["department"] and booking["department"]:
        adding_service = re.search(r"\b(?:also|too|add|as well)\b", clean_text)
        if adding_service and not re.search(r"\b(?:instead|replace)\b", clean_text):
            departments = booking["department"].split(" and ")
            for department in found["department"].split(" and "):
                if department not in departments:
                    departments.append(department)
            found["department"] = " and ".join(departments)
            correction = True

    # New details at confirmation are a request to revise the appointment.
    if stage in ["confirm", "done"] and any(
            value is not None and value != booking[slot] for slot, value in found.items()):
        correction = True

    availability = bool(re.search(r"\b(?:available|availible|availability|do you have)\b", clean_text))
    availability_note = "I can't check shop availability. I can record your preferred appointment details. " if availability else ""

    if stage == "done" and not correction:
        return availability_note + "Your appointment is already confirmed. You can request a change, such as 'make it Friday,' or type start over.", booking

    changes = []
    for slot, value in found.items():
        if value is not None and (booking[slot] is None or correction or stage == "change"):
            booking[slot] = value
            changes.append(f"{LABELS[slot]}: {value}")

    if correction and re.search(r"\b(?:remove|clear) (?:the )?vehicle count\b", clean_text):
        booking["vehicle_count"] = None
        changes.append("Vehicles: not specified")

    acknowledgement = availability_note
    if changes and (correction or stage == "change"):
        acknowledgement += "Updated " + "; ".join(changes) + ". "

    if has_relative_date(text):
        booking["day"] = None
        booking["stage"] = "collect"
        return acknowledgement + "Please give a specific weekday, such as Tuesday, without a relative date like tomorrow or next Tuesday.", booking

    if correction and not changes:
        booking["stage"] = "change"
        return availability_note + "Please give the new service department, weekday, time, or number of vehicles, such as 'Friday at 2pm'.", booking

    missing = next_missing(booking)
    if missing:
        booking["stage"] = "collect"
        return acknowledgement + PROMPTS[missing], booking

    if stage == "confirm" and not correction and not changes:
        if clean_text in ["no", "n", "no thanks", "incorrect", "not correct", "no that is not correct"]:
            booking["stage"] = "change"
            return "No problem. What would you like to change? Give a new service department, day, time, or number of vehicles.", booking
        if clean_text in ["yes", "y", "correct", "confirm", "yes please", "yes thats correct", "yes that s correct", "yes that is correct"]:
            booking["stage"] = "done"
            return "Your appointment has been confirmed: " + booking_summary(booking) + ".", booking

    if stage == "change" and not changes:
        return "What would you like to change? Give a new service department, day, time, or number of vehicles before confirming.", booking

    booking["stage"] = "confirm"
    return acknowledgement + "Please confirm: " + booking_summary(booking) + ". Is that correct? Reply yes or no, or tell me what you would like to change.", booking
