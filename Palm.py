import streamlit as st
import google.generativeai as palm

# Load API key from Streamlit secrets
API_KEY = st.secrets["palm_api_key"]
palm.configure(api_key=API_KEY)

def chat_with_palm(messages):
    defaults = {
        'model': 'models/chat-bison-001',
        'temperature': 0.4,
        'candidate_count': 1,
        'top_k': 40,
        'top_p': 0.95,
    }
    context = ""
    examples = []
    messages.append("NEXT REQUEST")

    # Use palm.chat function to interact with the PaLM model
    response = palm.chat(
        **defaults,
        context=context,
        examples=examples,
        messages=messages
    )

    return response.last

def display_ui():
    st.title("Chat with PaLM")

    # Get user input
    user_message = st.text_input("Your Message:", "what's up")

    if st.button("Send Message"):
        # Call the chat_with_palm function to interact with the PaLM model
        response = chat_with_palm([user_message])

        # Display the AI's response
        st.text_area("PaLM's Response:", response)

if __name__ == "__main__":
    display_ui()
