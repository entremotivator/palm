import streamlit as st
from google.generativeai import configure, chat
from google.api_core import retry
import google.generativeai as palm

# Retrieve PaLM API key from environment variables or st.secrets
API_KEY = st.secrets.get("palm_api_key")

# Import and configure google.generativeai
configure(api_key=API_KEY)

@retry.Retry()
def retry_chat(**kwargs):
    return chat(**kwargs)


def display_ui():
    st.header("Chat with PaLM")

    # Chat box and history
    chat_history = []

    defaults = {
        'model': 'models/chat-bison-001',
        'temperature': 0.4,
        'candidate_count': 1,
        'top_k': 40,
        'top_p': 0.95,
    }
    context = ""
    examples = []
    messages = [
        "what's up",
        "Hey! I'm doing well, thanks for asking. How are you doing today?"
    ]
    messages.append("NEXT REQUEST")
    response = palm.chat(
        **defaults,
        context=context,
        examples=examples,
        messages=messages
    )
    print(response.last)  # Response of the AI to your most recent request


if __name__ == "__main__":
    display_ui()
