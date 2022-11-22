"""
Author: Lily Smith
Course: CSCI 3725
Assignment: M6
11/21/22

This module uses the Guardian API to find an article relating to a given 
search term with a positive or negative polarity.
"""
from api_keys import GUARDIAN_API_KEY
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

BASE_REQUEST_STRING = "https://content.guardianapis.com/search"
sentiment_anlyzer = SentimentIntensityAnalyzer()

def get_polarity_scores(input):
    """
    Returns a dictionary containing pos, neg, neu, and compound scores for
    the input text using VADER's sentiment analyzer.
    Args:
        input (str): the input string containing the words to be counted
    """
    sentiment_dict = sentiment_anlyzer.polarity_scores(input)
    return sentiment_dict

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
        articles.append((article, get_polarity_scores(article)))
  
    articles.sort(key=lambda x: x[1][polarity], reverse=True)
    return articles[0][0]
