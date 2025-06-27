# Importing required libraries
import os
from dotenv import load_dotenv
from typing import List, Tuple

from huggingface_hub import hf_hub_download
import streamlit as st

from modules.streamlit_utils import launching, display_message, avatars
from modules.chatbot_utils import respond, vanilla, function_call_chatbot, bluetooth_processor

# Load dotenv
load_dotenv()

# Launching
# Set title and config
st.set_page_config(page_title = "Chatbot Assistant",
                    page_icon = "🥺",
                    initial_sidebar_state = "auto",
                    menu_items = {"Get help": "https://en.wikipedia.org",
                                    "Report a bug": "https://en.wikipedia.org/wiki/Insect",
                                    "About": "https://en.wikipedia.org/wiki/Duck"})
st.header("Your multi-tasking assistant (just like u)")

api_key, mode = launching()

# Welcoming message
if "opened" not in st.session_state:
    # Initial 
    history = []
    
    # Set opened to True
    st.session_state.opened = True

    if history != []:
        # Display welcoming message
        display_message("user", avatars["user"], history[0][0])
        display_message("assistant", avatars["assistant"], history[0][1])

        # Save message
        st.session_state.messages.append({"role": "user", "content": history[0][0]})
        st.session_state.messages.append({"role": "assistant", "content": history[0][1]})
else:
    session = st.session_state.messages
    history = []
    for index, message in enumerate(session):
        if index % 2 == 0:
            conversation = []
            conversation.append(message["content"])
        else:
            conversation.append(message["content"])
            history.append(tuple(conversation))

# User input
question = st.chat_input(
    placeholder = f"Your mode: {mode}",
)

if question:
    # Display
    display_message("user", avatars["user"], question)
    st.session_state.messages.append({"role": "user", "content": question})

    # Display assistant response in chat message container
    if mode == "Vanilla":
        with st.chat_message(name = "assistant", avatar = avatars["assistant"]):
            answer = st.write_stream(vanilla(message, history, stream = True))
    elif mode == "Function calling":
        with st.chat_message(name = "assistant", avatar = avatars["assistant"]):
            answer = st.write_stream(function_call_chatbot(message, history, stream = True))
    elif mode == "Bluetooth command":
        with st.chat_message(name = "assistant", avatar = avatars["assistant"]):
            answer = st.write(bluetooth_processor(message))
    elif mode == "Bluetooth command":
        with st.chat_message(name = "assistant", avatar = avatars["assistant"]):
            answer = st.write(bluetooth_processor(message))
    else:
        answer = "This is your RAG endpoint - we are still working on it."
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": answer})