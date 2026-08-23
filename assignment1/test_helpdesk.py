from helpdesk_bot import FALLBACK, get_response, match_rule, normalize


def check(message, expected, actual):
    if expected != actual:
        print("FAILED")
        print("Message:", message)
        print("Expected:", expected)
        print("Actual:", actual)
        return False

    return True


def check_contains(message, expected_text, actual):
    if expected_text not in actual:
        print("FAILED")
        print("Message:", message)
        print("Expected text:", expected_text)
        print("Actual:", actual)
        return False

    return True


def run_tests():
    passed = 0
    total = 0

    tests = [
        ("normalize lowercase", "  I Need BATTERY  ", "i need battery", normalize("  I Need BATTERY  ")),
        ("electrical topic", "My battery light is on", "electrical", match_rule("My battery light is on")["topic"]),
        ("electrical topic 2", "The radio speaker stopped working", "electrical", match_rule("The radio speaker stopped working")["topic"]),
        ("drivability topic", "My check engine light came on", "drivability", match_rule("My check engine light came on")["topic"]),
        ("drivability topic 2", "The transmission is slipping when I drive", "drivability", match_rule("The transmission is slipping when I drive")["topic"]),
        ("interior topic", "My seat is torn", "interior", match_rule("My seat is torn")["topic"]),
        ("interior topic 2", "The dashboard button broke", "interior", match_rule("The dashboard button broke")["topic"]),
        ("interior topic 3", "My ac is not working", "interior", match_rule("My ac is not working")["topic"]),
        ("exterior topic", "My windshield has a crack", "exterior", match_rule("My windshield has a crack")["topic"]),
        ("exterior topic 2", "There is a dent in my bumper", "exterior", match_rule("There is a dent in my bumper")["topic"]),
        ("maintenance topic", "I need an oil change", "maintenance", match_rule("I need an oil change")["topic"]),
        ("maintenance topic 2", "Can you inspect my brakes and tires", "maintenance", match_rule("Can you inspect my brakes and tires")["topic"]),
        ("best match chooses drivability", "My battery light is on, but the engine is shaking and the transmission slips", "drivability", match_rule("My battery light is on, but the engine is shaking and the transmission slips")["topic"]),
        ("fallback no topic 1", "What time do you close?", FALLBACK, get_response("What time do you close?")),
        ("fallback no topic 2", "How much is a car wash?", FALLBACK, get_response("How much is a car wash?")),
        ("fallback no topic 3", "Can I schedule an appointment?", FALLBACK, get_response("Can I schedule an appointment?")),
    ]

    for message, user_text, expected, actual in tests:
        total += 1
        if check(user_text, expected, actual):
            passed += 1

    response_tests = [
        ("single response", "My battery is dead", "electrical issue"),
        ("tie response", "My battery light is on and the engine is shaking", "electrical and drivability issues"),
        ("three topic tie response", "My battery, engine, and seat all need work", "electrical, drivability, and interior issues"),
    ]

    for name, user_text, expected_text in response_tests:
        total += 1
        if check_contains(user_text, expected_text, get_response(user_text)):
            passed += 1

    print(f"{passed} out of {total} tests passed.")


if __name__ == "__main__":
    run_tests()
