"""
CSC-128 Assignment 4: Entity extraction (adapted from room reservation starter example)
Calvin A. Prepetit
"""
import re

DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday",
        "saturday", "sunday"]

NUMBER_WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
                "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
                "eleven": 11, "twelve": 12}

DEPARTMENT_KEYWORDS = {
    "Electrical": ["electrical", "battery", "radio", "speaker", "fuse", "wiring",
                   "alternator", "starter", "speedometer", "gauge", "light", "lights",
                   "headlights", "alarm", "key fob", "horn", "ignition", "charging"],
    "Drivability": ["drivability", "driveability", "driving", "drivin", "engine",
                    "transmission", "brake", "brakes", "stall", "stalled", "stalling",
                    "shaking", "acceleration", "accelerate", "knocking", "shift",
                    "shifting", "gear", "clutch", "fuel", "exhaust", "vibration",
                    "overheating", "overheats", "wont move", "won t move"],
    "Interior": ["interior", "seat", "seats", "dashboard", "carpet", "headliner",
                 "trim", "console", "ac", "air conditioning", "heater", "climate",
                 "vent", "airbag", "inside", "stereo"],
    "Exterior": ["exterior", "windshield", "window", "paint", "dent", "scratch",
                 "bumper", "mirror", "door", "hood", "fender", "glass", "body",
                 "grill", "roof", "crash", "collision", "outside"],
    "Maintenance": ["maintenance", "oil", "fluid", "fluids", "filter", "inspection",
                    "inspect", "alignment", "rotation", "tire pressure", "wipers",
                    "wiper blades", "coolant", "flush", "tune up", "lubrication"],
}
VEHICLE_PATTERN = (r"(?<![\w:.+-])(\d+|" + "|".join(NUMBER_WORDS)
                   + r")\s+(?:vehicles?|cars?|trucks?)\b")


def find_department(text):
    """TODO 1: return matching service departments, or None."""
    clean_text = " ".join(re.sub(r"[^a-z0-9\s]", " ", text.lower()).split())
    matches = []
    for department, keywords in DEPARTMENT_KEYWORDS.items():
        pattern = r"\b(?:" + "|".join(re.escape(word) for word in keywords) + r")\b"
        if re.search(pattern, clean_text):
            matches.append(department)
    return " and ".join(matches) if matches else None


def strip_vehicle_count(text):
    """TODO 2: remove vehicle quantities before finding time."""
    return re.sub(VEHICLE_PATTERN, " ", text, flags=re.IGNORECASE)


def has_relative_date(text):
    """Calendar-based dates are outside the assignment's scope."""
    days = "|".join(DAYS)
    pattern = (r"\b(?:today|tomorrow|yesterday|"
               r"(?:next|this|last|coming|following)\s+(?:week|" + days + r"))\b")
    return re.search(pattern, text.lower()) is not None


def find_day(text):
    """TODO 3: return a capitalized weekday name, or None."""
    if has_relative_date(text):
        return None
    pattern = r"\b(" + "|".join(DAYS) + r")\b"
    matches = set(re.findall(pattern, text.lower()))
    if len(matches) == 1:
        return matches.pop().capitalize()
    return None


def find_time(text):
    """TODO 4: handle 3pm, 3 pm, 3:30pm, and 15:00. Return None if absent."""
    pattern = r"(?<![\w:.+-])(\d{1,2})(?::(\d{2}))?\s*(am|pm)?(?![\w:])"
    times = set()
    for match in re.finditer(pattern, text.lower()):
        hour, minute, period = match.groups()
        # A bare quantity is not a time. Require a colon or am/pm.
        if minute is None and period is None:
            continue
        hour = int(hour)
        minute = int(minute or "0")
        if minute > 59 or (period and not 1 <= hour <= 12):
            continue
        if period is None and not 0 <= hour <= 23:
            continue
        if period:
            hour = hour % 12 + (12 if period == "pm" else 0)
        suffix = "AM" if hour < 12 else "PM"
        times.add(f"{hour % 12 or 12}:{minute:02d} {suffix}")
    return times.pop() if len(times) == 1 else None


def find_vehicle_count(text):
    """TODO 5: handle "4 cars", "four cars", and "just my car"."""
    lowered = text.lower()
    if re.search(r"\bboth (?:cars|trucks|vehicles)\b", lowered):
        return 2
    if re.search(r"\bjust my (?:car|truck|vehicle)\b", lowered):
        return 1
    match = re.search(VEHICLE_PATTERN, lowered)
    if match:
        value = match.group(1)
        count = int(value) if value.isdigit() else NUMBER_WORDS[value]
        return count if count > 0 else None
    return None


def extract_all(text):
    """TODO 6: run every extractor in the correct order and return a dict."""
    vehicle_count = find_vehicle_count(text)
    remaining = strip_vehicle_count(text)
    return {
        "department": find_department(remaining),
        "day": find_day(remaining),
        "time": find_time(remaining),
        "vehicle_count": vehicle_count,
    }
