import streamlit as st
from .param import avatars

### FUNCTIONS
# Function for message displaying and history
def display_message(name: str, avatar: str, content: str) -> None:
    """
    :name: should be either "user" or "assistant"
    :avatar: a name or an emoji
    :content: string of text
    """

    # Display assistant response in chat message container
    with st.chat_message(name = name, avatar = avatar):
        st.write(content)

# Function runs every loop
def launching():
    """
    Set of actions done every time the program is relaunched. These includes:
    + Title
    + Sidebar
    + Chat history display
    """

    # Sidebar to input stuff
    with st.sidebar:
        api_key = st.text_input("API key", key = "file_qa_api_key", type = "password")
        "[Enter password to get Llama 3.2 3B!]()"
        "[![Open in GitHub Codespaces (my link here)](https://github.com/Phuishere)]()"

        mode = st.radio(
            "Choose your mode:",
            ("Vanilla", "RAG", "Function calling", "Bluetooth command", "Whisper Transcript")
        )

    # Initialize Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [] # a list of dicts to display later

    # Display message on rerun
    for message in st.session_state.messages:
        # Role variable: either "assistant" or "user"
        name = message["role"]
        avatar = avatars[name]
        content = message["content"]

        # Set avatar and display
        display_message(name, avatar, content)

    return api_key, mode