"""
"""
from population import Population
import random
from poem import Poem

class GA:
    """
    """

    def __init__(self, num_generations, population_size):
        """
        """
        self.num_generations = num_generations
        self.population_size = population_size
        self.population = Population(population_size)
        self.best_poem = None
        self.best_poem_gen = 0

    def get_next_population(self):
        """
        """
        breeding_pool = []
        for i in range(self.population_size):
            breeding_pool.append(self.population.rank_selection())
        next_population = []
        for i in range(0, len(breeding_pool), 2):
            parent1 = self.population.poems[breeding_pool[i]]
            parent2 = self.population.poems[breeding_pool[i + 1]]
            if random.random() < 1:
                child1, child2 = self.population.recombine(parent1, parent2)
            else:
                child1 = Poem(parent1.lines.copy())
                child2 = Poem(parent2.lines.copy())
            child1.mutate()
            child2.mutate()
            next_population.append(child1)
            next_population.append(child2)
        return next_population
    
    def run_ga(self):
        """
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