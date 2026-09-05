"""
CSC-128 Assignment 3 starter: Intent classifier
Calvin A. Prepetit
"""
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# TODO 1: build a stop word list. Do not include "not" or "no".
STOP_WORDS = {
    "i", "me", "my", "a", "an", "the", "is", "are", "am", "was", "were",
    "to", "for", "with", "of", "on", "in", "at", "and", "or", "but",
    "can", "could", "would", "you", "please", "it", "this", "that",
    "just", "really", "very"
}

# TODO 2: five intents, at least six example phrasings each
TRAINING = {
    "electrical_issue": [
        "my lights keep dimming when the music gets loud and im not sure why",
        "the radio stopped working the other day, it flashes every now and then but wont play music",
        "my headlights are flickering and I don't know what to do. Driving at night is scary",
        "my battery keeps dying and I have to jump start the car",
        "the car wont start but the radio turns on and then turns right back off",
        "my alarm keeps going off whenever I put the key in and it's maddening",
        "my speedometer and dash meter are not working right",
        "I think I am having an electrical issue",
    ],
    "drivability_issue": [
        "my car isnt running and it stopped on me while I was driving",
        "the transmission feels like it is slipping when I try to accelerate",
        "my car keeps stalling while driving and I dont know why",
        "my brakes are grinding and the car does not feel safe to drive",
        "the car wont move no matter what I do",
        "the engine overheats every time I'm in traffic, which is about the right temperature for my life",
        "steam started coming from under the hood and then the car stopped",
        "I think this is a drivability issue",
        "I am having a driving issue",
        "the car is not driving anywhere",
    ],
    "interior_issue": [
        "my seat is torn and I need someone to look at the inside of the car",
        "the dashboard is cracked and part of the trim is loose",
        "my ac is not getting cold and it only blows hot air from outside",
        "the heater is not working and the inside of the car stays cold",
        "the carpet is damaged from water getting inside the vehicle when I left a hose in the sunroof",
        "one of the interior door handles is loose and feels like it might break",
        "I think I am having an interior issue",
    ],
    "exterior_issue": [
        "my windshield is cracked and I need it checked before it gets worse",
        "the side mirror is broken and hanging off the car",
        "there is a dent in the door from someone hitting it in a parking lot",
        "the bumper is damaged and hanging loose like it has somewhere else to be",
        "the paint is scratched across the side of the vehicle",
        "one of the body panels is bent and does not line up right",
        "I think I am having an exterior issue",
    ],
    "maintenance_request": [
        "I need an oil change and maybe a tire rotation",
        "my fluids need to be checked before I leave for my trip",
        "I need air put in my tires and the tire pressure checked",
        "I need a vehicle inspection before I keep driving it",
        "I need my wiper blades changed as mine are leaving streaks",
        "I need a coolant flush and a general maintenance check",
        "I think I need maintenance service",
    ],
}

RESPONSES = {
    "electrical_issue": "It sounds like you are having an electrical issue. A ticket has been opened, and a technician will be with you shortly.",
    "drivability_issue": "It sounds like you are having a drivability issue. A ticket has been opened, and a technician will be with you shortly.",
    "interior_issue": "It sounds like you are having an interior issue. A ticket has been opened, and a technician will be with you shortly.",
    "exterior_issue": "It sounds like you are having an exterior issue. A ticket has been opened, and a technician will be with you shortly.",
    "maintenance_request": "It sounds like you are making a maintenance request. A ticket has been opened, and a technician will be with you shortly.",
}

FALLBACK = "I can help with electrical, drivability, interior, exterior, and maintenance issues. What problem are you having with the vehicle?"

# TODO 6: set this using the evidence your tests print out
DEFAULT_THRESHOLD = 0.42


def stem(word):
    if word.endswith("ing") and len(word) > 5:
        return word[:-3]
    if word.endswith("ed") and len(word) > 4:
        return word[:-2]
    if word.endswith("s") and len(word) > 3:
        return word[:-1]
    return word


def normalize(text):
    """TODO 3: lowercase, remove punctuation, drop stop words, and stem words."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    tokens = text.split()
    return " ".join(stem(token) for token in tokens if token not in STOP_WORDS)


class IntentClassifier:
    def __init__(self, training=None, threshold=DEFAULT_THRESHOLD):
        # TODO 4: flatten TRAINING into parallel phrases and labels lists,
        # then fit a TfidfVectorizer on the normalized phrases.
        self.training = training or TRAINING
        self.threshold = threshold
        self.phrases = []
        self.labels = []

        for intent, examples in self.training.items():
            for example in examples:
                self.phrases.append(normalize(example))
                self.labels.append(intent)

        self.vectorizer = TfidfVectorizer()
        self.training_vectors = self.vectorizer.fit_transform(self.phrases)

    def classify(self, text):
        """
        TODO 5: return (intent, confidence).

        Transform the text, take cosine similarity against every training
        phrase, find the best score, and return None for the intent when
        that score is below the threshold.
        """
        clean_text = normalize(text)
        text_vector = self.vectorizer.transform([clean_text])
        scores = cosine_similarity(text_vector, self.training_vectors)[0]

        best_index = scores.argmax()
        best_score = float(scores[best_index])
        best_intent = self.labels[best_index]

        if best_score < self.threshold:
            return None, best_score

        return best_intent, best_score

    def respond(self, text):
        """Return (reply, intent, confidence)."""
        intent, confidence = self.classify(text)
        if intent is None:
            return FALLBACK, None, confidence
        return RESPONSES[intent], intent, confidence
