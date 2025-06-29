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