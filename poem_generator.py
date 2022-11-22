"""
Author: Lily Smith
Course: CSCI 3725
Assignment: M6
11/21/22

This module contains the main method for running the program to generate and
speak a cinquain poem. The program takes a search term and polarity as prompts
for generating the poem. 
"""
import collections
import spacy
import sys
from poem import Poem
from ga import GA
import textacy
import article
import os
import time

nlp = spacy.load("en_core_web_md")
NUM_GENERATIONS = 8
POPULATION_SIZE = 20
POLARITY_MAP = {"positive": "pos", "negative": "neg"}
LINE_DELAY = 0.3

def write_output(output_filename, poem):
    """
    Saves the poem to the specified output file.
    Args:
        output_filename (str): the name of the output file
        poem (Poem): the poem to be saved
    """
    if not output_filename.endswith(".txt"):
        output_filename += ".txt"
    with open(output_filename, "w") as file:
        file.write(str(poem))

def get_next_word_map(bigrams):
    """
    Maps each word to a list of words that succeed it (next_word_map) and 
    groups each word in bigrams according to its tag (tag_map). Returns 
    next_word_map and tag_map.
    Args:
        bigrams (list(tuple(str, str))): a list of tuples that contain bigrams
        from the input text
    """
    next_word_map = collections.defaultdict(set)
    tag_map = collections.defaultdict(set)
    for first, second in bigrams:
        first_text = first.text
        second_text = second.text
        if first.pos_ != "PROPN":
            first_text = first_text.lower()
        if second.pos_ != "PROPN":
            second_text = second_text.lower()
        next_word_map[first_text].add(second)
        tag_map[first.tag_].add(first_text)
        tag_map[second.tag_].add(second_text)

    for key, value in next_word_map.items():
        next_word_map[key] = list(value)
    for key, value in tag_map.items():
        tag_map[key] = list(value)
    return next_word_map, tag_map

def speak_poem(filename):
    """
    Uses text-to-speech to "speak" the poem from the specified filename.
    Args:
        filename (str): the name of the file containing the poem to be 
            performed
    """
    if not filename.endswith(".txt"):
        filename += ".txt"
    with open(filename) as file:
        lines = file.readlines()
        for line in lines:
            os.system(f"say '{line.strip()}'")
            time.sleep(LINE_DELAY)

def generate_poem(search_term, polarity, output_filename):
    """
    Generates a cinquain poem using an article relating to the given term as 
    the corpus.
    Args:
        search_term (str): the search term that candidate articles should 
            contain
        polarity (str): indicates whether the generated poem should have a
            positive or negative polarity
        output_filename (str): the name of the file to write the generated
            poem to
    """
    input = article.get_article_for_term(search_term, polarity)
    doc = nlp(input)
    bigrams = textacy.extract.ngrams(doc, n=2, filter_stops=False, 
        filter_punct=True, filter_nums=True)
    next_word_map, tag_map = get_next_word_map(bigrams)
    Poem.nlp = nlp
    Poem.next_word_map = next_word_map
    Poem.tag_map = tag_map
    Poem.search_term_doc = nlp(search_term)
    Poem.polarity = polarity
    
    ga = GA(NUM_GENERATIONS, POPULATION_SIZE)
    poem = ga.run_ga()
    write_output(output_filename, poem)

def main():
    """
    Performs or generates a cinquain poem that relates to the given 
    search_term and has the specified polarity.
    """
    if len(sys.argv) == 2:
        poem_file = sys.argv[1]
        try:
            speak_poem(poem_file)
        except:
            print(f"Could not find file {poem_file}")
            return
    elif len(sys.argv) == 4:
        prompt, polarity, output_filename = sys.argv[1:]
        if polarity not in POLARITY_MAP:
            print(f"Polarity must be one of the following: {POLARITY_MAP.keys()}")
            return
        polarity = POLARITY_MAP[polarity]
        generate_poem(prompt, polarity, output_filename)
        speak_poem(output_filename) 
    else:
        print("Usage: python3 poem_generator.py <prompt> <polarity>" \
            " <output filename>")


if __name__ == "__main__":
    main()