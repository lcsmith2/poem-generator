import collections
import spacy
import sys
from poem import Poem
from ga import GA
import textacy
import article

NLP = spacy.load("en_core_web_md")

def get_frequency_map(bigrams):
    frequency_map = collections.defaultdict(set)
    tag_map = collections.defaultdict(set)
    for first, second in bigrams:
        first_text = first.text
        second_text = second.text
        if first.pos_ != "PROPN":
            first_text = first_text.lower()
        if second.pos_ != "PROPN":
            second_text = second_text.lower()
        frequency_map[first_text].add(second)
        tag_map[first.tag_].add(first_text)
        tag_map[second.tag_].add(second_text)

    for key, value in frequency_map.items():
        frequency_map[key] = list(value)
    for key, value in tag_map.items():
        tag_map[key] = list(value)
    return frequency_map, tag_map

def main():
    input = article.get_article_for_term(sys.argv[1], sys.argv[2])
    Poem.NLP = spacy.load("en_core_web_md")

    doc = NLP(input)
    bigrams = textacy.extract.ngrams(doc, n=2, filter_stops=False, 
        filter_punct=True, filter_nums=False)
    frequency_map, tag_map = get_frequency_map(bigrams)
    Poem.frequency_map = frequency_map
    Poem.tag_map = tag_map
    
    ga = GA(8, 20)
    ga.run_ga()


if __name__ == "__main__":
    main()