"""
CSC-128 Assignment 2: Conversation logic
Calvin A. Prepetit

The conversation logic for the auto shop appointment bot is kept here so it can be tested without Streamlit.
"""

DEPARTMENT_KEYWORDS = {
    "Electrical": ["electrical", "battery", "radio", "speaker", "fuse", "wiring", "alternator", "starter", "speedometer", "meter", "gauge", "light", "lights", "dim", "alarm", "key", "key fob", "fob", "security", "horn", "lock", "locks", "unlock", "power", "charging", "ignition", "start", "starting", "turn on", "power window", "switch"],
    "Drivability": ["drivability", "driveability", "driving", "drivin", "engine", "check engine", "transmission", "brake", "brakes", "tire", "tires", "stall", "stalled", "shaking", "drive", "move", "moving", "go", "going", "goin", "anywhere", "stopped", "running", "acceleration", "accelerate", "noise", "knock", "knocking", "shift", "shifting", "gear", "clutch", "fuel", "exhaust", "vibrate", "vibration", "overheating"],
    "Interior": ["interior", "seat", "dashboard", "dial", "carpet", "headliner", "trim", "console", "ac", "air conditioning", "cold", "hot", "heater", "climate", "vent", "airbag", "inside", "stereo", "radio", "speaker"],
    "Exterior": ["exterior", "windshield", "window", "paint", "dent", "scratch", "bumper", "mirror", "door", "hood", "fender", "glass", "crack", "cracked", "broken", "body", "grill", "roof", "crash", "collision", "outside"],
    "Maintenance": ["maintenance", "oil", "change", "fluid", "fluids", "check", "checked", "chekced", "filter", "inspection", "inspect", "alignment", "rotation", "service", "tires", "brakes", "pressure", "trip", "wipers", "coolant", "flush", "tune up", "tune-up", "lubrication"],
}

SLOTS_BY_DEPARTMENT = {
    "Electrical": ["Monday 7:00 AM", "Wednesday 1:00 PM", "Friday 5:00 PM"],
    "Drivability": ["Monday 9:00 AM", "Thursday 3:00 PM", "Saturday 7:00 AM"],
    "Interior": ["Tuesday 8:00 AM", "Thursday 12:00 PM", "Sunday 2:00 PM"],
    "Exterior": ["Tuesday 10:00 AM", "Friday 3:00 PM", "Sunday 5:00 PM"],
    "Maintenance": ["Monday 7:00 AM", "Saturday 7:00 PM", "Sunday 9:00 AM"],
}

RESTART_WORDS = ["restart", "start over", "cancel"]


def format_options(options, joining_word):
    if len(options) < 3:
        return (" " + joining_word + " ").join(options)

    return ", ".join(options[:-1]) + ", " + joining_word + " " + options[-1]


DEPARTMENT_OPTIONS = format_options([department.lower() for department in DEPARTMENT_KEYWORDS], "or")

GREETING = "Welcome to the Auto Shop Appointment Bot. What type of service do you need: " + DEPARTMENT_OPTIONS + "?"


def normalize(text):
    for punctuation in ",.?!;:-":
        text = text.replace(punctuation, " ")
    return " ".join(text.lower().split())


def new_state():
    return {
        "stage": "choose_department",
        "department": "",
        "details": "",
        "slot": "",
    }


def find_department(text):
    clean_text = normalize(text)
    padded_text = " " + clean_text + " "
    best_departments = []
    best_score = 0

    for department, keywords in DEPARTMENT_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            clean_keyword = normalize(keyword)
            if " " in clean_keyword:
                score += clean_text.count(clean_keyword)
            else:
                score += padded_text.count(" " + clean_keyword + " ")

        if score and score >= best_score:
            if score > best_score:
                best_departments = []
                best_score = score
            best_departments.append(department)

    best_departments = sorted(list(set(best_departments)))
    return format_options(best_departments, "and") if best_departments else None


def find_slot(text, options):
    clean_text = normalize(text)
    compact_text = clean_text.replace(" ", "")

    for slot in options:
        clean_slot = normalize(slot)
        slot_parts = clean_slot.split()
        day = slot_parts[0]
        time_str = " ".join(slot_parts[1:])
        compact_time = time_str.replace(" ", "")
        short_time = " ".join(slot.split()[1:]).lower().replace(":00", "").replace(" ", "")

        if day in clean_text or time_str in clean_text or compact_time in compact_text or short_time in compact_text:
            return slot

    return None


def get_slots(department):
    if " and " in department or ", " in department:
        return ["Monday 7:00 AM", "Wednesday 1:00 PM", "Friday 5:00 PM", "Saturday 7:00 PM"]

    return SLOTS_BY_DEPARTMENT[department]


def slot_options(department):
    return "; ".join(get_slots(department))


def has_issue_details(text):
    return len(normalize(text).split()) >= 2


def wants_restart(text):
    clean_text = normalize(text)
    return any(word in clean_text for word in RESTART_WORDS)


def is_yes(text):
    clean_text = normalize(text)
    words = clean_text.split()
    return clean_text in ["yes", "y", "correct", "confirm"] or "yes" in words or "correct" in words


def is_no(text):
    clean_text = normalize(text)
    words = clean_text.split()
    return clean_text in ["no", "n", "incorrect"] or "no" in words or "incorrect" in words or "not correct" in clean_text


def handle(text, state):
    """
    Return (reply, updated_state).

    Stages to support:
      choose_department -> describe_issue -> choose_slot -> confirm -> done

    Also supports a restart. "start over", "cancel", and "restart" reset the conversation.
    """
    updated_state = dict(state) if state else new_state()

    if wants_restart(text):
        return "Okay, starting over. What type of service do you need: " + DEPARTMENT_OPTIONS + "?", new_state()

    stage = updated_state["stage"]

    if stage == "choose_department":
        department = find_department(text)
        if not department:
            return "I can schedule " + DEPARTMENT_OPTIONS + " work. Which service area do you need?", updated_state

        updated_state["department"] = department

        if has_issue_details(text):
            updated_state["details"] = text.strip()
            updated_state["stage"] = "choose_slot"
            return "I saved those details for " + department + " service. These are the available appointments: " + slot_options(department) + ". Which one works best?", updated_state

        updated_state["stage"] = "describe_issue"
        return "Please provide details of the " + department + " issue you are experiencing.", updated_state

    if stage == "describe_issue":
        if not text.strip():
            return "Please describe the issue you are having with the vehicle.", updated_state

        updated_state["details"] = text.strip()
        updated_state["stage"] = "choose_slot"
        return "These are the available appointments: " + slot_options(updated_state["department"]) + ". Which one works best?", updated_state

    if stage == "choose_slot":
        slot = find_slot(text, get_slots(updated_state["department"]))
        if not slot:
            return "Please choose one of these appointments: " + slot_options(updated_state["department"]) + ".", updated_state

        updated_state["slot"] = slot
        updated_state["stage"] = "confirm"
        return "Please confirm: " + updated_state["department"] + " service for \"" + updated_state["details"] + "\" on " + slot + ". Is that correct?", updated_state

    if stage == "confirm":
        if is_no(text):
            updated_state["stage"] = "choose_slot"
            updated_state["slot"] = ""
            return "No problem. Would you like to choose a different appointment time? " + slot_options(updated_state["department"]), updated_state

        if is_yes(text):
            updated_state["stage"] = "done"
            return "Your appointment has been confirmed. A technician will review your notes before you arrive.", updated_state

        return "Please answer yes or no so I know whether to confirm the appointment.", updated_state

    return "Your appointment is already confirmed. Type start over if you need to schedule a different appointment.", updated_state
