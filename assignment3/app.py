"""
CSC-128 Assignment 3: Auto Shop Service Bot
Calvin A. Prepetit

This version uses an intent classifier instead of keyword matching.

Run with:
streamlit run app.py
"""
import streamlit as st

from classifier import IntentClassifier

GREETING = "Welcome to the Auto service desk. Is your issue related to electrical, drivability, interior, exterior, or maintenance? Please describe your problem in detail."


@st.cache_resource
def get_classifier():
    return IntentClassifier()


def main():
    st.set_page_config(page_title="Auto Shop Service Bot")

    st.title("Auto Shop Service Bot")
    st.caption("You are chatting with an automated assistant, not a person.")

    classifier = get_classifier()

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": GREETING},
        ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            if message["role"] == "assistant" and "confidence" in message:
                st.caption(
                    f"Intent: {message.get('intent') or 'None (fallback)'} | "
                    f"Confidence: {message.get('confidence', 0.0):.2f}"
                )

    user_text = st.chat_input("Describe your vehicle issue...")

    if user_text:
        st.session_state.messages.append({"role": "user", "content": user_text})

        reply, intent, confidence = classifier.respond(user_text)

        st.session_state.messages.append({
            "role": "assistant",
            "content": reply,
            "intent": intent,
            "confidence": confidence,
        })
        st.rerun()


if __name__ == "__main__":
    main()
