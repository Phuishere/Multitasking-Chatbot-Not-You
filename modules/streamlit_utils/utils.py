import streamlit as st
from .param import avatars
from ..ux_language_utils import Locale, Translator, TextResources, LANGUAGE_MAP

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

def init_page(text: TextResources):
    # Set title
    st.header(text.TITLE)
    st.markdown("[Link Github](https://github.com/Phuishere/Multitasking-Chatbot-Not-You)")

# Function runs every loop
def render_page(text: TextResources, state: dict[str, Locale]):
    """
    Set of actions done every time the program is relaunched. These includes:
    + Title
    + Sidebar
    + Chat history display
    """

    # Sidebar to input stuff
    with st.sidebar:
        selected_language = st.sidebar.selectbox(
            "🌐 Select Language", options=list(LANGUAGE_MAP.keys())
        )
        
        locale: Locale = LANGUAGE_MAP[selected_language]
        if locale.value != state["locale"].value:
            translator = Translator(locale = locale)
            text = TextResources(translator = translator)

        api_key = st.text_input("API key", key = "file_qa_api_key", type = "password")
        "[Enter password to get Llama 3.2 3B!]()"
        "[![Open in GitHub Codespaces (our link here)](https://github.com/Phuishere)]()"

        mode = st.radio(
            text.MODE,
            (text.VANILLA, text.RAG, text.FUNCTION_CALLING, text.TRANSCRIPT)
        )
    
    init_page(text = text)

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

    return {
        "api_key": api_key,
        "mode": mode,
        "locale": locale,
        "text": text
    }