"""
Author: Lily Smith
Course: CSCI 3725
Assignment: M6
11/21/22

This module contains the GA class which runs a genetic algorithm to create
poems with a higher fitness.
"""
from population import Population
from poem import Poem

class GA:
    """
    Represents a genetic algorithm. This class contains methods for running the
    algorithm to get a candidate poem.
    """

    def __init__(self, num_generations, population_size):
        """
        Constructor for the GA class.
        Args:
            num_generations (int): the number of generations that should be run
            population_size (int): the number of poems in the population
        """
        self.num_generations = num_generations
        self.population_size = population_size
        self.population = Population(population_size)
        self.best_poem = None
        self.best_poem_gen = 0

    def get_next_population(self):
        """
        Returns the next population for the genetic algorithm. First,
        individuals are selected to be added to the breeding pool with 
        probability proportional to ntheir fitness. Then, for each pair of 
        parents, two children are created through recombination. Each child
        goes through mutation and is added to the next population.
        """
        breeding_pool = []
        # Get poems for breeding pool
        for i in range(self.population_size):
            breeding_pool.append(self.population.rank_selection())
        next_population = []
        for i in range(0, len(breeding_pool), 2):
            # Recombination
            parent1 = self.population.poems[breeding_pool[i]]
            parent2 = self.population.poems[breeding_pool[i + 1]]
            child1, child2 = self.population.recombine(parent1, parent2)
            # Mutation
            child1.mutate()
            child2.mutate()
            next_population.append(child1)
            next_population.append(child2)
        return next_population
    
    def run_ga(self):
        """
        Runs the genetic algorithm for self.num_generations generations and
        prints and returns the poem with the highest fitness from all created
        poems.
        """
        for i in range(self.num_generations):
            self.population.sort_population()
            best_poem_in_gen = self.population.poems[-1]
            if not self.best_poem or (best_poem_in_gen.get_fitness() > 
                self.best_poem.get_fitness()):
                self.best_poem = Poem(best_poem_in_gen.lines)
                self.best_poem_gen = i
            
            self.population.poems = self.get_next_population()
        print(f"Best poem found during generation {self.best_poem_gen} with " \
            f"fitness {round(self.best_poem.get_fitness(), 3)}:")
        print(self.best_poem)
        return self.best_poem

    def __str__(self):
        """Returns a string representation of the GA object."""
        return str(self.population)
    
    def __repr__(self):
        """Returns a printable representation of the GA object."""
        return repr(self.population)