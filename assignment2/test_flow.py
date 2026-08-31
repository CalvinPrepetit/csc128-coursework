from flow import handle, new_state


def check(message, expected, actual):
    if expected != actual:
        print("FAILED")
        print("Message:", message)
        print("Expected:", expected)
        print("Actual:", actual)
        return False

    return True


def check_state(message, expected, actual):
    for key, expected_value in expected.items():
        if expected_value != actual[key]:
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


def run_tests():
    passed = 0
    total = 0

    conversations = [
        (
            "successful match on electrical path",
            ["My battery keeps dying", "5pm", "yes thats correct"],
            {
                "stage": "done",
                "department": "Electrical",
                "details": "My battery keeps dying",
                "slot": "Friday 5:00 PM",
            },
        ),
        (
            "wrong input then successful maintenance path",
            ["Monday", "maintenance", "Oil change and tire rotation", "Saturday", "yes"],
            {
                "stage": "done",
                "department": "Maintenance",
                "details": "Oil change and tire rotation",
                "slot": "Saturday 7:00 PM",
            },
        ),
        (
            "successful match on two service areas",
            ["My battery failed and the engine failed", "Wednesday", "yes"],
            {
                "stage": "done",
                "department": "Drivability and Electrical",
                "details": "My battery failed and the engine failed",
                "slot": "Wednesday 1:00 PM",
            },
        ),
        (
            "restart clears old state",
            ["interior", "The seat is torn", "start over", "exterior", "The mirror is broken", "Sunday", "yes"],
            {
                "stage": "done",
                "department": "Exterior",
                "details": "The mirror is broken",
                "slot": "Sunday 5:00 PM",
            },
        ),
        (
            "declined confirmation redirects to slot selection",
            ["drivability", "The engine is shaking", "Monday", "no that is not correct"],
            {
                "stage": "choose_slot",
                "department": "Drivability",
                "details": "The engine is shaking",
                "slot": "",
            },
        ),
    ]

    for name, messages, expected_state in conversations:
        reply, actual_state = replay(messages)
        total += 1
        if check_state(name, expected_state, actual_state):
            passed += 1

    stage_tests = [
        ("Monday before department", ["Monday"], "choose_department"),
        ("Monday as details", ["electrical", "Monday"], "choose_slot"),
        ("Monday as slot", ["electrical", "Battery problem", "Monday"], "confirm"),
        ("Monday at confirmation", ["electrical", "Battery problem", "Monday", "Monday"], "confirm"),
        ("Monday after done", ["electrical", "Battery problem", "Monday", "yes", "Monday"], "done"),
        ("misspelled fluids checked accepts details", ["fluids chekced"], "choose_slot"),
    ]

    for name, messages, expected_stage in stage_tests:
        reply, actual_state = replay(messages)
        total += 1
        if check(name, expected_stage, actual_state["stage"]):
            passed += 1

    department_tests = [
        ("wont start chooses electrical", ["The car just wont start no matter what I do"], "Electrical"),
        ("not going anywhere chooses drivability", ["It is not going anywhere"], "Drivability"),
        ("heater vent chooses interior", ["The heater only blows cold air from the vent"], "Interior"),
        ("cracked glass chooses exterior", ["The glass is cracked and the body panel is damaged"], "Exterior"),
        ("air tires fluids chooses maintenance", ["I need air in my tires and my fluids checked before my trip"], "Maintenance"),
    ]

    for name, messages, expected_department in department_tests:
        reply, actual_state = replay(messages)
        total += 1
        if check(name, expected_department, actual_state["department"]):
            passed += 1

    restart_tests = [
        ("restart from choose_department", []),
        ("restart from describe_issue", ["electrical"]),
        ("restart from choose_slot", ["My battery keeps dying"]),
        ("restart from confirm", ["My battery keeps dying", "Friday"]),
        ("restart from done", ["My battery keeps dying", "Friday", "yes"]),
    ]

    reset_state = {
        "stage": "choose_department",
        "department": "",
        "details": "",
        "slot": "",
    }

    for name, messages in restart_tests:
        reply, actual_state = replay(messages + ["start over"])
        total += 1
        if check_state(name, reset_state, actual_state):
            passed += 1

    print(f"{passed} out of {total} tests passed.")


if __name__ == "__main__":
    run_tests()
