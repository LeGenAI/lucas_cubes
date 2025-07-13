import sys
import os
import random
import time

# Adjust path to import from the core directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.lucas_cube import GeneralizedLucasCube
from core.search_utils import PerfectCodeSearcher

class MemeticAlgorithmSearch:
    def __init__(self, n, s, population_size, generations, mutation_rate, elitism_k, local_search_steps):
        self.cube = GeneralizedLucasCube(n, s)
        self.searcher = PerfectCodeSearcher(self.cube)
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.elitism_k = elitism_k
        self.local_search_steps = local_search_steps
        self.n = n
        self.theoretical_size = (len(self.cube.vertices) + self.n) // (self.n + 1)

    def _calculate_fitness(self, code: list[str]) -> tuple[float, int, int]:
        covered_vertices = set()
        collisions = 0
        code_set = set(code)

        for codeword in code:
            neighborhood = {codeword} | set(self.cube.get_neighbors(codeword))
            # Check for collisions with other codewords' neighborhoods
            for other_cw in code_set:
                if codeword == other_cw: continue
                dist = sum(1 for i, j in zip(codeword, other_cw) if i != j)
                if dist < 3:
                    collisions += 1
            covered_vertices.update(neighborhood)
        
        uncovered_count = len(self.cube.vertex_set - covered_vertices)
        # Divide collisions by 2 as each is counted twice
        fitness = len(covered_vertices) - (uncovered_count * self.n) - (collisions // 2 * self.n * 10)
        return fitness, uncovered_count, collisions // 2

    def _local_search_optimizer(self, code: list[str]) -> list[str]:
        """Intensively tries to repair a single candidate code."""
        current_code = set(code)
        for _ in range(self.local_search_steps):
            # Try to fix a collision
            colliding_pairs = []
            for cw1 in current_code:
                for cw2 in current_code:
                    if cw1 >= cw2: continue
                    if sum(1 for i, j in zip(cw1, cw2) if i != j) < 3:
                        colliding_pairs.append((cw1, cw2))
            
            if colliding_pairs:
                # Remove one of the colliding codewords at random
                cw_to_remove = random.choice(random.choice(colliding_pairs))
                current_code.remove(cw_to_remove)
                continue # Next iteration

            # Try to cover an uncovered vertex
            all_covered = set().union(*(self.searcher.cube.get_closed_neighborhood(c) for c in current_code))
            uncovered = self.cube.vertex_set - all_covered
            if uncovered:
                vertex_to_cover = random.choice(list(uncovered))
                # Add a neighbor of the uncovered vertex as a new codeword
                potential_adds = self.cube.get_closed_neighborhood(vertex_to_cover)
                if potential_adds:
                    current_code.add(random.choice(potential_adds))

        return list(current_code)

    def _initialize_population(self):
        return [random.sample(self.cube.vertices, self.theoretical_size) for _ in range(self.population_size)]

    def _selection(self, population, fitnesses):
        total_fitness = sum(f[0] for f in fitnesses)
        if total_fitness == 0: return [random.choice(population) for _ in population]
        probs = [f[0] / total_fitness for f in fitnesses]
        return random.choices(population, weights=probs, k=self.population_size)

    def _crossover(self, parent1, parent2):
        point = random.randint(1, min(len(parent1), len(parent2)) - 1)
        return parent1[:point] + parent2[point:]

    def _mutate(self, code):
        if random.random() < self.mutation_rate:
            if code and random.random() < 0.5: code.pop(random.randrange(len(code)))
            else: code.append(random.choice(self.cube.vertices))
        return code

    def run(self):
        print("--- Running Strategy 5: Memetic Algorithm Search ---")
        population = self._initialize_population()
        start_time = time.time()

        for gen in range(self.generations):
            fitness_data = [self._calculate_fitness(ind) for ind in population]
            fitnesses = [f[0] for f in fitness_data]

            best_idx = fitnesses.index(max(fitnesses))
            best_fitness, uncovered, collisions = fitness_data[best_idx]

            if gen % 10 == 0:
                elapsed = time.time() - start_time
                print(f"Gen {gen:4d}: Best Fitness={best_fitness:.1f} | Uncovered={uncovered} | Collisions={collisions} | Time: {elapsed:.2f}s")

            if uncovered == 0 and collisions == 0:
                print("\nPerfect code conditions met! Verifying...")
                final_code = population[best_idx]
                if self.searcher.is_perfect_code(final_code):
                    print(f"\n{'='*60}")
                    print(f"✅ SUCCESS! Found a perfect code in Λ_{self.n}(1^{self.cube.s}).")
                    print(f"{'='*60}")
                    return final_code

            sorted_pop = [x for _, x in sorted(zip(fitnesses, population), key=lambda p: p[0], reverse=True)]
            new_population = sorted_pop[:self.elitism_k]

            selected = self._selection(population, fitness_data)
            while len(new_population) < self.population_size:
                p1, p2 = random.sample(selected, 2)
                child = self._crossover(p1, p2)
                child = self._mutate(child)
                child = self._local_search_optimizer(child) # Memetic step
                new_population.append(child)
            
            population = new_population

        print("\n--- Memetic Search Complete ---")
        print("❌ FAILURE. Algorithm did not find a perfect code.")
        return None

if __name__ == '__main__':
    N = 15
    S_TARGET = 12
    POP_SIZE = 100
    GENERATIONS = 10 # A longer search
    MUTATION_RATE = 0.1
    ELITISM_K = 5
    LOCAL_SEARCH_STEPS = 3 # Number of optimization steps for each child

    ma = MemeticAlgorithmSearch(N, S_TARGET, POP_SIZE, GENERATIONS, MUTATION_RATE, ELITISM_K, LOCAL_SEARCH_STEPS)
    ma.run()
