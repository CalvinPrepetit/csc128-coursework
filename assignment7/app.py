"""CSC-128 Assignment 7: Auto Shop Service Advisor interface.
Calvin A. Prepetit
"""

import streamlit as st
from groq import APIConnectionError, APIError, AuthenticationError, Groq, NotFoundError, RateLimitError

from agent import MODEL, new_session, process_turn


def get_client():
    """The model interprets language; Python validates and commits confirmed writes."""
    return Groq(api_key=st.secrets["GROQ_API_KEY"])


def friendly_error(error):
    if isinstance(error, RateLimitError):
        return "The model reached its rate limit. Please wait and retry. No unconfirmed request was saved."
    if isinstance(error, AuthenticationError):
        return "The model rejected the API key. Check your local secrets file."
    if isinstance(error, NotFoundError):
        return "The selected model is unavailable. Check MODEL in agent.py."
    if isinstance(error, APIConnectionError):
        return "The model connection failed. Please try again later."
    if isinstance(error, (KeyError, FileNotFoundError)):
        return "Add GROQ_API_KEY to .streamlit/secrets.toml to use the bot."
    if isinstance(error, APIError):
        return "The model rejected this request. Please try Start Over."
    return "I could not complete that turn. No unconfirmed request was saved. Please try again."


def main():
    st.set_page_config(page_title="Auto Shop Service Advisor")
    st.title("Auto Shop Service Advisor")
    st.caption("You are chatting with automated software for a fictional auto shop.")
    if "advisor_session" not in st.session_state:
        st.session_state.advisor_session = new_session()
    session = st.session_state.advisor_session
    st.sidebar.header("Bot Settings")
    st.sidebar.write("Model:", MODEL)
    st.sidebar.caption("Repeating weekday schedule. Requests are stored only in this browser session.")
    if st.sidebar.button("Start Over"):
        records = session["records"]
        session = new_session()
        session["records"] = records
        st.session_state.advisor_session = session
        st.rerun()
    with st.sidebar.expander("Tool log", expanded=True):
        if not session["tool_log"]:
            st.write("No tool calls yet.")
        for number, entry in enumerate(session["tool_log"], 1):
            st.write(f"{number}. {entry['name']}")
            st.code(f"Arguments: {entry['arguments']}\nResult: {entry['result']}")
    with st.sidebar.expander("Saved service requests"):
        if session["records"]:
            st.json(session["records"])
        else:
            st.write("No service requests saved.")
    for message in session["display"]:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    if session["pending_write"]:
        st.info("Review the exact fields above before confirming.")
        yes, no = st.columns(2)
        action = "yes" if yes.button("Confirm service request") else "no" if no.button("Change details") else None
    else:
        action = None
    text = st.chat_input("Ask about hours, openings, or a service request...")
    if action or text:
        text = action or text
        with st.chat_message("user"):
            st.write(text)
        with st.chat_message("assistant"):
            with st.spinner("Working on it..."):
                try:
                    reply = process_turn(text, session, get_client)
                except Exception as error:
                    reply = friendly_error(error)
                    session["display"].append({"role": "assistant", "content": reply})
                    session["messages"].append({"role": "assistant", "content": reply})
            st.write(reply)
        st.rerun()


if __name__ == "__main__":
    main()
