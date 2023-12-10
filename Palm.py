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

    # Chat box and history
    chat_history = []

    prompt = st.text_area("Type your message here...", key="input_box")
    if st.button("SEND", key="send_button"):
        # Choose the PaLM model you want to use
        models = [m for m in palm.list_models() if 'generateMessage' in m.supported_generation_methods]
        if models:
            model = models[0].name  # Adjust this based on your preference

            # Optionally, provide a context for the conversation
            context = "You are an expert at solving word problems."  # Adjust as needed

            # Retry the chat and store the conversation history
            response = retry_chat(
                model=model,
                context=context,
                messages=chat_history + [prompt],
            )

            if response:
                generated_text = response.last.text
                chat_history.append(generated_text)

    st.write("Chat History:")
    for message in chat_history:
        st.write(message)

    st.write("")
    st.header(":blue[Response]")
    st.write("")

    if chat_history:
        st.markdown(chat_history[-1], unsafe_allow_html=False, help=None)


if __name__ == "__main__":
    display_ui()
