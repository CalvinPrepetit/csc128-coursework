"""
CSC-128 Assignment 1 starter: Rule-based help desk bot
Calvin A. Prepetit

Run:  streamlit run helpdesk_bot.py
"""
import streamlit as st

# TODO 1: add at least five topics. Each one needs a topic name, a list of
# keywords, and the response text. Two are done for you as a pattern.
RULES = [
    {
        "topic": "electrical",
        "keywords": ["battery", "radio", "speaker", "light", "gauge", "window", "power", "electrical", "fuse", "wiring", "alternator", "starter", "ignition", "start", "turn on"],
        "response": "It sounds like you are having an electrical issue. A ticket has been opened, and a technician will be with you shortly.",
    },
    {
        "topic": "drivability",
        "keywords": ["engine", "transmission", "check engine", "noise", "stall", "shaking", "drive", "acceleration", "tire", "brake", "drivability", "driving", "clutch", "gear", "ignition", "fuel", "exhaust", "move", "vibrate", "go"],
        "response": "It sounds like you are having a drivability issue. A ticket has been opened, and a technician will be with you shortly.",
    },
    {
        "topic": "interior",
        "keywords": ["seat", "carpet", "headliner", "dashboard", "dial", "button", "interior", "trim", "console", "vent", "airbag", "heater", "ac", "air conditioning", "climate", "stereo", "radio", "speaker", "inside"],
        "response": "It sounds like you are having an interior issue. A ticket has been opened, and a technician will be with you shortly.",
    },
    {
        "topic": "exterior",
        "keywords": ["body", "windshield", "window", "paint", "dent", "scratch", "bumper", "exterior", "hood", "door", "grill", "roof", "fender", "crash", "collision", "mirror", "headlight", "taillight", "outside"],
        "response": "It sounds like you are having an exterior issue. A ticket has been opened, and a technician will be with you shortly.",
    },
    {
        "topic": "maintenance",
        "keywords": ["oil", "fluid", "brakes", "tires", "inspect", "maintenance", "flush", "filter", "tune-up", "alignment", "rotation", "lubrication", "service", "check"],
        "response": "It sounds like you are having a maintenance issue. A ticket has been opened, and a technician will be with you shortly.",
    },
]

# TODO 2: write a fallback that names what the bot can actually do
FALLBACK = "I can help with electrical, drivability, interior, exterior, and maintenance issues. What problem are you having with the vehicle?"

GREETING = "Welcome to the Auto service desk. Is your issue related to electrical, drivability, interior, exterior, or maintenance? Please describe your problem in detail."


def normalize(text):
    """TODO 3: lowercase the text and collapse extra whitespace."""
    for punctuation in ",.?!;:":
        text = text.replace(punctuation, " ")
    return " ".join(text.lower().split())
 

def match_rules(text):
    """
    TODO 4: return the rule whose keywords appear most often in the message.

    Do not stop at the first match. Count how many keywords each rule hits
    and return the best one. Return None if nothing matches.
    """
    normalized_text = normalize(text)
    padded_text = " " + normalized_text + " "
    best_rules = []
    best_score = 0

    for rule in RULES:
        score = 0

        for keyword in rule["keywords"]:
            normalized_keyword = normalize(keyword)
            if " " in normalized_keyword:
                score += normalized_text.count(normalized_keyword)
            else:
                score += padded_text.count(" " + normalized_keyword + " ")

        if score > best_score:
            best_rules = [rule]
            best_score = score
        elif score == best_score and score > 0:
            best_rules.append(rule)

    return best_rules


def match_rule(text):
    rules = match_rules(text)
    return rules[0] if rules else None


def get_response(text):
    """TODO 5: use match_rule, and return FALLBACK when it returns None."""
    rules = match_rules(text)

    if not rules:
        return FALLBACK

    if len(rules) == 1:
        return rules[0]["response"]

    topics = [rule["topic"] for rule in rules]

    if len(topics) == 2:
        topic_text = " and ".join(topics)
    else:
        topic_text = ", ".join(topics[:-1]) + ", and " + topics[-1]

    return f"It sounds like you are having {topic_text} issues. A ticket has been opened, and a technician will be with you shortly."


def main():
    st.title("Auto Service Desk Bot")
    st.caption("You are chatting with an automated assistant, not a person.")

    # TODO 6: store the message history in st.session_state, remembering the
    # first-run guard, then redraw it, then handle new input.
    if "messages" not in st.session_state:
     st.session_state.messages = [
        {"role": "assistant", "content": GREETING},
    ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
         st.write(message["content"])

    user_message = st.chat_input("Please describe the issue you are having with your vehicle...")

    if user_message:
        st.session_state.messages.append({"role": "user", "content": user_message})

        with st.chat_message("user"):
            st.write(user_message)

        bot_response = get_response(user_message)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})

        with st.chat_message("assistant"):
            st.write(bot_response)

if __name__ == "__main__":
    main()
