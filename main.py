# Importing required libraries
import os
from dotenv import load_dotenv
from typing import List, Tuple

from torch import classes
import streamlit as st

from modules.streamlit_utils import init_page, render_page, display_message, avatars
from modules.ux_utils import Locale, Translator, TextResources
from modules.chatbot_utils import vanilla, function_call_chatbot, rag_chatbot, bluetooth_processor
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

    # TODO: Get initial history from session in DB
    st.session_state.history = []
    history = st.session_state.history
    
    # Set opened to True
    st.session_state.opened = True

    if st.session_state.history != []:
        # Display welcoming message
        display_message("user", avatars["user"], history[0][0])
        display_message("assistant", avatars["assistant"], history[0][1])

        # Save message
        st.session_state.messages.append({"type": "chat", "role": "user", "content": history[0][0]})
        st.session_state.messages.append({"type": "chat", "role": "assistant", "content": history[0][1]})

else:
    # Relaunch
    st.session_state.state = render_page(
        text = st.session_state.state["text"],
        state = st.session_state.state
    )

    # Get session
    session = st.session_state.messages
    history = st.session_state.history


# Get state and text
state = st.session_state.state
text = state["text"]

# User input
question = st.chat_input(
    placeholder = text.MODE.format(mode = state["mode"]),
)

# Get answer from each mode
if st.session_state.state["audio_transcript"]:
    # Display
    display_message("user", avatars["user"], st.session_state.state["audio_transcript"])
    st.session_state.messages.append({
        "type": "chat", "role": "user",
        "content": st.session_state.state["audio_transcript"] 
    })

    # Get transcript from audio
    question = st.session_state.state["audio_transcript"]
    answer, stream = vanilla(message = question, history = history, stream = True)

    # Either stream or write depending on the answer
    if stream:
        with st.chat_message(name = "assistant", avatar = avatars["assistant"]):
            answer = st.write_stream(answer)
    else:
        with st.chat_message(name = "assistant", avatar = avatars["assistant"]):
            answer = st.write(answer)

    # Add assistant response to chat history
    st.session_state.messages.append({"type": "chat", "role": "assistant", "content": answer})
    st.session_state.history.append((question, answer))

elif question:
    # Display
    display_message("user", avatars["user"], question)
    st.session_state.messages.append({"type": "chat", "role": "user", "content": question})

    if state["mode"] == text.RAG:
        # If file has any change, update Chroma database
        update_database = st.session_state.state.get("update_database")
        answer, stream = rag_chatbot(
            message = question, history = history, stream = True,
            n_results = 4, update_database = update_database, text = text
        )
    elif state["mode"] == text.FUNCTION_CALLING:
        answer, stream = function_call_chatbot(message = question, history = history, stream = True)
    elif state["mode"] == text.VANILLA:
        answer, stream = vanilla(message = question, history = history, stream = True)
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
    st.session_state.messages.append({"type": "chat", "role": "assistant", "content": answer})
    st.session_state.history.append((question, answer))