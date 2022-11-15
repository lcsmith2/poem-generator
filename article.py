"""
This module uses the Guardian API to find an article relating to a given 
search term with polarity positive or negative.
"""

from api_keys import GUARDIAN_API_KEY
import requests
import lexicons
import collections

BASE_REQUEST_STRING = "https://content.guardianapis.com/search"

def get_polarity_count(input):
    """
    Returns a dictionary containing the number positive and negative words
    input contains according to the NRC Emotion Lexicon.
    Args:
        input (str): the input string containing the words to be counted
    """
    polarity_lexicon = lexicons.get_polarity_lexicon()
    polarity_counts = collections.defaultdict(int)
    words = input.split()
    for word in words:
        word = word.lower().strip()
        if word in polarity_lexicon:
            polarity_counts[polarity_lexicon[word]] += 1
    return polarity_counts

def get_article_for_term(search_term, polarity):
    """
    Returns the body of an article that relates to search_term with the 
    highest ratio of positive to negative words if polarity is positive, and 
    negative to positive words if polarity is negative.
    Args:
        search_term (str): the term to include in the query
        polarity (str): a string equal to 'positive' or 'negative' indicating
            the polarity that the article should be
    """
    query = f"?q={search_term}&api-key={GUARDIAN_API_KEY}&show-fields=bodyText"
    request_string = BASE_REQUEST_STRING + query
    response = requests.get(request_string)
    results = response.json()["response"]["results"]
    articles = []
    for result in results:
        article = result["fields"]["bodyText"]
        if not article:
            continue
        articles.append((article, get_polarity_count(article)))
  
    articles.sort(key=lambda x: x[1]["positive"] / max(x[1]["negative"], 1), 
        reverse=polarity=="positive")
    return articles[0][0]
