"""CSC-128 Assignment 7: Auto Shop Service Advisor tools.
Calvin A. Prepetit

Fictional, repeating weekday schedule for this classroom demonstration.
Each browser session supplies its own request list through the dispatcher.
"""

from contextvars import ContextVar
from copy import deepcopy
import re

SHOP_HOURS = {
    "Monday": "7:30 AM to 6:00 PM",
    "Tuesday": "7:30 AM to 6:00 PM",
    "Wednesday": "7:30 AM to 6:00 PM",
    "Thursday": "7:30 AM to 6:00 PM",
    "Friday": "7:30 AM to 6:00 PM",
    "Saturday": "8:00 AM to 2:00 PM",
    "Sunday": "Closed",
}
OPENINGS = {
    "maintenance": ["Tuesday at 9:00 AM", "Thursday at 1:30 PM", "Friday at 9:00 AM"],
    "diagnostic": ["Wednesday at 10:00 AM", "Friday at 2:00 PM"],
    "brakes": ["Monday at 11:00 AM", "Saturday at 9:30 AM"],
}
SERVICE_REQUESTS = []  # Standalone default for deterministic tests.
REQUEST_STORE = ContextVar("request_store", default=SERVICE_REQUESTS)


def service_category(concern):
    """Choose an approved schedule category without diagnosing the vehicle."""
    text = concern.lower()
    # Reported faults outrank a customer's guess about routine maintenance.
    if re.search(r"\b(?:noise|knocking|rattle|shaking|vibration|slipping|leak|overheating|"
                 r"fail(?:ing|ure)?|transmission|battery|damage|curb)\b|\bwon['’]?t\s+start\b", text):
        return "diagnostic"
    if re.search(r"\b(?:oil|rotation|maintenance)\b", text):
        return "maintenance"
    if re.search(r"\bbrakes?\b", text):
        return "brakes"
    return "diagnostic"


def get_shop_hours(day="all"):
    """Return the full local schedule or the hours for 1 day."""
    if not isinstance(day, str):
        raise ValueError("day must be a weekday name or all")
    if day.strip().lower() in {"all", "week", "this week", "every day"}:
        return {"hours": dict(SHOP_HOURS)}
    day = day.strip().title()
    if day not in SHOP_HOURS:
        raise ValueError("day must be Monday through Sunday or all")
    return {"hours": {day: SHOP_HOURS[day]}}


def find_service_openings(service_type):
    """Return unreserved demo openings from the current session's store."""
    if not isinstance(service_type, str):
        raise ValueError("service_type must be a string")
    category = service_type.strip().lower()
    if re.search(r"\b(?:oil|rotation)\b", category):
        category = "maintenance"
    if category not in OPENINGS:
        raise ValueError("choose maintenance, diagnostic, or brakes")
    reserved = {f"{item['day']} at {item['time']}" for item in REQUEST_STORE.get()}
    return {"service_type": category,
            "openings": [slot for slot in OPENINGS[category] if slot not in reserved]}


def validate_request(arguments):
    """Validate exact fields before either previewing or writing a request."""
    required = {"customer_name", "vehicle", "concern", "day", "time"}
    if not isinstance(arguments, dict) or set(arguments) != required:
        raise ValueError("provide only customer_name, vehicle, concern, day, and time")
    if any(not isinstance(value, str) or not value.strip() for value in arguments.values()):
        raise ValueError("every request field must contain text")
    values = {key: value.strip() for key, value in arguments.items()}
    for key in ("customer_name", "vehicle", "concern"):
        value = values[key]
        if (re.fullmatch(r"[\[<{].*[\]>}]", value)
                or key in {"customer_name", "vehicle"} and re.search(r"[\[\]<>{}]", value)
                or value.lower() in {"name", "customer name", "vehicle", "concern", "your name", "your vehicle", "unknown", "tbd", "n/a", "not provided", "not specified", "placeholder"}):
            raise ValueError(f"{key} must be a customer-provided value, not a placeholder")
    values["day"] = values["day"].title()
    if not re.search(r"\b(?:19|20)\d{2}\b", values["vehicle"]) or len(
            re.sub(r"\b(?:19|20)\d{2}\b", "", values["vehicle"]).split()) < 2:
        raise ValueError("vehicle must include its year, make, and model")
    time = re.fullmatch(r"(0?[1-9]|1[0-2])(?::([0-5]\d))?\s*(AM|PM)", values["time"].upper())
    if not time:
        raise ValueError("time must include AM or PM, such as 9am or 1:30 PM")
    values["time"] = f"{int(time[1])}:{time[2] or '00'} {time[3]}"
    slot = f"{values['day']} at {values['time']}"
    category = service_category(values["concern"])
    if slot not in find_service_openings(category)["openings"]:
        raise ValueError(f"{slot} is not an available {category} opening")
    return values


def create_service_request(customer_name, vehicle, concern, day, time):
    """Save only a validated request; dispatch enforces prior confirmation."""
    values = validate_request(dict(customer_name=customer_name, vehicle=vehicle,
                                   concern=concern, day=day, time=time))
    records = REQUEST_STORE.get()
    request = {"request_id": f"SR-{len(records) + 1:03d}", **values}
    records.append(request)
    return deepcopy(request)


AVAILABLE_TOOLS = {
    "get_shop_hours": get_shop_hours,
    "find_service_openings": find_service_openings,
    "create_service_request": create_service_request,
}
WRITE_TOOLS = {"create_service_request"}


def schema(name, description, properties, required):
    return {"type": "function", "function": {
        "name": name, "description": description,
        "parameters": {"type": "object", "properties": properties,
                       "required": required, "additionalProperties": False}}}


TOOL_SCHEMAS = [
    schema("get_shop_hours",
           "Use this read-only tool whenever a customer asks about opening or closing hours. "
           "Use day='all' for the full week or when no day is supplied. Do not guess hours.",
           {"day": {"type": "string", "description": "Weekday name or all."}}, []),
    schema("find_service_openings",
           "Use this read-only tool when a customer asks for appointment openings or before "
           "proposing a service request. Oil change and tire rotation use maintenance. "
           "Reported noise, suspected failure, transmission trouble, or other faults take priority: "
           "use diagnostic even if the customer guesses that an oil/fluid change might fix it. "
           "Choose diagnostic for unexplained issues and brakes for brake service. "
           "Damage, wheel replacement, and other repairs use diagnostic intake, not a promise of completed repairs. "
           "Only offer times returned by this tool.",
           {"service_type": {"type": "string", "enum": list(OPENINGS)}}, ["service_type"]),
    schema("create_service_request",
           "Use this state-changing tool when the customer's name, vehicle, original concern, and an "
           "available weekday/time are collected. The application will display those exact "
           "fields and require the customer's agreement before executing the write. "
           "Request the tool once; do not repeat verbal confirmation questions. "
           "When the customer corrects both the day and time, keep their other details "
           "and call this tool immediately for a revised preview; do not ask if the selected time works. "
           "Never claim a request was saved before receiving its successful result.",
           {key: {"type": "string", "description":
                  "Copy the customer's original issue wording verbatim, not a summary." if key == "concern"
                  else "Customer-provided " + key.replace("_", " ") + "."} for key in
            ("customer_name", "vehicle", "concern", "day", "time")},
           ["customer_name", "vehicle", "concern", "day", "time"]),
]
