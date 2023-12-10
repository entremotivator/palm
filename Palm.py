# Author - MrSentinel

import streamlit as st
import google.generativeai as palm
from dotenv import load_dotenv
import os
import toml

# Load environment variables from a .env file
load_dotenv()

# Function to read configuration from config.toml
def read_config():
    with open("config.toml", "r") as file:
        config = toml.load(file)
    return config

# Read configuration from config.toml
config = read_config()

# Get the PaLM API key from the configuration file or environment variables
API_KEY = os.environ.get("PALM_API_KEY") or config["PALM"]["API_KEY"]

# Configure PaLM with the API key
palm.configure(api_key=API_KEY)

def main():
    # Access secrets using st.secrets
    st.image("./Google_PaLM_Logo.svg.webp", use_column_width=False, width=100)
    st.header("Chat with PaLM")
    st.write("")

    # User input for the prompt and temperature
    prompt = st.text_input("Prompt please...", placeholder="Prompt", label_visibility="visible")
    temp = st.slider("Temperature", 0.0, 1.0, step=0.05)  # Hyperparameter - range [0-1]

    # Button to trigger text generation
    if st.button("SEND", use_container_width=True):
        # Accessing secrets for PaLM model
        model = st.secrets["palm_model"]

        # Generate text using the specified PaLM model
        response = palm.generate_text(
            model=model,
            prompt=prompt,
            temperature=temp,
            max_output_tokens=1024
        )

        # Display the generated response
        st.write("")
        st.header(":blue[Response]")
        st.write("")
        st.markdown(response.result, unsafe_allow_html=False, help=None)

if __name__ == "__main__":
    main()
