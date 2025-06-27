from .tool_search import search, lookup_weather
from .tool_wikipedia import get_wiki_first_paragraph
from .tool_gmail import send_email

def search_func(search_query: str):
    """
    Search information on the Internet.
    
    Args:
        search_query (str): Information we want to search.

    Returns:
        str: The search results of the query.
    """
    search_results = search(search_query = search_query)
    if search_results:
        context = "Search results:\n\n"
        for s in search_results:
            context += s["body"]
            context += "\n\n***\n\n"
    else:
        context = ""
    return context

# Currently on development
def price_func(search_query: str):
    """
    """
    sites = ["site:https://giaca.nsvl.com.vn/",
             "site:https://www.bachhoaxanh.com",]
    for site in sites:
        search_query = search_query + " " + site + " OR"
    price_info = search(search_query, max_results = 4)
    
    # Price information
    if price_info:
        context = "Price information:\n\n"
        for p in price_info:
            context += p["body"]
            context += "\n\n***\n\n"
    else:
        return ""
    return context

def weather_func(place: str):
    """
    Look up weather of a destination.
    
    Args:
        place (str): the place.

    Returns:
        str: The weather of place.
    """
    weather_info = lookup_weather(place)
    if weather_info:
        context = "Weather news:\n\n"
        for w in weather_info:
            context += w["body"]
            context += "\n\n***\n\n"
    else:
        context = ""
    return context

def wikipedia_func(query: str):
    """
    Look up knowledge and theory on Wikipedia.
    
    Args:
        query (str): Theory and knowledge.

    Returns:
        str: The search result of the query.
    """
    context = "Wikipedia information: " + get_wiki_first_paragraph(query)
    return context

# Gmail function - currently unavailable because of model's bad JSON parsing
def gmail_func(subject: str, content: str, sender_email: str, receiver_email: str, password: str) -> str:
    """
    Send email to user.

    Args:
        subject (str): the title of email
        content (str): the content of email
        sender_email (str): email of user (after FROM:)
        receiver_email (str): email address that receives the email (after TO:)
        password (str): user's password
    """
    content = content.replace('\n', '\\n')

    status = send_email(subject, content, sender_email, receiver_email, password)
    return status