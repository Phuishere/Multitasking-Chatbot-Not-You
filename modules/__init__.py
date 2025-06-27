import json
from .chatbot_utils import respond
from .chatbot_utils.prompts import original_prompt, bluetooth_prompt, agent_output_format, agent_system_prompt
from .agent_tool.bluetooth_command_utils import add_only_flags
from .agent_tool.tool_rag import get_rag_context

# Only a simple chatbot
def vanilla(message: str, history: list[str], stream: bool = True):
    """
    Send message and chat session log to Server to process using the chatbot.\n
    The data shall be in this format: {"message": str, "history": [[message, answer], [message, answer], ...]}.\n
    If everything goes well, the function will send a tuple: (answer, bool). The answer could be a string or a generator.\n
    """
    # Catch error:
    try:
        # Pass the user input together with output settings to get_chat_response method.
        answer = respond(
            message, history = history,
            system_message = original_prompt, stream = stream
        )

        return answer, stream

    except Exception as e:
        return f"There was some error in the chatbot (Sever-side error).: {e}", False

# function_call_chatbot
def function_call_chatbot(message: str, history: list[str], stream: bool = True):
    """
    Send message and chat session log to Server to process using a Llama 3.2 function calling model.\n
    The data shall be in this format: {"message": str, "history": [[message, answer], [message, answer], ...]}.\n
    """
    # Catch error:
    try:
        # Pass the user input together with output settings to get_chat_response method.
        results = respond(message, use_func_call=True)

        # Get context from function calling
        if type(results) is not str: # To avoid error when the model fail to parse the JSON
            context = ""
            for result in results:
                context += f"\n## Function: {result['function']}\n"
                context += result['return_value']
        else:
            context = "No context - There is an error in parsing JSON."
        
        # Print out context
        print(f">>> Message: {message}")
        print(f">>> Context: {context}")

        # Models
        prompt = agent_output_format.format(context = context, user_input = message)
        answer = respond(
            message = prompt, history = history,
            system_message = agent_system_prompt, stream = stream
        )

        return answer, stream
    except Exception as e:
        return "There was some error in the function calling Chatbot (Sever-side error): {e}", False

# RAG model
def rag_chatbot(message: str, history: list[str], stream: bool = True, n_results: int = 4):
    """
    Send message and chat session log to Server to process using a Llama 3.2 function calling model.\n
    The data shall be in this format: {"message": str, "history": [[message, answer], [message, answer], ...]}.\n
    """
    # Catch error:
    try:
        # Pass the user input together with output settings to get_chat_response method.
        context = get_rag_context(message, n_results = 4)

        # Print out context
        print(f">>> Message: {message}")
        print(f">>> Context: {context}")

        # Models
        prompt = agent_output_format.format(context = context, user_input = message)
        answer = respond(
            message = prompt, history = history,
            system_message = agent_system_prompt, stream = stream
        )

        return answer, stream
    except Exception as e:
        return "There was some error in the RAG chatbot (Sever-side error): {e}", False
    
# Bluetooth processor using Llama 3.2 1B Instruct finetuned with GRPO
def bluetooth_processor(message: str):
    """
    Send message and chat session log to Server to process command using finetuned Llama 3.2 1B model.\n
    The data shall be in this format: {"message": str}.\n
    """
    # Catch error:
    try:
        # Loop that let model try 3 times
        tries = 0
        while True:
            try:
                # Get response from model
                answer = ""
                commands = respond(
                    message = message, history = [],
                    model = "Llama-3.2-1B-Instruct-GRPO-GGUF.gguf", system_message = bluetooth_prompt
                )

                # Load commands into JSON format (dictionary) and get the answer
                commands = json.loads(commands)
                for command in commands:
                    answer += f"{command['signal']},{command['color']};"

                # Insert only into the command using Regex
                answer = add_only_flags(
                    message, command_string = answer,                
                    colors = ["red", "green", "yellow"]
                )
                break
            
            except Exception as e:
                tries += 1
                if tries == 3:
                    return f"Failed to get the command: {e}", False
        return answer
    except:
        return f"There was some error in the Bluetooth processor (Sever-side error): {e}", False