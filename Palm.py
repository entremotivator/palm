import streamlit as st
import os
import google.generativeai as palm


# Retrieve PaLM API key from environment variables or st.secrets
API_KEY = st.secrets.get("palm_api_key") or os.environ.get("PALM_API_KEY")
palm.configure(api_key=API_KEY)

def generate_text_with_curl(prompt):
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

def main():
    st.image("./Google_PaLM_Logo.svg.webp", use_column_width=False, width=100)
    st.header("Chat with PaLM")
    st.write("")

    prompt = st.text_input("Prompt please...", placeholder="Prompt", label_visibility="visible")
    temp = st.slider("Temperature", 0.0, 1.0, step=0.05)    # Hyper parameter - range[0-1]

    if st.button("SEND", use_container_width=True):
        # Use the cURL-like request
        response = generate_text_with_curl(prompt)

        st.write("")
        st.header(":blue[Response]")
        st.write("")

        generated_text = response.get("text", "")
        st.markdown(generated_text, unsafe_allow_html=False, help=None)

    # Display model information
    st.write("")
    st.header("Model Information")
    model_info = get_model_info()
    st.write(model_info)

if __name__ == "__main__":
    main()
