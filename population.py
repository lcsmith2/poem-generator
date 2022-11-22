"""
Author: Lily Smith
Course: CSCI 3725
Assignment: M6
11/21/22

This module contains the Population class which is used in the GA class to
run a genetic algorithm.
"""
from poem import Poem
import random

class Population:
    """
    This class represents a population of Poem objects which is used in a
    genetic algorithm.
    """
    
    def __init__(self, population_size):
        """
        Constructor for the Population class. Generates the initial population
        of poems.
        Args:
            population_size (int): the number of poems in the population
        """
        self.poems = []
        self.population_size = population_size
        for i in range(population_size):
            self.poems.append(Poem())

    def recombine(self, poem1, poem2):
        """
        Returns the two children that result from performing uniform crossover
        with poem1 and poem2. Each line of child1 has equal probability of 
        being from poem1 or poem2. child2 is the complement of child1.
        Args:
            poem1 (Poem): the first parent
            poem2 (Poem): the second parent
        """
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
        """
        Ranks each individual with according to its fitness and chooses a 
        random poem for the breeding pool. The probability for an 
        poem to be chosen is its rank divided by the sum of all ranks in the 
        population.
        """
        total = (self.population_size * (self.population_size + 1)) / 2.0
        index = 0
        r = random.random() * total
        while index < self.population_size - 1:
            # Subtract rank of current individual (index - startIndex + 1)
            r -= index + 1
            if r <= 0.0:
                break
            index += 1
        return index
    
    def sort_population(self):
        """Sorts the population in ascending order by fitness."""
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
            result += repr(poem) + "\n\n"
        return result