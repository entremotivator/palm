import streamlit as st
import google.generativeai as palm
from google.api_core import retry
import json
import toml

# Load secrets from the file using st.secrets
secrets = st.secrets["google_cloud_credentials"]

# Access individual secrets
project_id = secrets["credentials"]["project_id"]
private_key_id = secrets["credentials"]["private_key_id"]
private_key = secrets["credentials"]["private_key"]
client_email = secrets["credentials"]["client"]["email"]
client_id = secrets["credentials"]["client"]["id"]
auth_uri = secrets["credentials"]["auth"]["uri"]
token_uri = secrets["credentials"]["auth"]["token_uri"]
auth_provider_x509_cert_url = secrets["credentials"]["auth"]["provider_x509_cert_url"]
client_x509_cert_url = secrets["credentials"]["client_x509_cert"]["url"]
universe_domain = secrets["metadata"]["universe_domain"]

# Streamlit app content
st.title("Google Cloud Service Account Secrets Example")
st.write(f"Project ID: {project_id}")
st.write(f"Private Key ID: {private_key_id}")
st.write(f"Client Email: {client_email}")
st.write(f"Client ID: {client_id}")
st.write(f"Auth URI: {auth_uri}")
st.write(f"Token URI: {token_uri}")
st.write(f"Auth Provider X.509 Cert URL: {auth_provider_x509_cert_url}")
st.write(f"Client X.509 Cert URL: {client_x509_cert_url}")
st.write(f"Universe Domain: {universe_domain}")

# Constants
API_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta3/models/text-bison-001:generateText"
HEADERS = {'Content-Type': 'application/json'}
IMAGE_PATH = "./Google_PaLM_Logo.svg.webp"



# Retrieve PaLM API key from environment variables or st.secrets
API_KEY = st.secrets.get("palm_api_key")

def configure_palm():
    # Import and configuration of google.generativeai should be done here
    palm.configure(api_key=API_KEY)

@retry.Retry()
def retry_chat(**kwargs):
    return palm.chat(**kwargs)

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

def display_ui():
    st.image(IMAGE_PATH, use_column_width=False, width=100)
    st.header("Chat with PaLM")
    st.write("")

    prompt = st.text_input("Prompt please...", placeholder="Prompt", label_visibility="visible")
    temp = st.slider("Temperature", 0.0, 1.0, step=0.05)  # Hyperparameter - range[0-1]

    if st.button("SEND", use_container_width=True):
        # Choose the PaLM model you want to use
        models = [m for m in palm.list_models() if 'generateMessage' in m.supported_generation_methods]
        model = models[0].name  # Adjust this based on your preference

        # Optionally, provide a context for the conversation
        context = "You are an expert at solving word problems."  # Adjust as needed

        generate_and_display_response(prompt, model, context)

def main():
    configure_palm()
    display_ui()

if __name__ == "__main__":
    main()
