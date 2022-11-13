from poem import Poem
import random

class Population:
    """This class represents a population of Poem objects."""
    
    def __init__(self, population_size=10):
        self.poems = []
        self.population_size = population_size
        for i in range(population_size):
            self.poems.append(Poem())

    def recombine(self, poem1, poem2):
        child1_lines = []
        child2_lines = []
        for i in range(len(poem1.lines)):
            if random.randint(0, 1) == 0:
                child1_lines.append(poem1.lines[i])
                child2_lines.append(poem2.lines[i])
            else:
                child1_lines.append(poem2.lines[i])
                child2_lines.append(poem1.lines[i])
        return (Poem(child1_lines), Poem(child2_lines))

    def rank_selection(self):
        total_weight = (self.population_size * (self.population_size + 1)) / 2.0
        index = 0
        r = random.random() * total_weight
        while index < self.population_size - 1:
            # Subtract rank of current individual (index - startIndex + 1)
            r -= index + 1
            if r <= 0.0:
                break
            index += 1
        return index
    
    def sort_population(self):
        self.poems.sort(key=lambda poem: poem.get_fitness())

    def __str__(self):
        """Returns a string representation of the population."""
        result = ""
        for poem in self.poems:
            result += str(poem) + "\n\n"
        return result

    def __repr__(self):
        """Returns a printable representation of the population."""
        result = ""
        for poem in self.poems:
            result += str(poem) + "\n\n"
        return result