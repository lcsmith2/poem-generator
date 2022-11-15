"""
This module contains the main method for running the program to generate and
speak a cinquain poem.
"""
import collections
import spacy
import sys
from poem import Poem
from ga import GA
import textacy
import article
import os

nlp = spacy.load("en_core_web_md")
NUM_GENERATIONS = 8
POPULATION_SIZE = 20

def write_output(output_filename, poem):
    if not output_filename.endswith(".txt"):
        output_filename += ".txt"
    with open(output_filename, "w") as file:
        file.write(str(poem))

def get_frequency_map(bigrams):
    """
    Maps each word to a list of words that succeed it (frequency_map) and 
    groups each word in bigrams according to its tag (tag_map). Returns 
    frequency_map and tag_map.
    Args:
        bigrams (list(tuple(str, str))): a list of tuples that contain bigrams
        from the input text
    """
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
    """
    Generates a cinquain poem using an article relating to the given term as 
    the corpus.
    """
    if len(sys.argv) != 4:
        print("Usage: python3 poem_generator.py <search term> <polarity>" \
            "<output filename>")
        return

    search_term, polarity, output_filename = sys.argv[1:]
    input = article.get_article_for_term(search_term, polarity)
    doc = nlp(input)
    bigrams = textacy.extract.ngrams(doc, n=2, filter_stops=False, 
        filter_punct=True, filter_nums=True)
    frequency_map, tag_map = get_frequency_map(bigrams)
    Poem.nlp = nlp
    Poem.frequency_map = frequency_map
    Poem.tag_map = tag_map
    Poem.search_term_doc = nlp(search_term)
    Poem.polarity = polarity
    
    ga = GA(NUM_GENERATIONS, POPULATION_SIZE)
    poem = ga.run_ga()
    write_output(output_filename, poem)
    os.system(f"say '{str(poem)}'")

if __name__ == "__main__":
    main()