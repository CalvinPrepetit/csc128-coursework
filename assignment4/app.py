"""
CSC-128 Assignment 4: Auto Shop Appointment Bot (Slot Filling Adaptation)
Calvin A. Prepetit

Run with:
streamlit run app.py
"""
import streamlit as st

from booking import GREETING, handle, new_state


def reset_conversation():
    st.session_state.state = new_state()
    st.session_state.messages = [{"role": "assistant", "content": GREETING}]


def show_appointment_summary():
    state = st.session_state.state
    st.sidebar.header("Appointment Summary")
    st.sidebar.write("Service:", state["department"] or "Pending Customer Input")
    st.sidebar.write("Day:", state["day"] or "Pending Customer Input")
    st.sidebar.write("Time:", state["time"] or "Pending Customer Input")
    st.sidebar.write("Vehicles:", state["vehicle_count"] or "Not specified (optional)")
    status = {"collect": "Collecting details", "confirm": "Awaiting confirmation",
              "change": "Awaiting changes", "done": "Confirmed"}
    st.sidebar.caption("Status: " + status[state["stage"]])


def main():
    st.set_page_config(page_title="Auto Shop Appointment Bot (Slot Filling Adaptation)")
    st.title("Auto Shop Appointment Bot (Slot Filling Adaptation)")
    st.caption("You are chatting with an automated assistant, not a person.")
    st.caption("Appointments are stored only in this session.")

    if "state" not in st.session_state:
        reset_conversation()

    if st.sidebar.button("Start Over"):
        reset_conversation()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_text = st.chat_input("Enter your appointment details...")
    if user_text:
        reply, updated_state = handle(user_text, st.session_state.state)
        st.session_state.state = updated_state
        st.session_state.messages.append({"role": "user", "content": user_text})
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()

    show_appointment_summary()


if __name__ == "__main__":
    main()
