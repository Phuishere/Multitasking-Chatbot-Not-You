import wikitextparser as wtp
import requests

# Set a custom User-Agent to identify your application
HEADERS = {
    "User-Agent": 'Jarvis_App/1.0 ("https://github.com/CallMeQan/Jarvis-Backend-Server")'
}

def search_wiki(query: str, language: str = "en", max_results: int = 1) -> requests.Response:
    '''
    A function that search for a term on Wikipedia and return the JSON response.
    
    :query: define the Wikipedia page title (should be tone-correct)
    :language: language of the Wikipedia page (vi, en, zh, ja, de, etc.)
    :identity: used in header information in request to MediaWiki REST API
    :return: a short string describing the term in query
    '''
    # Construct the URL for the MediaWiki REST API
    url = f"https://{language}.wikipedia.org/w/rest.php/v1/search/page?q={query}&limit={max_results}"

    # Send a GET request to the API
    response = requests.get(url, headers = HEADERS)

    return response

def get_wiki_short_text(query: str, language: str = "en") -> str:
    '''
    A function that search for a term on Wikipedia and return a short
    description of that page.
    
    :query: define the Wikipedia page title (should be tone-correct)
    :language: language of the Wikipedia page (vi, en, zh, ja, de, etc.)
    :identity: used in header information in request to MediaWiki REST API
    :return: a short string describing the term in query
    '''
    # Send a GET request to the API
    response = search_wiki(query = query, language = language)

    # Check if the request was successful
    try:
        if response.status_code == 200:
            answer = response.json()
            answer = answer.get("pages")
            if answer:
                answer = answer[0]["description"]
            else:
                answer = "No information found."
        else:
            answer = "Failed to retrieve page."
    except:
        answer = "Failed to retrieve page."

    return f"{query}: {answer}"

def get_wiki_first_paragraph(query: str) -> str:
    '''
    A function that search for a term on Wikipedia and return either the first
    paragraph or a short description of that page.
    
    :query: define the Wikipedia page title (should be tone-correct)
    :language: language of the Wikipedia page (vi, en, zh, ja, de, etc.)
    :identity: used in header information in request to MediaWiki REST API
    :return: the first paragraph of the Wikipedia page or the short description
    '''
    # Set language
    language: str = "en"

    # Send a GET request to the API
    response = search_wiki(query = query, language = language)

    if response.status_code == 200:
        answer = response.json()
        answer = answer.get("pages")

        # If there is an answer, search the title.
        if answer and len(answer) > 0:
            title = answer[0]["title"]
        else:
            return "No information found."
        
        # GET the raw article of Wikipedia
        raw_response = requests.get(f"https://{language}.wikipedia.org/w/index.php?title={title}&action=raw&format=json", headers = HEADERS)

        # Use the title to look up the first paragraph. If not, use the original short description.
        if raw_response.status_code == 200:
            content = raw_response.text
            try:
                result = query + content.split(f"'''{query}'''")[1].split("\n")[0]
            except:
                return answer[0]["description"]
        
        # Parse the wikitext and extract plain text
        return wtp.parse(result).plain_text()
        
    else:
        return "Error. Cannot retrieved information."

if __name__ == "__main__":
    print(get_wiki_short_text(query = "Germany"))
    print(get_wiki_first_paragraph(query = "Germany"))