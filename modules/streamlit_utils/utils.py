import os
import tempfile
import io
import streamlit as st
import whisper
from .param import avatars
from ..ux_utils import ImageResources, Locale, Translator, TextResources, LANGUAGE_MAP

global audio_value
global audio_index
audio_index = 0

global whisper_model
whisper_model = None

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

        # TODO: Use this for a larger model (?)
        api_key = st.text_input("API key", key = "file_qa_api_key", type = "password")
        "[Enter password to get Gemma 3 12B!]()"
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

    global audio_index
    global audio_value
    
    # Get audio UI and audio value
    audio_transcript = None
    if mode == text.TRANSCRIPT:
        # Load whisper_model for the first time
        global whisper_model
        if not whisper_model:
            whisper_model = whisper.load_model("large-v3-turbo")

        audio_value = st.audio_input(text.TRANSCRIPT_PROMPT.format(audio_index = audio_index), key = audio_index)
        if audio_value:
            st.session_state.messages.append({"type": "audio", "role": None, "content": audio_value})
            
            audio_bytes = audio_value.getvalue()

            buffer = io.BytesIO(audio_bytes)
            buffer.name = "audio.wav"

            with tempfile.NamedTemporaryFile(suffix = ".wav", delete = False) as tmp:
                tmp.write(buffer.getvalue())
                tmp.flush()
                audio_path = tmp.name

            audio = whisper.audio.load_audio(audio_path)
            audio = whisper.pad_or_trim(audio)
            mel = whisper.log_mel_spectrogram(
                audio, n_mels = whisper_model.dims.n_mels
            ).to(whisper_model.device)

            # Detect the spoken language
            _, probs = whisper_model.detect_language(mel)
            print(f"Detected language: {max(probs, key=probs.get)}")

            # Decode the audio (transcript send to state)
            options = whisper.DecodingOptions()
            audio_transcript = whisper.decode(whisper_model, mel, options).text

            # Re-render the UI
            audio_index += 1
            audio_value = st.audio_input(
                text.TRANSCRIPT_PROMPT.format(audio_index = audio_index),
                key = audio_index
            )
    
    # Set up RAG messages and utilizations
    update_database = False
    if mode == text.RAG:
        rag_messages = []
        st.subheader(text.RAG_FILE_HEADER, divider=True)
        
        # Get directory
        rag_directory = "./res/documents_rag"
        os.makedirs(rag_directory, exist_ok=True)  # Ensure directory exists
            
        # Show files individually
        files: list[str] = []
        with st.container():
            for i, file in enumerate(os.listdir(rag_directory)):
                # Set columns for each row
                col_1, col_2, col_3, col_4 = st.columns(4)
                
                col_1.markdown(text.RAG_FILE_LABEL.format(index = i + 1))

                if file.lower().endswith(".pdf"):
                    col_2.image(ImageResources.PDF_ICON.value, )
                elif file.lower().endswith(".doc") or files[i].lower().endswith(".docx"):
                    col_2.image(ImageResources.WORD_ICON.value)
                elif file.lower().endswith(".ppt") or files[i].lower().endswith(".pptx"):
                    col_2.image(ImageResources.POWERPOINT_ICON.value)
                else:
                    col_2.image(ImageResources.CAT_READING_ICON.value)

                col_3.caption(f"File: {file}")

                # Delete button
                delete = col_4.button("❌🗑️", key = i)
                if delete:
                    # Delete from dir
                    del_file = os.path.join(rag_directory, file)
                    os.remove(del_file)

                    # Message
                    del_message = f"❌❌🗑️ File {file}"
                    rag_messages.append(del_message)

        # Upload file
        uploaded_files = st.file_uploader(
            text.RAG_PROMPT, accept_multiple_files = True
        )
        if uploaded_files:
            for uploaded_file in uploaded_files:
                # Save the file
                save_path = os.path.join(rag_directory, uploaded_file.name)
                with open(save_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # Display message
                rag_message = f"✅✅✅ File {uploaded_file.name}"
                rag_messages.append(rag_message)
        
        # If there are changes, log them and add into database
        if len(rag_messages) > 0:
            for rag_message in rag_messages:
                st.success(rag_message)
            update_database = True

    return {
        "api_key": api_key,
        "mode": mode,
        "locale": locale,
        "text": text,
        "audio_transcript": audio_transcript,
        "update_database": update_database
    }