from classifier import DEFAULT_THRESHOLD, FALLBACK, IntentClassifier


MATCH_TESTS = [
    ("my battery keeps dying every morning", "electrical_issue"),
    ("the radio stopped working and will not play music", "electrical_issue"),
    ("my headlights are flickering at night", "electrical_issue"),
    ("my alarm keeps going off when I open the door", "electrical_issue"),
    ("my car wont move when I press the gas", "drivability_issue"),
    ("the engine is overheating in traffic", "drivability_issue"),
    ("my brakes are grinding when I stop", "drivability_issue"),
    ("the transmission is slipping when I drive", "drivability_issue"),
    ("my ac only blows hot air", "interior_issue"),
    ("the seat is torn and the trim is loose", "interior_issue"),
    ("my windshield is cracked", "exterior_issue"),
    ("the bumper is damaged and hanging loose", "exterior_issue"),
    ("I need an oil change and tire rotation", "maintenance_request"),
    ("my fluids need to be checked before my trip", "maintenance_request"),
    ("I need air in my tires and new wiper blades", "maintenance_request"),
]

REJECT_TESTS = [
    "what time does the library close",
    "how much does parking cost downtown",
    "can you help me with my homework",
    "where is the nearest coffee shop",
    "what is the weather tomorrow",
]


def check(message, expected, actual):
    if expected != actual:
        print("FAILED")
        print("Message:", message)
        print("Expected:", expected)
        print("Actual:", actual)
        return False

    return True


def run_tests():
    passed = 0
    total = 0

    score_checker = IntentClassifier(threshold=0.0)
    classifier = IntentClassifier()

    match_scores = []
    reject_scores = []

    print("Threshold evidence")
    print("Current threshold:", DEFAULT_THRESHOLD)
    print()

    print("Messages that should match")
    for message, expected_intent in MATCH_TESTS:
        intent, score = score_checker.classify(message)
        match_scores.append(score)
        print(f"{message} -> {intent}, confidence {score:.2f}")

        actual_intent, actual_score = classifier.classify(message)
        total += 1
        if check(message, expected_intent, actual_intent):
            passed += 1

    print()
    print("Messages that should reject")
    for message in REJECT_TESTS:
        intent, score = score_checker.classify(message)
        reject_scores.append(score)
        print(f"{message} -> {intent}, confidence {score:.2f}")

        reply, actual_intent, actual_score = classifier.respond(message)
        total += 1
        if check(message, None, actual_intent) and check(message, FALLBACK, reply):
            passed += 1

    print()
    print(f"Lowest match score: {min(match_scores):.2f}")
    print(f"Highest reject score: {max(reject_scores):.2f}")
    print(f"{passed} out of {total} tests passed.")


if __name__ == "__main__":
    run_tests()