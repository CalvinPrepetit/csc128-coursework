"""
CSC-128 Assignment 6: Auto Shop Service Bot
Calvin A. Prepetit

- This file contains the Streamlit interface and grounded model call.
- Retrieval happens before the model is contacted.
- Empty retrieval returns a refusal directly from code.
"""

import streamlit as st
from groq import APIConnectionError, APIError, AuthenticationError, Groq, NotFoundError, RateLimitError

from retriever import DEFAULT_THRESHOLD, Retriever


MODEL = "openai/gpt-oss-20b"
BOT_NAME = "Auto Shop Service Bot"
REFUSAL = (
    "I do not have that information in the auto shop policy guide. "
    "Please contact the shop directly."
)

GROUNDED_PROMPT = """
You are the Auto Shop Service Bot for a fictional auto service shop.

Answer the customer's question using ONLY the reference text between
BEGIN APPROVED REFERENCE TEXT and END APPROVED REFERENCE TEXT.

Rules:
1. Do not use outside knowledge, even if you believe it is correct.
2. Do not add details that are not stated in the reference text.
3. Do not guess prices, hours, dates, numbers, warranty decisions, repair results, or safety facts.
4. If the reference text does not contain the answer, reply with exactly:
"I do not have that information in the auto shop policy guide. Please contact the shop directly."
5. Keep the answer practical, direct, and under 4 sentences.
6. Do not create citations. The application displays the retrieved sources separately.

BEGIN APPROVED REFERENCE TEXT
{context}
END APPROVED REFERENCE TEXT
"""

GREETING = (
    f"Welcome to the {BOT_NAME}. "
    "I can answer questions using the shop's approved visit and service policies."
)

RETRIEVER = Retriever()


def get_client():
    """Create the Groq client using the API key in Streamlit secrets."""
    return Groq(api_key=st.secrets["GROQ_API_KEY"])


def answer_question(question, client=None):
    """Return a grounded answer and sources, or refuse before calling the model."""
    hits = RETRIEVER.search(question)
    if not hits:
        return REFUSAL, []

    context = RETRIEVER.build_context(hits)
    active_client = client or get_client()
    response = active_client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": GROUNDED_PROMPT.format(context=context)},
            {"role": "user", "content": question},
        ],
        temperature=0.0,
    )

    reply = response.choices[0].message.content.strip()
    sources = []
    for document, _score in hits:
        label = f"{document['source']} ({document['id']})"
        if label not in sources:
            sources.append(label)
    return reply, sources


def error_message(error):
    """Return a useful message when the language model cannot be reached."""
    if isinstance(error, RateLimitError):
        return "The language model reached its rate limit. Please wait a minute and try again."
    if isinstance(error, NotFoundError):
        return "The selected language model is not available right now. Please check the model name."
    if isinstance(error, (APIConnectionError, APIError, AuthenticationError, KeyError)):
        return "I could not reach the language model. Please check the API key and try again."
    return "Something went wrong while creating the grounded response. Please try again."


def reset_conversation():
    """Start the visible history with the bot greeting."""
    st.session_state.messages = [
        {"role": "assistant", "content": GREETING, "sources": []}
    ]


def show_sources(sources):
    """Display deterministic source attribution under an answer."""
    if sources:
        st.caption("Sources: " + "; ".join(sources))


def show_sidebar():
    """Show the grounded-bot settings and reset control."""
    st.sidebar.header("Bot Settings")
    st.sidebar.write("Model:", MODEL)
    st.sidebar.write("Retrieval threshold:", f"{DEFAULT_THRESHOLD:.2f}")
    st.sidebar.caption("The model receives only retrieved policy chunks, not general shop information.")
    if st.sidebar.button("Start Over"):
        reset_conversation()
        st.rerun()


def main():
    """Render the Streamlit chat interface."""
    st.set_page_config(page_title=BOT_NAME)
    st.title(BOT_NAME)
    st.caption("You are chatting with automated software using a fictional shop policy guide.")

    if "messages" not in st.session_state:
        reset_conversation()

    show_sidebar()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            show_sources(message.get("sources", []))

    question = st.chat_input("Ask about shop visits or service policies...")
    if question:
        st.session_state.messages.append({"role": "user", "content": question, "sources": []})
        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            placeholder.write("Working on it...")
            try:
                reply, sources = answer_question(question)
            except Exception as error:
                reply = error_message(error)
                sources = []
            placeholder.write(reply)
            show_sources(sources)

        st.session_state.messages.append(
            {"role": "assistant", "content": reply, "sources": sources}
        )


if __name__ == "__main__":
    main()
