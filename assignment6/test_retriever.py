"""Retrieval and refusal tests for CSC-128 Assignment 6."""

from retriever import DEFAULT_THRESHOLD, Retriever


MATCH_TESTS = [
    ("what time are you open on saturday", "shop_hours"),
    ("are you closed on sundays", "shop_hours"),
    ("do I need an appointment or can I walk in", "appointments"),
    ("what happens if I am more than 15 minutes late", "late_arrival"),
    ("what should I bring when I drop off my car", "check_in"),
    ("can I leave my keys there after the shop closes", "after_hours"),
    ("will you start extra repairs without asking me", "diagnostic_authorization"),
    ("will someone call me before the repair estimate changes", "estimates"),
    ("can I bring my own replacement parts", "customer_parts"),
    ("what do I need when I pick up my car", "payment_pickup"),
    ("should I remove valuables before service", "belongings"),
    ("my brakes barely work should I drive it there", "unsafe_vehicle"),
    ("what paperwork should I bring for a warranty review", "warranty_review"),
]

REJECT_TESTS = [
    "can you file an insurance claim for my accident",
    "does my manufacturer have an open recall",
    "how much is a new transmission for my car",
    "what tire pressure should I use for a 2022 sedan",
    "can you tell me how to replace my brake pads at home",
    "will you buy my used car from me",
]


def top_result(retriever, question):
    hits = retriever.search(question, top_k=1)
    if not hits or hits[0][1] <= 0.0:
        return None, 0.0
    document, score = hits[0]
    return document["id"], score


def run_tests():
    passed = 0
    total = 0
    score_retriever = Retriever(threshold=0.0)
    retriever = Retriever()
    match_scores = []
    reject_scores = []

    print("Threshold evidence")
    print("Current threshold:", DEFAULT_THRESHOLD)
    print()

    print("Questions that should retrieve")
    for question, expected_id in MATCH_TESTS:
        evidence_id, evidence_score = top_result(score_retriever, question)
        match_scores.append(evidence_score)
        print(f"{question} -> {evidence_id}, score {evidence_score:.3f}")

        hits = retriever.search(question)
        actual_id = hits[0][0]["id"] if hits else None
        total += 1
        if actual_id == expected_id:
            passed += 1
        else:
            print("FAILED")
            print("Expected:", expected_id)
            print("Actual:", actual_id)

    print()
    print("Questions that should be refused")
    for question in REJECT_TESTS:
        evidence_id, evidence_score = top_result(score_retriever, question)
        reject_scores.append(evidence_score)
        print(f"{question} -> {evidence_id}, score {evidence_score:.3f}")

        hits = retriever.search(question)
        total += 1
        if hits == []:
            passed += 1
        else:
            print("FAILED")
            print("Expected: no retrieved chunks")
            print("Actual:", [document["id"] for document, _score in hits])

    print()
    print(f"Lowest match score: {min(match_scores):.3f}")
    print(f"Highest reject score: {max(reject_scores):.3f}")
    print(f"{passed} out of {total} tests passed.")

    sample_hits = retriever.search(MATCH_TESTS[0][0])
    context = retriever.build_context(sample_hits)
    assert sample_hits, "A matching question should produce context."
    assert sample_hits[0][0]["source"] in context, "Context should include the source label."
    assert "[REFERENCE 1]" in context, "Context should clearly delimit retrieved text."

    if passed != total:
        raise AssertionError(f"{total - passed} retrieval tests failed.")


if __name__ == "__main__":
    run_tests()
