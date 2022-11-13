from api_keys import GUARDIAN_API_KEY
import requests
import lexicons
import collections

BASE_REQUEST_STRING = "https://content.guardianapis.com/search"

def get_emotion_count(input):
    emotion_lexicon = lexicons.get_emotion_lexicon()
    polarity_lexicon = lexicons.get_polarity_lexicon()
    emotion_counts = collections.defaultdict(int)
    polarity_counts = collections.defaultdict(int)
    words = input.split()
    for word in words:
        word = word.lower().strip()
        if word in emotion_lexicon:
            emotion_counts[emotion_lexicon[word]] += 1
        if word in polarity_lexicon:
            polarity_counts[polarity_lexicon[word]] += 1
    return polarity_counts

def get_article_for_term(search_term, polarity):
    query = f"?q={search_term}&api-key={GUARDIAN_API_KEY}&show-fields=bodyText"
    request_string = BASE_REQUEST_STRING + query
    response = requests.get(request_string)
    results = response.json()["response"]["results"]
    articles = []
    for result in results:
        article = result["fields"]["bodyText"]
        if not article:
            continue
        articles.append((article, get_emotion_count(article)))
  
    articles.sort(key=lambda x: x[1]["positive"] / x[1]["negative"], 
        reverse=polarity=="positive")
    return articles[0][0]
