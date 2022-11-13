import random

class Poem:
    """ This class represents a poem. """
    phrase_docs = {}
    frequency_map = {}
    tag_map = {}
    NLP = None
    NUMBER_OF_LINES = 5
    TEMPLATE = [["VBN"], ["IN", "DT"], ["NN", "IN", "NN"], 
        ["IN", "DT", "NN", "IN"], ["NN"]]
    MUTATION_PROB = 0.1

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

    def get_line(self, line_number, prev_word=None):
        line = []
        for x in Poem.TEMPLATE[line_number]:
            if prev_word:
                candidates = []
                for word in Poem.frequency_map[prev_word]:
                    if word.tag_ == x:
                        candidates.append(word.text)
                if candidates:
                    line.append(random.choice(candidates))
                    continue
            if x in Poem.tag_map:
                line.append(random.choice(Poem.tag_map[x]))
        return " ".join(line)

    def get_docs_for_lines(self):
        docs = {}
        for line in self.lines:
            if line in Poem.phrase_docs:
                docs[line] = Poem.phrase_docs[line]
            else:
                docs[line] = Poem.NLP(line)
        return docs

    def get_initial_lines(self):
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
        count = 0
        score = 0
        for i in range(len(self.lines)):
            for j in range(i + 1, len(self.lines)):
                line_i_doc = self.docs[self.lines[i]]
                line_j_doc = self.docs[self.lines[j]]
                score += line_i_doc.similarity(line_j_doc)
                count += 1
        self.fitness = score / count
        return self.fitness

    def mutate2(self):
        for i in range(len(self.lines)):
            if random.random() < Poem.MUTATION_PROB:
                if i > 0:
                    last_word = self.lines[i].split()[-1]
                    self.lines[i] = self.get_line(i, last_word)
                else:
                    self.lines[i] = self.get_line(i)
                self.fitness = -1
        if self.fitness == -1:
            self.docs = self.get_docs_for_lines()

    def mutate(self):
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
        return "\n".join(self.lines) + "\n" + str(self.get_fitness())

    def __repr__(self):
        """Returns a printable representation of the poem."""
        return "\n".join(self.lines) 