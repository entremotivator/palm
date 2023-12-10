import streamlit as st
from google.generativeai import configure, chat
from google.api_core import retry

# Retrieve PaLM API key from environment variables or st.secrets
API_KEY = st.secrets.get("palm_api_key")

# Import and configure google.generativeai
configure(api_key=API_KEY)

@retry.Retry()
def retry_chat(**kwargs):
    return chat(**kwargs)


def display_ui():
    st.header("Chat with PaLM")
    st.write("")

    def generate_and_display_response(prompt, model, context=""):
    response = retry_chat(
        model=model,
        context=context,
        messages=[prompt],
    )

    st.write("")
    st.header(":blue[Response]")
    st.write("")

    if response:
        generated_text = response.last.text
        formatted_text = format_generated_text(generated_text)
        st.markdown(formatted_text, unsafe_allow_html=False, help=None)

def format_generated_text(generated_text):
    # Add any formatting or post-processing here
    formatted_text = generated_text.capitalize()  # Example: Capitalize the text
    return formatted_text


if __name__ == "__main__":
    main()
