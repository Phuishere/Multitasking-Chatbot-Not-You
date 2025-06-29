# Importing required libraries
import os
from dotenv import load_dotenv
from typing import List, Tuple

from torch import classes
import streamlit as st

from modules.streamlit_utils import init_page, render_page, display_message, avatars
from modules.ux_language_utils import Locale, Translator, TextResources
from modules.ux_language_utils.data import MainText, SideBarText
from modules import vanilla, function_call_chatbot, rag_chatbot, bluetooth_processor
from modules.chatbot_utils.install_utils import install_models

# Load dotenv
load_dotenv()

# Launching and init services
classes.__path__ = [] # Must have to avoid error (somehow)

if "opened" not in st.session_state:        
    # Initialize language
    locale = Locale.ENGLISH
    translator = Translator(locale = Locale.ENGLISH)
    text = TextResources(translator = translator)

    # Config (must be at the start of the code)
    st.set_page_config(page_title = text.PAGE_TITLE,
                    page_icon = "🥺",
                    initial_sidebar_state = "auto",
                    menu_items = {
                        text.GET_HELP: "https://en.wikipedia.org",
                        text.REPORT_A_BUG: "https://en.wikipedia.org/wiki/Insect",
                        text.ABOUT: "https://en.wikipedia.org/wiki/Duck"
                    })

    # State is a dict:
    state = {
        "api_key": "",
        "mode": text.VANILLA,
        "locale": Locale.ENGLISH,
        "text": TextResources
    }

    # Render page the first time and get session state
    st.session_state.state = render_page(
        text = text,
        state = state
    )

    # Welcoming message
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
    # Relaunch
    st.session_state.state = render_page(
        text = st.session_state.state["text"],
        state = st.session_state.state
    )

    # Get session
    session = st.session_state.messages
    history = []
    for index, message in enumerate(session):
        if index % 2 == 0:
            conversation = []
            conversation.append(message["content"])
        else:
            conversation.append(message["content"])
            history.append(tuple(conversation))


# Get state and text
state = st.session_state.state
text = state["text"]

# User input
question = st.chat_input(
    placeholder = text.MODE.format(mode = state["mode"]),
)

if question:
    # Display
    display_message("user", avatars["user"], question)
    st.session_state.messages.append({"role": "user", "content": question})

    # Get answer from each mode
    if state["mode"] == text.RAG:
        answer, stream = rag_chatbot(message = question, history = history, stream = True, n_results = 4)
    elif state["mode"] == text.FUNCTION_CALLING:
        answer, stream = function_call_chatbot(message = question, history = history, stream = True)
    elif state["mode"] == text.TRANSCRIPT:
        answer, stream = vanilla(message = question, history = history, stream = True)
    elif state["mode"] == text.VANILLA:
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