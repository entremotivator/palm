import streamlit as st
import requests
import os

# Constants
API_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta3/models/text-bison-001:generateText"
HEADERS = {'Content-Type': 'application/json'}
IMAGE_PATH = "./Google_PaLM_Logo.svg.webp"
params = {'key': API_KEY}  # Use the API key obtained from Streamlit secrets
    data = {
        "prompt": {
            "text": prompt
        }
    }
    response = requests.post(url, headers=headers, params=params, json=data)
    return response.json() 

# Load environment variables from .env file

# Retrieve PaLM API key from environment variables or st.secrets
API_KEY = st.secrets.get("palm_api_key") or os.environ.get("PALM_API_KEY")

def configure_palm():
    import google.generativeai as palm
    palm.configure(api_key=API_KEY)

def generate_text_with_palm(prompt):
    try:
        response = requests.post(API_ENDPOINT, headers=HEADERS, params={'key': API_KEY}, json={"prompt": {"text": prompt}})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")
        return None

def display_ui():
    st.image(IMAGE_PATH, use_column_width=False, width=100)
    st.header("Chat with PaLM")
    st.write("")

    prompt = st.text_input("Prompt please...", placeholder="Prompt", label_visibility="visible")
    temp = st.slider("Temperature", 0.0, 1.0, step=0.05)    # Hyper parameter - range[0-1]

    if st.button("SEND", use_container_width=True):
        generate_and_display_response(prompt)

def generate_and_display_response(prompt):
    response = generate_text_with_palm(prompt)

    st.write("")
    st.header(":blue[Response]")
    st.write("")

    if response:
        generated_text = response.get("text", "")
        formatted_text = format_generated_text(generated_text)
        st.markdown(formatted_text, unsafe_allow_html=False, help=None)

def format_generated_text(generated_text):
    # Add any formatting or post-processing here
    formatted_text = generated_text.capitalize()  # Example: Capitalize the text
    return formatted_text

def main():
    configure_palm()
    display_ui()

if __name__ == "__main__":
    main()
