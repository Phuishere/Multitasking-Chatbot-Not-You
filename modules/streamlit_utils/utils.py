import tempfile
import io
import streamlit as st
import whisper
import whisper.utils
from .param import avatars
from ..ux_language_utils import Locale, Translator, TextResources, LANGUAGE_MAP

global audio_value
global audio_index
audio_index = 0

model = whisper.load_model("large-v3-turbo")

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

# Init page (only run once)
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

    global audio_index
    global audio_value
    
    # Get audio UI and audio value
    audio_value = st.audio_input(f"Record a voice message {audio_index}th", key = audio_index)
    transcript = None
    if audio_value:
        st.session_state.messages.append({"type": "audio", "role": None, "content": audio_value})
        
        # # Process data and get mel spectrogram
        # buffer = io.BytesIO()
        # # You need to set the name with the extension
        # buffer.name = "file.mp3"
        # .export(buffer, format="mp3")

        # buffer = audio_value.getbuffer()
        
        audio_bytes = audio_value.getvalue()

        buffer = io.BytesIO(audio_bytes)
        buffer.name = "audio.wav"

        with tempfile.NamedTemporaryFile(suffix = ".wav", delete = False) as tmp:
            tmp.write(buffer.getvalue())
            tmp.flush()
            audio_path = tmp.name

        audio = whisper.audio.load_audio(audio_path)
        audio = whisper.pad_or_trim(audio)
        mel = whisper.log_mel_spectrogram(audio, n_mels=model.dims.n_mels).to(model.device)

        # Detect the spoken language
        _, probs = model.detect_language(mel)
        print(f"Detected language: {max(probs, key=probs.get)}")

        # Decode the audio
        options = whisper.DecodingOptions()
        transcript = whisper.decode(model, mel, options).text

        # if not audio_value.closed:
        #     audio_value.flush()
        audio_index += 1
        audio_value = st.audio_input(f"Record a voice message {audio_index}th", key = audio_index)

    # Display message on rerun
    for message in st.session_state.messages:
        # Role variable: either "assistant" or "user"
        message_type = message["type"]

        # Display message
        if message_type == "chat":
            # Get role, content and avatar
            role = message["role"]
            content = message["content"]
            avatar = avatars[role]
            
            # Display message
            display_message(role, avatar, content)
        elif message_type == "audio":
            st.audio(message["content"])

    return {
        "api_key": api_key,
        "mode": mode,
        "locale": locale,
        "text": text,
        "audio_transcript": transcript,
    }