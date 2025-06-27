from duckduckgo_search import DDGS
import datetime

def search(search_query: str, region: str = "vn-vi", safesearch: str = "on", max_results: int = 3) -> list[dict]:
    '''
    A function to search using DuckDuckGo API. 
    The return value will be dictionaries of: title, href and body. Format of each instance: {'title': str, 'href': str, 'body': str}. 
    The return value could be [] when there is no search result.

    :search_query: string query that we need to search for
    :region: region for the search (au-en, ca-en, vn-vi, cn-zh, etc.)
    :safesearch: whether to apply safe search (on or off)
    :max_results: the results to include, the more the better, but will take more context
    :return: a list of dictionary results (in the "body" part of the search)
    '''

    result = DDGS().text(
        keywords = search_query,
        region = region,
        safesearch = safesearch,
        timelimit = None,
        max_results = max_results,
    )

    return result

def lookup_weather(place: str = "Binh Duong", region: str = "vn-vi", max_results: int = 2):
    '''
    A function to search for today's weather.

    :place: the place we need to look up the weather
    :region: region for the search (uk-en, au-en, ca-en, vn-vi, cn-zh, etc.)
    :max_results: the results to include, the more the better, but will take more context
    :return: a list of string results about the weather (in the "body" part of the search)
    '''
    # Get the today's weather, especially emphasizing the date
    today = datetime.datetime.now()
    today = today.strftime("%d/%m/%Y")

    # Connecting the query
    query = f'{today} weather in {place}'
    
    # Return the answer
    return search(query, region = region, max_results = max_results)

if __name__ == "__main__":
    search_query = "27/05/2025 weather Binh Duong"
    print(search(search_query))
    print(lookup_weather(place = "Thu Dau Mot"))