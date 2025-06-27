# Importing required libraries
import os
from typing import List, Tuple
from llama_cpp import Llama
from llama_cpp_agent import LlamaCppAgent
from llama_cpp_agent.providers import LlamaCppPythonProvider
from llama_cpp_agent.chat_history import BasicChatHistory
from llama_cpp_agent.chat_history.messages import Roles
from llama_cpp_agent.messages_formatter import MessagesFormatter, PromptMarkers
from huggingface_hub import hf_hub_download

import streamlit as st
from modules.streamlit_utils import launching, display_message, avatars
from modules.chatbot_utils import respond
import json

# Define the prompt markers for Gemma 3
gemma_3_prompt_markers = {
    Roles.system: PromptMarkers("", "\n"),  # System prompt should be included within user message
    Roles.user: PromptMarkers("<start_of_turn>user\n", "<end_of_turn>\n"),
    Roles.assistant: PromptMarkers("<start_of_turn>model\n", "<end_of_turn>\n"),
    Roles.tool: PromptMarkers("", ""),  # If need tool support
}

# Create the formatter
gemma_3_formatter = MessagesFormatter(
    pre_prompt="",  # No pre-prompt
    prompt_markers=gemma_3_prompt_markers,
    include_sys_prompt_in_first_user_message=True,  # Include system prompt in first user message
    default_stop_sequences=["<end_of_turn>", "<start_of_turn>"],
    strip_prompt=False,  # Don't strip whitespace from the prompt
    bos_token="<bos>",  # Beginning of sequence token for Gemma 3
    eos_token="<eos>",  # End of sequence token for Gemma 3
)

llm = None
llm_model = None

def respond(
    message: str,
    history: List[Tuple[str, str]],
    model: str = "gemma-3-1b-it-q4_0.gguf",
    system_message: str = "You are a helpful assistant.",
    max_tokens: int = 1024,
    temperature: float = 0.7,
    top_p: float = 0.95,
    top_k: int = 40,
    repeat_penalty: float = 1.1,
):
    """
    Respond to a message using the Gemma3 model via Llama.cpp.

    Args:
        - message (str): The message to respond to.
        - history (List[Tuple[str, str]]): The chat history.
        - model (str): The model to use.
        - system_message (str): The system message to use.
        - max_tokens (int): The maximum number of tokens to generate.
        - temperature (float): The temperature of the model.
        - top_p (float): The top-p of the model.
        - top_k (int): The top-k of the model.
        - repeat_penalty (float): The repetition penalty of the model.

    Returns:
        str: The response to the message.
    """
    print("Inside the respond() function")
    try:
        # Load the global variables
        global llm
        global llm_model

        # Ensure model is not None
        if model is None:
            model = "gemma-3-1b-it-q4_0.gguf"

        # Load the model
        if llm is None or llm_model != model:
            # Check if model file exists
            model_path = f"./models/{model}"
            # if not os.path.exists(model_path):
            #     yield f"Error: Model file not found at {model_path}. Please check your model path."
            #     return

            llm = Llama(
                model_path=f"models/{model}",
                flash_attn=False,
                n_gpu_layers=0,
                n_batch=8,
                n_ctx=2048,
                n_threads=8,
                n_threads_batch=8,
            )
            llm_model = model
        provider = LlamaCppPythonProvider(llm)

        # Create the agent
        agent = LlamaCppAgent(
            provider,
            system_prompt=f"{system_message}",
            custom_messages_formatter=gemma_3_formatter,
            debug_output=True,
        )

        # Set the settings like temperature, top-k, top-p, max tokens, etc.
        settings = provider.get_provider_default_settings()
        settings.temperature = temperature
        settings.top_k = top_k
        settings.top_p = top_p
        settings.max_tokens = max_tokens
        settings.repeat_penalty = repeat_penalty
        settings.stream = True

        messages = BasicChatHistory()

        # Add the chat history
        for msn in history:
            user = {"role": Roles.user, "content": msn[0]}
            assistant = {"role": Roles.assistant, "content": msn[1]}
            messages.add_message(user)
            messages.add_message(assistant)

        # Get the response stream
        stream = agent.get_chat_response(
            message,
            llm_sampling_settings=settings,
            chat_history=messages,
            returns_streaming_generator=False,
            print_output=False,
        )

        # Generate the response
        # outputs = ""
        # for output in stream:
        #     outputs += output
        #     yield outputs
        return stream

    # Handle exceptions that may occur during the process
    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}") from e























# Launching
launching()

def parse_multiple_json(raw_text):
    decoder = json.JSONDecoder()
    pos = 0
    objects = []
    while pos < len(raw_text):
        # Loại bỏ khoảng trắng ở vị trí hiện tại
        while pos < len(raw_text) and raw_text[pos].isspace():
            pos += 1
        if pos >= len(raw_text):
            break
        try:
            obj, new_pos = decoder.raw_decode(raw_text, pos)
            objects.append(obj)
            pos = new_pos
        except json.JSONDecodeError:
            # Nếu không decode được, thoát vòng lặp
            break
    return objects

# Welcoming message
if "opened" not in st.session_state:
    # Set opened to True
    st.session_state.opened = True

    # Display welcoming message
    welcome = "Hello user, this is your personal assistant! How may I help you?"
    display_message("assistant", avatars["assistant"], welcome)

# Other stuff
# embed_model = SentenceTransformer('sentence-transformers/paraphrase-MiniLM-L6-v2')

# # Reading files
# documents = SimpleDirectoryReader("./static/document").load_data()
# index = GPTVectorStoreIndex.from_documents(documents)

# storage_context_dict=index.storage_context.to_dict()

# User input
question = st.chat_input(
    placeholder = "Can you give me a short summary?",
)

if question:
    history = [("Hello", "Hello my friend! How can I help you today?"),
               ("Please be a tsundere cat maid for me!", "Yes master 🧹🐱! What do you need me to help with? I am more than ready to support you, meow! 🐱")]
    
    display_message("user", avatars["user"], question)

    answer = respond(message = question, history = history)

    display_message("assistant", avatars["assistant"], answer)

# print("before the function")
# history = [("Hello", "Hello my friend! How can I help you today?"),
#            ("Please be a tsundere cat maid for me!", "Yes master 🧹🐱! What do you need me to help with? I am more than ready to support you, meow! 🐱")]
# respond(message = "Hi, tell me about yourself", history = history)