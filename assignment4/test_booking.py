"""
CSC-128 Assignment 4: Extractor and conversation tests
Calvin A. Prepetit

Run with python test_booking.py.
Use --without-time-fix to demonstrate the documented collision failing.
"""
import re
import sys

import extractors
from booking import handle, new_state
from extractors import find_day, find_vehicle_count, find_department, find_time, strip_vehicle_count

COLLISION_MESSAGE = "Book maintenance for 4 vehicles on Thursday at 3pm"


def check(message, expected, actual):
    if expected != actual:
        print("FAILED")
        print("Message:", message)
        print("Expected:", expected)
        print("Actual:", actual)
        return False
    return True


def replay(messages):
    state = new_state()
    reply = ""
    for message in messages:
        reply, state = handle(message, state)
    return reply, state


def legacy_find_time(text):
    """The learning page's permissive pattern, before requiring an explicit time."""
    pattern = r"\b(\d{1,2})(?::(\d{2}))?\s*(am|pm)?\b"
    match = re.search(pattern, text.lower())
    if not match:
        return None
    return f"{match.group(1)}:{match.group(2) or '00'}{match.group(3) or ''}"


def check_collision():
    # Check the hour, not display formatting: the broken version selects 4, not 3.
    result = extractors.find_time(COLLISION_MESSAGE)
    actual_hour = int(result.split(":")[0]) if result else None
    return check(COLLISION_MESSAGE, 3, actual_hour)


def run_tests():
    passed = 0
    total = 0
    extractor_cases = [
        (find_department, "My headlights and radio stopped working", "Electrical"),
        (find_department, "My car keeps stalling while driving", "Drivability"),
        (find_department, "My AC and heater are not working", "Interior"),
        (find_department, "The mirror and glass are broken", "Exterior"),
        (find_department, "I need my cars oil shanged", "Maintenance"),
        (find_department, "change my appointment to Friday", None),
        (find_department, "painting a room", None),
        (find_day, "THURSDAY please", "Thursday"),
        (find_day, "mondays", None),
        (find_time, "3 pm", "3:00 PM"),
        (find_time, "3:30pm", "3:30 PM"),
        (find_time, "15:00", "3:00 PM"),
        (find_time, "24:00", None),
        (find_vehicle_count, "4 vehicles", 4),
        (find_vehicle_count, "four cars", 4),
        (find_vehicle_count, "-4 vehicles", None),
        (strip_vehicle_count, "4 vehicles at 3pm", "  at 3pm"),
    ]
    for function, message, expected in extractor_cases:
        total += 1
        passed += check(function.__name__ + ": " + message, expected, function(message))

    full = "Book maintenance for Thursday at 3pm for two vehicles"
    conversations = [
        ("both cars supplied with a schedule correction",
         ["oil changed and starter replaced Friday at 4pm",
          "actually mine and my wife car need work Tuesday at 3pm instead so both cars can be serviced"],
         {"stage": "confirm", "department": "Electrical and Maintenance", "day": "Tuesday", "time": "3:00 PM", "vehicle_count": 2},
         ["Updated", "Electrical and Maintenance service", "Tuesday", "3:00 PM", "2 vehicles", "Please confirm"]),
        ("multiple services in one request", ["oil change and bumper on Friday at 9am"],
         {"stage": "confirm", "department": "Exterior and Maintenance"},
         ["Exterior and Maintenance service", "Friday", "9:00 AM"]),
        ("add bumper at confirmation", [full, "wait actually could you look at my bumper too"],
         {"stage": "confirm", "department": "Maintenance and Exterior"},
         ["Updated Service: Maintenance and Exterior", "Please confirm"]),
        ("add while collecting without duplicates", ["maintenance", "also maintenance and bumper"],
         {"stage": "collect", "department": "Maintenance and Exterior"},
         ["Updated Service: Maintenance and Exterior", "What day"]),
        ("replace multiple services", [full, "add bumper", "electrical instead"],
         {"stage": "confirm", "department": "Electrical"}, ["Updated Service: Electrical"]),
        ("add after booking and reconfirm all services", [full, "yes", "also check my bumper", "yes"],
         {"stage": "done", "department": "Maintenance and Exterior"},
         ["confirmed", "Maintenance and Exterior service", "Thursday", "3:00 PM", "2 vehicles"]),
        ("availability question changes preferred schedule", [full, "well do you have Saturday at 8am availible"],
         {"stage": "confirm", "day": "Saturday", "time": "8:00 AM"},
         ["can't check shop availability", "Updated Day: Saturday", "Time: 8:00 AM", "Please confirm"]),
        ("new schedule without correction phrase", [full, "Saturday at 8am"],
         {"stage": "confirm", "day": "Saturday", "time": "8:00 AM"},
         ["Updated Day: Saturday", "Please confirm"]),
        ("all four slots in one message", [full],
         {"stage": "confirm", "department": "Maintenance", "day": "Thursday", "time": "3:00 PM", "vehicle_count": 2},
         ["Maintenance service", "Thursday", "3:00 PM", "2 vehicles", "Please confirm"]),
        ("optional quantity volunteered early", ["just my car", "Friday at 15:00", "interior"],
         {"stage": "confirm", "department": "Interior", "day": "Friday", "time": "3:00 PM", "vehicle_count": 1},
         ["Interior service", "1 vehicle"]),
        ("correct vehicle count", [full, "change that to three vehicles"],
         {"stage": "confirm", "vehicle_count": 3}, ["Updated Vehicles: 3"]),
        ("declining keeps details editable", [full, "no"],
         {"stage": "change", "department": "Maintenance", "day": "Thursday"}, ["What would you like to change"]),
        ("decline edit and confirm", [full, "no", "Friday", "yes thats correct"],
         {"stage": "done", "day": "Friday"}, ["Your appointment has been confirmed", "Maintenance service", "Friday", "3:00 PM", "2 vehicles"]),
        ("remove optional vehicle count", [full, "actually remove vehicle count"],
         {"stage": "confirm", "vehicle_count": None, "department": "Maintenance"},
         ["Updated Vehicles: not specified", "Please confirm"]),
        ("relative correction cannot keep the old day", [full, "actually next Tuesday at 4pm"],
         {"stage": "collect", "day": None, "time": "4:00 PM"}, ["specific weekday"]),
        ("clarified weekday completes appointment", ["maintenance tomorrow at 3pm", "Tuesday", "yes"],
         {"stage": "done", "department": "Maintenance", "day": "Tuesday", "time": "3:00 PM"},
         ["Your appointment has been confirmed"]),
    ]
    for name, messages, expected, reply_parts in conversations:
        reply, actual = replay(messages)
        result = {key: actual[key] for key in expected}
        total += 1
        state_ok = check(name + ": " + repr(messages), expected, result)
        reply_ok = check(name + " reply: " + reply, True, all(part in reply for part in reply_parts))
        passed += state_ok and reply_ok

    restart_cases = [([full, "yes"], "start over")]
    for messages, command in restart_cases:
        reply, state = replay(messages + [command])
        total += 1
        passed += check("reset " + repr(messages) + " with " + command, new_state(), state)

    total += 1
    passed += check_collision()
    print(f"{passed} out of {total} tests passed.")
    return passed == total


if __name__ == "__main__":
    if "--without-time-fix" in sys.argv:
        extractors.find_time = legacy_find_time
        print("Using the original time pattern. This regression test should fail.")
        success = check_collision()
    else:
        success = run_tests()
    sys.exit(0 if success else 1)
