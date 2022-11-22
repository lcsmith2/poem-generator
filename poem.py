"""
Author: Lily Smith
Course: CSCI 3725
Assignment: M6
11/21/22

This module contains the Poem class which is used to represent a poem.
"""
import random
import cmudict
from article import get_polarity_scores

class Poem:
    """ 
    This class represents a cinquain poem. A poem contains a list of lines and 
    has a fitness to indicate how similar each line is the to the target term 
    and whether the polarity of the poem aligns with what is specified. In
    addition, cinquain poems have five lines where the first through fifth 
    line have 2, 4, 6, 8, 2 syllables respectively.
    """
    phrase_docs = {}
    next_word_map = {}
    tag_map = {}
    search_term_doc = None
    polarity = ""
    cmu_dict = cmudict.dict()
    nlp = None
    NUMBER_OF_LINES = 5
    MUTATION_PROB = 0.25
    MAX_NUM_RETRIES = 100
    POLARITY_WEIGHT = 0.4
    NUM_SYLLABLES = [2, 4, 6, 8, 2]
    TEMPLATE = [
            [["NN"], ["VBN"], ["NNS"], ["NNP"]], 
            [["DT", "JJ", "NN"], ["NNP, NN"], ["VBP", "RB"]], 
            [["IN", "JJ", "NN"], ["NN", "IN", "NN"], ["DT", "JJ", "NN"]], 
            [["IN", "DT", "NN", "IN"], ["NN", "VBZ", "DT", "NN"]], 
            [["NN"], ["NNP"], ["JJ"]]
        ]

    def __init__(self, lines=[]):
        """
        Constructor for the poem class.
        Args:
            lines (list(str)): the lines for the poem
        """
        self.lines = lines
        self.fitness = -1
        if len(self.lines) == 0:
            self.lines = self.get_initial_lines()
        self.docs = self.get_docs_for_lines()

    def get_num_syllables(self, line):
        """
        Returns the number of syllables in the given line using cmudict. If
        cmudict does not contain a word, the the method returns -1.
        Args:
            line (str): the line to count the syllables for
        """
        num_syllables = 0
        for word in line:
            if word.lower() not in Poem.cmu_dict:
                return -1
            else:
                word_syllables_count = [len(list(y for y in x if 
                    y[-1].isdigit())) for x in Poem.cmu_dict[word.lower()]]
                num_syllables += max(word_syllables_count)
        return num_syllables

    def get_next_word(self, tag, last_added_word):
        """
        Returns the next word given the tag and last added word. 

        If there is a last added word, a list of candidate words with the
        specified tag is collected. If this list is not empty, one of these
        words is randomly selected and returned. Otherwise, if the tag is in 
        Poem.tag_map, a random word is returned from the list of words from
        the corpus with the specified tag. If none of these conditions are met,
        the method returns none.
        Args:
            tag (str): the string corresponding to desired the Penn Treebank
                part-of-speech tag for the next word
            last_added_word (str): the last added word in the line
        """
        if last_added_word:
            candidates = []
            for word in Poem.next_word_map[last_added_word]:
                if word.tag_ == tag:
                    candidates.append(word.text)
            if candidates:
                return random.choice(candidates)
        if tag in Poem.tag_map:
            return random.choice(Poem.tag_map[tag])
        return None

    def get_line(self, line_number, prev_word=None):
        """
        Returns a string corresponding to a line in the poem where the number
        of syllables is equal to NUM_SYLLABLES[line_number]. 
        
        A random tag structure is selected to be used as the template for the 
        line. If there is a previous word in the poem, that is also used to 
        determine what the initial word will be for the current line. A new 
        line is generated until it has the correct number of syllables or the 
        number of tries exceeds the maximum number of retries.
        Args:
            line_number (int): the line number for the line that is being
                generated
            prev_word (str): the last word of the previous line in the poem if
                it exists, else none
        """
        num_syllables = Poem.NUM_SYLLABLES[line_number]
        line = []
        num_tries = 0
        while not line or (self.get_num_syllables(line) != num_syllables and 
            num_tries < Poem.MAX_NUM_RETRIES):
            num_tries += 1
            line = []
            last_added_word = prev_word
            # Add words to line following a template of tags
            for tag in random.choice(Poem.TEMPLATE[line_number]):
                next_word = self.get_next_word(tag, last_added_word)
                if next_word:
                    line.append(next_word)
                else:
                    break
                last_added_word = line[-1]
        return " ".join(line)

    def get_docs_for_lines(self):
        """
        Returns a dictionary mapping lines in the poem to their respective
        spaCy docs.
        """
        docs = {}
        for line in self.lines:
            if line in Poem.phrase_docs:
                docs[line] = Poem.phrase_docs[line]
            else:
                docs[line] = Poem.nlp(line)
        return docs

    def get_initial_lines(self):
        """
        Returns the initial lines for the poem. Each line is generated by
        calling self.get_line()
        """
        lines = []
        for i in range(Poem.NUMBER_OF_LINES):
            if lines:
                lines.append(self.get_line(i, lines[-1].split()[-1]))
            else:
                lines.append(self.get_line(i))
        return lines

    def get_fitness(self):
        """
        Returns the fitness of the poem.
        
        The fitness of a poem is equal to similarity_score + 
        Poem.POLARITY_WEIGHT * polarity_score where similarity_score is the 
        average similarity between the search term and each line in the poem 
        using spaCy's docs and polarity_score is the ratio of text that is the
        specified polarity according to VADER's valence scores.
        """
        if self.fitness != - 1:
            return self.fitness
        score = 0
        for i in range(len(self.lines)):
            line_i_doc = self.docs[self.lines[i]]
            score += line_i_doc.similarity(Poem.search_term_doc)
        self.fitness = score / len(self.lines)
        polarity_score = get_polarity_scores(" ".join(self.lines))
        self.fitness += polarity_score[Poem.polarity] * Poem.POLARITY_WEIGHT
        return self.fitness

    def mutate(self):
        """
        Mutates the poem with probability Poem.MUTATION_PROB.
        
        If mutation is to occur, a random line is selected and replaced with
        a newly generated one using self.get_line(). If the line to be
        mutated is not the first one, the last word of the previous line is
        passed as an argument for getting the line to replace it.
        """
        if random.random() < Poem.MUTATION_PROB:
            line_to_mutate = random.randint(0, len(self.lines) - 1)
            if line_to_mutate > 0:
                last_word = self.lines[line_to_mutate - 1].split()[-1]
                self.lines[line_to_mutate] = self.get_line(line_to_mutate, 
                    last_word)
            else:
                self.lines[line_to_mutate] = self.get_line(line_to_mutate)
            self.fitness = -1
            self.docs = self.get_docs_for_lines()

    def get_formatted_lines(self):
        """
        Returns a list of formatted poem lines. Appends any tokens containing
        an apostrophe to the previous word in a line, modifies the article
        depending on if the next word starts with a vowel, and capitalizes the
        first letter of the first word in each line.
        """
        formatted_lines = []
        for line in self.lines:
            words = line.split()
            current_line = []
            for i in range(len(words)):
                if "’" in words[i] or "'" in words[i]:
                    current_line[-1] += words[i]
                else:
                    if words[i] == "a" or words[i] == "an":
                        words[i] = "a"
                        if words[i + 1][0].lower() in "aeiou":
                            words[i] = "an"
                    if i == 0:
                        words[i] = words[i][0].upper() + words[i][1:]
                    current_line.append(words[i])
            formatted_lines.append(" ".join(current_line))
        return formatted_lines

    def __str__(self):
        """Returns a string representation of the poem."""
        formatted_lines = self.get_formatted_lines()
        return "\n".join(formatted_lines)

    def __repr__(self):
        """Returns a printable representation of the poem."""
        return "\n".join(self.lines) + "\n" + str(self.get_fitness())