# Importing required libraries
import os
from dotenv import load_dotenv
from typing import List, Tuple

from torch import classes
import streamlit as st

from modules.streamlit_utils import launching, display_message, avatars
from modules import vanilla, function_call_chatbot, rag_chatbot, bluetooth_processor
from modules.chatbot_utils.install_utils import install_models

# Load dotenv
load_dotenv()

# Launching
classes.__path__ = [] # Must have to avoid error (somehow)

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
    if not os.getenv("MODEL_INSTALLED"):
        install_models()
        os.environ["MODEL_INSTALLED"] = "true"

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

    # Get answer from each mode
    has_error = False
    if mode == "RAG":
        answer, stream = rag_chatbot(message = question, history = history, stream = True, n_results = 4)
    elif mode == "Function calling":
        answer, stream = function_call_chatbot(message = question, history = history, stream = True)
    elif mode == "Bluetooth command":
        answer, stream = bluetooth_processor(message = question)
    elif mode == "Bluetooth command":
        answer, stream = bluetooth_processor(message = question)
    else:
        answer, stream = vanilla(message = question, history = history, stream = True)

    # Either stream or write depending on the answer
    if stream:
        with st.chat_message(name = "assistant", avatar = avatars["assistant"]):
            answer = st.write_stream(answer)
    else:
        with st.chat_message(name = "assistant", avatar = avatars["assistant"]):
            answer = st.write(answer)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": answer})