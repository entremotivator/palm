import streamlit as st
import requests
import os
import google.generativeai as palm
from google.api_core import retry

@retry.Retry()
def retry_chat(**kwargs):
  return palm.chat(**kwargs)

@retry.Retry()
def retry_reply(self, arg):
  return self.reply(arg)

# Constants
API_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta3/models/text-bison-001:generateText"
HEADERS = {'Content-Type': 'application/json'}
IMAGE_PATH = "./Google_PaLM_Logo.svg.webp"

# Load environment variables from .env file

# Retrieve PaLM API key from environment variables or st.secrets
API_KEY = st.secrets.get("palm_api_key") 

def generate_text_with_palm(prompt):
    url = "https://generativelanguage.googleapis.com/v1beta3/models/text-bison-001:generateText"
    headers = {'Content-Type': 'application/json'}
    params = {'key': API_KEY}
    data = {
        "prompt": {
            "text": prompt
        }
    }
    response = requests.post(url, headers=headers, params=params, json=data)
    return response.json()

def configure_palm():
    # Import and configuration of google.generativeai should be done here
    import google.generativeai as palm
    palm.configure(api_key=API_KEY)

def display_ui():
    st.image(IMAGE_PATH, use_column_width=False, width=100)
    st.header("Chat with PaLM")
    st.write("")

    prompt = st.text_input("Prompt please...", placeholder="Prompt", label_visibility="visible")
    temp = st.slider("Temperature", 0.0, 1.0, step=0.05)    # Hyperparameter - range[0-1]

    if st.button("SEND", use_container_width=True):
        generate_and_display_response(prompt)

models = [m for m in palm.list_models() if 'generateMessage' in m.supported_generation_methods]
model = models[0].name
print(model)
response = retry_chat(
    model=model,
    context="You are an expert at solving word problems.",
    messages=question,
)

print(response.last)

def main():
    configure_palm()
    display_ui()

if __name__ == "__main__":
    main()
