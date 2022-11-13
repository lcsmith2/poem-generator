from population import Population
import random
from poem import Poem

class GA:

    def __init__(self, num_generations, population_size):
        self.num_generations = num_generations
        self.population_size = population_size
        self.population = Population(population_size)
    
    def run_ga(self):
        best_poem = None
        best_poem_gen = 0
        for i in range(self.num_generations):
            print("generation", i)
            print(self.population)
            print()
            print()
            self.population.sort_population()
            best_poem_in_gen = self.population.poems[-1]
            if not best_poem or (best_poem_in_gen.get_fitness() > 
                best_poem.get_fitness()):
                best_poem = Poem(best_poem_in_gen.lines)
                best_poem_gen = i
            breeding_pool = []
            for j in range(self.population_size):
                breeding_pool.append(self.population.rank_selection())
            next_population = []
            for j in range(0, len(breeding_pool), 2):
                parent1 = self.population.poems[breeding_pool[j]]
                parent2 = self.population.poems[breeding_pool[j + 1]]
                if random.random() < 1:
                    child1, child2 = self.population.recombine(parent1, parent2)
                else:
                    child1 = Poem(parent1.lines.copy())
                    child2 = Poem(parent2.lines.copy())
                child1.mutate()
                child2.mutate()
                next_population.append(child1)
                next_population.append(child2)
            self.population.poems = next_population
        print(f"Best poem found during generation {best_poem_gen}:")
        print(best_poem)