import json
from .chatbot_utils import respond
from .chatbot_utils.prompts import original_prompt, bluetooth_prompt, agent_output_format, agent_system_prompt
from .agent_tool.bluetooth_command_utils import add_only_flags
from .agent_tool.tool_rag import get_rag_context
from .ux_utils import TextResources