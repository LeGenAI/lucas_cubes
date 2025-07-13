import sys
import os
import random

# Adjust path to import from the core directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.lucas_cube import GeneralizedLucasCube
from core.search_utils import PerfectCodeSearcher

class GeneticAlgorithmSearch:
    def __init__(self, n, s, population_size, generations, mutation_rate, elitism_k):
        self.cube = GeneralizedLucasCube(n, s)
        self.searcher = PerfectCodeSearcher(self.cube)
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.elitism_k = elitism_k
        self.n = n

        # Theoretical size can guide the GA
        self.theoretical_size = (len(self.cube.vertices) + self.n) // (self.n + 1)

    def _calculate_fitness(self, code: list[str]) -> float:
        covered_vertices = set()
        collisions = 0
        
        for codeword in code:
            neighborhood = {codeword} | set(self.cube.get_neighbors(codeword))
            if not covered_vertices.isdisjoint(neighborhood):
                collisions += 1
            covered_vertices.update(neighborhood)

        # Fitness is coverage minus a heavy penalty for collisions
        fitness = len(covered_vertices) - collisions * (self.n + 1) * 10 # Heavy penalty
        return fitness

    def _initialize_population(self):
        population = []
        for _ in range(self.population_size):
            # Start with a random subset of vertices of the theoretical size
            candidate = random.sample(self.cube.vertices, self.theoretical_size)
            population.append(candidate)
        return population

    def _selection(self, population, fitnesses):
        # Tournament selection
        selected = []
        for _ in range(len(population)):
            i, j = random.randrange(len(population)), random.randrange(len(population))
            winner = i if fitnesses[i] > fitnesses[j] else j
            selected.append(population[winner])
        return selected

    def _crossover(self, parent1, parent2):
        # Uniform crossover
        child = []
        p1_set, p2_set = set(parent1), set(parent2)
        # Union of parents provides the gene pool
        gene_pool = list(p1_set | p2_set)
        for gene in gene_pool:
            if random.random() < 0.5:
                if gene in p1_set:
                    child.append(gene)
            else:
                if gene in p2_set:
                    child.append(gene)
        return child

    def _mutate(self, code):
        # Add or remove a codeword
        if random.random() < self.mutation_rate:
            if len(code) > 1 and random.random() < 0.5:
                code.pop(random.randrange(len(code)))
            else:
                new_gene = random.choice(self.cube.vertices)
                if new_gene not in code:
                    code.append(new_gene)
        return code

    def run(self):
        print("--- Running Strategy 4: Genetic Algorithm Search ---")
        population = self._initialize_population()

        for gen in range(self.generations):
            fitnesses = [self._calculate_fitness(ind) for ind in population]

            best_fitness_in_gen = max(fitnesses)
            best_index = fitnesses.index(best_fitness_in_gen)
            best_code_size = len(population[best_index])

            if gen % 10 == 0:
                print(f"Gen {gen:4d}: Best Fitness = {best_fitness_in_gen:.2f}, Code Size = {best_code_size}")

            if best_fitness_in_gen >= len(self.cube.vertices):
                print("\nPotential perfect code found! Verifying...")
                final_code = population[best_index]
                if self.searcher.is_perfect_code(final_code):
                    print(f"\n{'='*60}")
                    print(f"✅ SUCCESS! Found a perfect code in Λ_{self.n}(1^{self.cube.s}).")
                    print(f"{'='*60}")
                    return final_code

            new_population = []
            # Elitism
            sorted_population = [x for _, x in sorted(zip(fitnesses, population), key=lambda pair: pair[0], reverse=True)]
            new_population.extend(sorted_population[:self.elitism_k])

            # Create the rest of the new population
            selected_parents = self._selection(population, fitnesses)
            while len(new_population) < self.population_size:
                p1, p2 = random.sample(selected_parents, 2)
                child = self._crossover(p1, p2)
                child = self._mutate(child)
                new_population.append(child)
            
            population = new_population

        print("\n--- GA Search Complete ---")
        print("❌ FAILURE. Genetic algorithm did not find a perfect code within the given generations.")
        return None

if __name__ == '__main__':
    N = 15
    S_TARGET = 12
    POP_SIZE = 100
    GENERATIONS = 1000 # Increase for a deeper search
    MUTATION_RATE = 0.1
    ELITISM_K = 5

    ga = GeneticAlgorithmSearch(N, S_TARGET, POP_SIZE, GENERATIONS, MUTATION_RATE, ELITISM_K)
    ga.run()
