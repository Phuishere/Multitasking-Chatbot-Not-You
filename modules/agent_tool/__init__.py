# Import the LlmStructuredOutputSettings
from llama_cpp_agent.llm_output_settings import LlmStructuredOutputSettings
from llama_cpp_agent.llm_output_settings import LlmStructuredOutputSettings
from .tools import search_func, weather_func, wikipedia_func, gmail_func

# Now let's create an instance of the LlmStructuredOutput class by calling the `from_functions` function of it and passing it a list of functions.
func_list = [search_func, weather_func, wikipedia_func]
output_settings = LlmStructuredOutputSettings.from_functions(func_list, allow_parallel_function_calling=True)