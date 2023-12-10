import streamlit as st
from google.generativeai import configure, chat
from google.api_core import retry

# Retrieve PaLM API key from environment variables or st.secrets
API_KEY = st.secrets["palm_api_key"]

# Import and configure google.generativeai
configure(api_key=API_KEY)

@retry.Retry()
def retry_chat(**kwargs):
    return chat(**kwargs)

def display_ui():
    st.header("Chat with PaLM")

    # Chat box and history
    chat_history = st.empty()

    defaults = {
        'model': 'models/chat-bison-001',
        'temperature': 0.4,
        'candidate_count': 1,
        'top_k': 40,
        'top_p': 0.95,
    }
    context = ""
    examples = []
    messages = st.text_area("Your Message:", ["what's up"])

    if st.button("Send Message"):
        messages.append("NEXT REQUEST")
        response = retry_chat(
            **defaults,
            context=context,
            examples=examples,
            messages=messages
        )
        chat_history.text(response.last)  # Display the response in the UI

if __name__ == "__main__":
    display_ui()
