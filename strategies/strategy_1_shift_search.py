import sys
import os
import itertools

# Adjust path to import from the core directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.lucas_cube import GeneralizedLucasCube
from core.code_utils import generate_hamming_code, create_coset
from core.search_utils import PerfectCodeSearcher

def find_shift_vector_by_weight(n: int, s: int, r: int, max_weight: int):
    """
    Implements the Constrained Coset Shifting strategy by searching for a low-weight shift vector.
    """
    print(f"--- Running Strategy 1: Constrained Coset Shifting for Λ_{n}(1^{s}) ---")
    print(f"Searching for a shift vector 'v' with Hamming weight <= {max_weight}.\n")

    # 1. Setup Cube, Base Code, and Searcher
    cube = GeneralizedLucasCube(n, s)
    searcher = PerfectCodeSearcher(cube)
    base_hamming_code = generate_hamming_code(r)

    print(f"Target cube Λ_{n}(1^{s}) has {len(cube)} vertices.")
    print(f"Base Ham({r}, 2) code has {len(base_hamming_code)} codewords.")

    # 2. Iterate through shift vectors of increasing weight
    total_vectors_checked = 0
    for weight in range(max_weight + 1):
        num_vectors_at_weight = 0
        # Generate all positions for the '1's in the vector
        for positions in itertools.combinations(range(n), weight):
            total_vectors_checked += 1
            num_vectors_at_weight += 1

            # Create the shift vector
            v_list = ['0'] * n
            for pos in positions:
                v_list[pos] = '1'
            v = "".join(v_list)

            # 3. Create and validate the coset
            shifted_code = create_coset(base_hamming_code, v)

            # Check if all codewords in the new coset are valid in the cube
            is_fully_valid = all(cw in cube.vertex_set for cw in shifted_code)

            if is_fully_valid:
                print(f"\nFound a promising shift vector: v = {v} (weight {weight})")
                print("All 2048 shifted codewords are valid in the cube.")
                print("Now performing the full perfect code check...")

                # 4. If valid, check if it's a perfect code
                is_perfect = searcher.is_perfect_code(shifted_code)
                if is_perfect:
                    print(f"\n{'='*60}")
                    print(f"✅ SUCCESS! Found a perfect code in Λ_{n}(1^{s}).")
                    print(f"Shift vector v = {v}")
                    print(f"{'='*60}")
                    # You can print or save the code here
                    return shifted_code
                else:
                    print("--> FAILURE. The code is valid but not perfect (neighborhoods overlap or don't cover all). Continuing search.")
        
        print(f"Checked {num_vectors_at_weight} vectors of weight {weight}. No perfect code found yet.")

    print(f"\n--- Search Complete ---")
    print(f"Checked all {total_vectors_checked} vectors with weight up to {max_weight}.")
    print(f"❌ FAILURE. No perfect code of the form v + Ham({r}, 2) was found within this weight limit.")
    return None

if __name__ == '__main__':
    # Our main target: Λ_15(1^12)
    N = 15
    S_TARGET = 12
    R = 4 # For n=15, r=4
    MAX_WEIGHT = 5 # Search vectors with up to 5 '1's

    find_shift_vector_by_weight(N, S_TARGET, R, MAX_WEIGHT)
