"""
CSC-128 Assignment 2: Stateful appointment bot
Calvin A. Prepetit

Run with:
streamlit run appointment_bot.py
"""
import streamlit as st

from flow import GREETING, handle, new_state


def reset_conversation():
    st.session_state.state = new_state()
    st.session_state.messages = [
        {"role": "assistant", "content": GREETING},
    ]


def show_appointment_summary():
    state = st.session_state.state

    st.sidebar.header("Appointment Summary")
    st.sidebar.write("Service:", state["department"] or "Pending Customer Input")
    st.sidebar.write("Details:", state["details"] or "Pending Customer Input")
    st.sidebar.write("Appointment:", state["slot"] or "Pending Customer Input")
    st.sidebar.caption("Current stage: " + state["stage"])


def main():
    st.title("Auto Shop Appointment Bot")
    st.caption("You are chatting with an automated assistant, not a person.")

    if "state" not in st.session_state:
        st.session_state.state = new_state()

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": GREETING},
        ]

    if st.sidebar.button("Start Over"):
        reset_conversation()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_message = st.chat_input("Please describe what you need help scheduling...")

    if user_message:
        st.session_state.messages.append({"role": "user", "content": user_message})

        with st.chat_message("user"):
            st.write(user_message)

        bot_response, updated_state = handle(user_message, st.session_state.state)
        st.session_state.state = updated_state
        st.session_state.messages.append({"role": "assistant", "content": bot_response})

        with st.chat_message("assistant"):
            st.write(bot_response)

    show_appointment_summary()


if __name__ == "__main__":
    main()
