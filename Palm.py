import streamlit as st
import google.generativeai as palm
import requests
import os
import vertexai
from vertexai.preview.language_models import ChatModel

def doChat():

    # initialize vertexai
    # projectname = "my-project"
    # location = "us-central1"
    vertexai.init(project="your-project-name", location="your-project-location")

    # load model
    chat_model = ChatModel.from_pretrained("chat-bison@001")

    # define model parameters
    parameters = {
        "temperature": 0.2,
        "max_output_tokens": 256,
        "top_p": 0.8,
        "top_k": 40,
    }

    # starts a chat session with the model
    chat = chat_model.start_chat()

    # sends message to the language model and gets a response
    response = chat.send_message("hi", **parameters) # user says "hi"
    
    return response

# Invoke doChat() 
print(doChat()) # bot replies "Hi there! How can I help you today?" 
