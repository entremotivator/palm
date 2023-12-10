import streamlit as st
import subprocess
import json
import os

# Load environment variables from

# Retrieve PaLM API key from environment variables or st.secrets
API_KEY = st.secrets.get("palm_api_key") or os.environ.get("PALM_API_KEY")
palm.configure(api_key=API_KEY)

def run_curl_command(prompt):
    curl_command = [
        "curl",
        "-H", "Content-Type: application/json",
        "-H", f"x-goog-api-key: {API_KEY}",
        "-d", f'{{"prompt": {{"text": "{prompt}"}}}}',
        "https://generativelanguage.googleapis.com/v1beta3/models/text-bison-001:generateText"
    ]
    result = subprocess.run(curl_command, capture_output=True, text=True)
    return result.stdout

def main():
    st.image("./Google_PaLM_Logo.svg.webp", use_column_width=False, width=100)
    st.header("Chat with PaLM")
    st.write("")

    prompt = st.text_input("Prompt please...", placeholder="Prompt", label_visibility="visible")
    temp = st.slider("Temperature", 0.0, 1.0, step=0.05)  # Hyperparameter - range[0-1]

    if st.button("SEND", use_container_width=True):
        model = "models/text-bison-001"  # This is the only model currently available

        # Use PaLM API for text generation
        response = palm.generate_text(
            model=model,
            prompt=prompt,
            temperature=temp,
            max_output_tokens=1024
        )

        st.write("")
        st.header(":blue[Response]")
        st.write("")

        st.markdown(response.result, unsafe_allow_html=False, help=None)

        # Run curl command for verification
        st.subheader("Curl Command Verification:")
        curl_response = run_curl_command(prompt)
        st.code(curl_response, language="json")

if __name__ == "__main__":
    main()
