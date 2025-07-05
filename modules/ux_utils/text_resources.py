from enum import Enum

class MainText(Enum):
    # Webpage title
    PAGE_TITLE = "PAGE_TITLE"

    # Menu items
    GET_HELP = "GET_HELP"
    REPORT_A_BUG = "REPORT_A_BUG"
    ABOUT = "ABOUT"

    TITLE = "TITLE"
    CHAT_PLACE_HOLDER_FORMAT = "CHAT_PLACE_HOLDER_FORMAT"

    # Transcript and RAG file
    TRANSCRIPT_PROMPT = "TRANSCRIPT_PROMPT"
    RAG_FILE_HEADER = "RAG_FILE_HEADER"
    RAG_FILE_LABEL = "RAG_FILE_LABEL"
    RAG_PROMPT = "RAG_PROMPT"
    RAG_UPDATE_ANNOUNCEMENT = "RAG_UPDATE_ANNOUNCEMENT"

class SideBarText(Enum):
    # API key
    API_KEY = "API_KEY"

    # Modes
    MODE = "MODE"
    VANILLA = "VANILLA"
    RAG = "RAG"
    FUNCTION_CALLING = "FUNCTION_CALLING"
    TRANSCRIPT = "TRANSCRIPT"

class Locale(Enum):
    ENGLISH = "en"
    VIETNAMESE = "vn"