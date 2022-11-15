"""
"""
import random
import cmudict
from article import get_polarity_count

class Poem:
    """ This class represents a poem. """
    phrase_docs = {}
    frequency_map = {}
    tag_map = {}
    search_term_doc = None
    polarity = ""
    cmu_dict = cmudict.dict()
    nlp = None
    NUMBER_OF_LINES = 5
    MUTATION_PROB = 0.25
    MAX_NUM_RETRIES = 100
    POLARITY_WEIGHT = 0.2
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
        """
        if last_added_word:
            candidates = []
            for word in Poem.frequency_map[last_added_word]:
                if word.tag_ == tag:
                    candidates.append(word.text)
            if candidates:
                return random.choice(candidates)
        if tag in Poem.tag_map:
            return random.choice(Poem.tag_map[tag])
        return None

    def get_line(self, line_number, prev_word=None):
        """
        """
        line = []
        num_tries = 0
        while not line or (self.get_num_syllables(line) != 
            Poem.NUM_SYLLABLES[line_number] and 
            num_tries < Poem.MAX_NUM_RETRIES):
            num_tries += 1
            line = []
            last_added_word = prev_word
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
        """
        lines = []
        for i in range(Poem.NUMBER_OF_LINES):
            if lines:
                lines.append(self.get_line(i, lines[-1].split()[-1]))
            else:
                lines.append(self.get_line(i))
        return lines

    def get_fitness(self):
        """Returns the fitness of the poem."""
        if self.fitness != - 1:
            return self.fitness
        score = 0
        for i in range(len(self.lines)):
            line_i_doc = self.docs[self.lines[i]]
            score += line_i_doc.similarity(Poem.search_term_doc)
        self.fitness = score / len(self.lines)
        polarity_count = get_polarity_count(" ".join(self.lines))
        polarity_fitness = polarity_count["positive"] / \
            max(polarity_count["negative"], 1)
        if Poem.polarity == "negative":
            polarity_fitness = polarity_count["negative"] / \
                max(polarity_count["positive"], 1)
        self.fitness += polarity_fitness * Poem.POLARITY_WEIGHT
        return self.fitness

    def mutate(self):
        """
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

    def __str__(self):
        """Returns a string representation of the poem."""
        formatted_lines = []
        for line in self.lines:
            words = line.split()
            current_line = []
            first_word = words[0][0].upper() + words[0][1:]
            if first_word == "An" or first_word == "A":
                first_word = "A"
                if words[1][0].lower() in "aeiou":
                    first_word = "An"
            current_line.append(first_word)
            for i in range(1, len(words)):
                if "’" in words[i] or "'" in words[i]:
                    current_line[-1] += words[i]
                else:
                    if words[i] == "a" or words[i] == "an":
                        words[i] = "a"
                        if words[i + 1][0].lower() in "aeiou":
                            words[i] = "an"
                    current_line.append(words[i])
            formatted_lines.append(" ".join(current_line))
        return "\n".join(formatted_lines)

    def __repr__(self):
        """Returns a printable representation of the poem."""
        return "\n".join(self.lines) + "\n" + str(self.get_fitness())