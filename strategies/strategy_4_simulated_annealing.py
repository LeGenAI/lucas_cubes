import sys
import os
import random
import time
import math

# Adjust path to import from the core directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.lucas_cube import GeneralizedLucasCube
from core.search_utils import PerfectCodeSearcher

from core.code_utils import get_hamming_distance

class SimulatedAnnealingSearch:
    def __init__(self, n, s, initial_temp, cooling_rate, max_iterations, collision_penalty):
        self.cube = GeneralizedLucasCube(n, s)
        self.searcher = PerfectCodeSearcher(self.cube)
        self.n = n
        self.s = s
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate
        self.max_iterations = max_iterations
        self.collision_penalty = collision_penalty
        self.theoretical_size = self.searcher.get_theoretical_code_size()

    def _calculate_energy(self, code: list[str]) -> tuple[float, int, int]:
        """Calculates the 'energy' of a code, which is a cost function we want to minimize."""
        code_set = set(code)
        
        # 1. Calculate collisions
        collisions = 0
        for cw1 in code_set:
            for cw2 in code_set:
                if cw1 >= cw2: continue
                if get_hamming_distance(cw1, cw2) < 3:
                    collisions += 1

        # 2. Calculate uncovered vertices
        covered_vertices = set().union(*(self.cube.get_closed_neighborhood(c) for c in code_set))
        uncovered_count = len(self.cube.vertex_set - covered_vertices)

        # 3. Energy formula
        # The goal is to have 0 uncovered vertices and 0 collisions.
        # Collisions are heavily penalized as they are a hard constraint for a perfect code.
        energy = (uncovered_count * self.n) + (collisions * self.collision_penalty)
        
        return energy, uncovered_count, collisions

    def _get_neighbor(self, current_code: list[str]) -> list[str]:
        """Creates a new candidate code by making a small modification to the current one."""
        neighbor = set(current_code)
        action = random.choice(['add', 'remove', 'swap'])

        # Try to add a codeword, especially if the code is smaller than theoretical size
        if action == 'add' and len(neighbor) < self.theoretical_size + 2:
            potential_adds = list(self.cube.vertex_set - neighbor)
            if potential_adds:
                neighbor.add(random.choice(potential_adds))
        
        # Try to remove a codeword, especially if the code is larger than theoretical size
        elif action == 'remove' and len(neighbor) > self.theoretical_size - 2 and neighbor:
            neighbor.remove(random.choice(list(neighbor)))

        # Swap a codeword with a new one from the vertex set
        elif action == 'swap' and neighbor:
            to_remove = random.choice(list(neighbor))
            potential_adds = list(self.cube.vertex_set - neighbor)
            if potential_adds:
                to_add = random.choice(potential_adds)
                neighbor.remove(to_remove)
                neighbor.add(to_add)
        
        # If action failed, just add or remove one
        if not neighbor:
             neighbor.add(random.choice(self.cube.vertices))

        return list(neighbor)

    def run(self):
        print("--- Running Strategy 4: Simulated Annealing Search ---")
        start_time = time.time()

        # Initial state
        current_code = random.sample(self.cube.vertices, int(self.theoretical_size))
        current_energy, uncovered, collisions = self._calculate_energy(current_code)
        
        best_code = current_code
        best_energy = current_energy
        
        temp = self.initial_temp

        for i in range(self.max_iterations):
            neighbor_code = self._get_neighbor(current_code)
            neighbor_energy, n_uncovered, n_collisions = self._calculate_energy(neighbor_code)

            # Metropolis-Hastings acceptance criterion
            if neighbor_energy < current_energy or random.random() < math.exp((current_energy - neighbor_energy) / temp):
                current_code = neighbor_code
                current_energy, uncovered, collisions = neighbor_energy, n_uncovered, n_collisions

            # Update the best solution found so far
            if current_energy < best_energy:
                best_energy = current_energy
                best_code = current_code

            # Cool down the temperature
            temp *= self.cooling_rate

            if i % 100 == 0:
                elapsed = time.time() - start_time
                print(f"Iter {i:5d}: Temp={temp:.2f}, Energy={current_energy:.1f}, Uncovered={uncovered}, Collisions={collisions}, Best Energy={best_energy:.1f}, Time={elapsed:.2f}s")

            if best_energy == 0:
                print("\nFound a state with zero energy! Verifying if it's a perfect code...")
                if self.searcher.is_perfect_code(best_code):
                    print(f"\n{'='*60}")
                    print(f"✅ SUCCESS! Found a perfect code in Λ_{self.n}(1^{self.s}).")
                    print(f"{'='*60}")
                    return best_code
                else:
                    # This can happen if energy calculation has flaws, but is_perfect_code is the ground truth.
                    print("Verification failed. The energy function might be imperfect. Continuing search...")


        print("\n--- Simulated Annealing Search Complete ---")
        print(f"❌ FAILURE. Algorithm did not find a perfect code after {self.max_iterations} iterations.")
        print(f"Best solution found had Energy = {best_energy}")
        return None

if __name__ == '__main__':
    N = 15
    S_TARGET = 12
    
    # Hyperparameters for the search
    INITIAL_TEMP = 1000.0
    COOLING_RATE = 0.999 # Slower cooling might be better
    MAX_ITERATIONS = 50000 # More iterations for a thorough search
    COLLISION_PENALTY = N * 20 # Make collisions very costly

    sa = SimulatedAnnealingSearch(N, S_TARGET, INITIAL_TEMP, COOLING_RATE, MAX_ITERATIONS, COLLISION_PENALTY)
    sa.run()
