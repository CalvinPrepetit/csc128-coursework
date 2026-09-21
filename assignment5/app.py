"""
CSC-128 Assignment 5: Auto Shop Service Advisor Bot
Calvin A. Prepetit

- This file contains the Streamlit interface for the auto shop advisor bot.
- It sends the system prompt, recent chat history, and streamed replies to Groq.
- It handles API failures without showing a traceback to the user.
"""
import streamlit as st
from groq import APIConnectionError, APIError, AuthenticationError, Groq, NotFoundError, RateLimitError

MODEL = "openai/gpt-oss-20b"
MAX_HISTORY = 10

SYSTEM_PROMPT = """
You are the Auto Shop Service Advisor Bot for a small auto service shop.

Your job is to help customers with auto service questions only. You can:
1. Help customers describe vehicle problems clearly.
2. Explain likely service areas: electrical, drivability, interior, exterior, and maintenance.
3. Suggest what information the customer should bring before a service appointment.
4. Help the customer prepare a short service note for a technician.

You must not:
1. Claim to diagnose the vehicle with certainty.
2. Give final repair instructions that replace a licensed mechanic.
3. Quote exact prices, warranty decisions, or shop availability.
4. Answer questions outside auto service support.
5. Invent policies, appointments, recalls, or facts you do not have.
6. Invent vehicle make, model, year, measurements, service history, causes, or events the customer did not mention.

Use only details the customer actually provided. If an important detail is missing, ask for it or say "if applicable" instead of making it up.
When writing a note for a technician, only include facts the customer gave you. For unknown details, use short placeholders such as [make/model/year], [when it started], or [what you tried]. Do not write sample first-person statements that claim the customer checked, tested, replaced, cleaned, or measured anything unless the customer already said so.
Do not broaden a symptom beyond what the customer said. For example, if the customer says "my lights keep dimming," do not change it to "all interior and exterior lights dim" or add when it happens unless the customer gave those details.

When a user asks for something outside the bot's scope, say that you can only help with auto service questions, then name what you can help with instead.

Keep answers practical and concise. Use short paragraphs or a short bullet list. Ask clarifying questions instead of filling in missing details. Remind the customer to contact the shop or a qualified technician for safety critical issues, pricing, warranty, or appointment availability.
"""

GREETING = (
    "Welcome to the Auto Shop Service Advisor Bot. "
    "I can help with electrical, drivability, interior, exterior, and maintenance questions. "
    "Please describe what is going on with your vehicle."
)


def get_client():
    """Creates the Groq client using the API key stored in Streamlit secrets."""
    return Groq(api_key=st.secrets["GROQ_API_KEY"])


def reset_conversation():
    """Starts the visible chat history with the bot greeting."""
    st.session_state.messages = [{"role": "assistant", "content": GREETING}]


def api_messages(history):
    """Builds the system prompt plus the most recent chat messages."""
    recent_messages = history[-MAX_HISTORY:]
    return [{"role": "system", "content": SYSTEM_PROMPT}] + recent_messages


def stream_reply(client, history, placeholder):
    """Streams the model response into a placeholder and returns the full reply."""
    stream = client.chat.completions.create(
        model=MODEL,
        messages=api_messages(history),
        stream=True,
        temperature=0.2,
    )

    full_reply = ""
    for chunk in stream:
        piece = chunk.choices[0].delta.content
        if piece:
            full_reply += piece
            placeholder.write(full_reply)

    return full_reply


def error_message(error):
    """Returns a message the user can act on when the API call fails."""
    if isinstance(error, RateLimitError):
        return (
            "I hit the rate limit for the language model. "
            "Please wait a minute and try again with a shorter message."
        )

    if isinstance(error, NotFoundError):
        return (
            "The selected language model is not available right now. "
            "Please check the model name in the app and try again."
        )

    if isinstance(error, (APIConnectionError, APIError, AuthenticationError, KeyError)):
        return (
            "I could not reach the language model right now. "
            "Please check the API key and try again. If this keeps happening, contact the shop directly."
        )

    return (
        "Something went wrong while contacting the language model. "
        "Please try again or contact the shop directly."
    )


def show_sidebar():
    """Shows the model settings, history cap, and reset button."""
    st.sidebar.header("Bot Settings")
    st.sidebar.write("Model:", MODEL)
    st.sidebar.write("History window:", str(MAX_HISTORY) + " messages")
    st.sidebar.caption("The system prompt is always sent with the recent conversation window.")

    if st.sidebar.button("Start Over"):
        reset_conversation()
        st.rerun()


def main():
    """Renders the chat app and saves each turn in session state."""
    st.set_page_config(page_title="Auto Shop Service Advisor Bot")
    st.title("Auto Shop Service Advisor Bot")
    st.caption("You are chatting with an automated assistant, not a person.")

    if "messages" not in st.session_state:
        reset_conversation()

    show_sidebar()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_text = st.chat_input("Describe your vehicle issue...")
    if user_text:
        st.session_state.messages.append({"role": "user", "content": user_text})

        with st.chat_message("user"):
            st.write(user_text)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            placeholder.write("Working on it...")
            try:
                reply = stream_reply(get_client(), st.session_state.messages, placeholder)
            except Exception as error:
                reply = error_message(error)
                st.write(reply)

        st.session_state.messages.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    main()
