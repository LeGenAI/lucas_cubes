import sys
import os
import itertools

# Adjust path to import from the core directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.lucas_cube import GeneralizedLucasCube
from core.code_utils import generate_hamming_code, create_coset
from core.search_utils import PerfectCodeSearcher

def find_best_shift_for_partition(partition: set, base_code: list, n: int, weight_limit: int) -> tuple:
    """Finds the shift vector that covers the most vertices in a given partition."""
    best_v, max_coverage = None, -1

    for weight in range(weight_limit + 1):
        for positions in itertools.combinations(range(n), weight):
            v_list = ['0'] * n
            for pos in positions:
                v_list[pos] = '1'
            v = "".join(v_list)
            
            shifted_code = create_coset(base_code, v)
            coverage = sum(1 for cw in shifted_code if cw in partition)
            
            if coverage > max_coverage:
                max_coverage = coverage
                best_v = v
    
    return best_v, max_coverage

def run_strategy_3(n: int, s: int, r: int, partition_weight: int, shift_weight_limit: int):
    """
    Implements the Hybrid Code Construction strategy.
    """
    print(f"--- Running Strategy 3: Hybrid Construction for Λ_{n}(1^{s}) ---")

    # 1. Setup
    cube = GeneralizedLucasCube(n, s)
    searcher = PerfectCodeSearcher(cube)
    base_code = generate_hamming_code(r)

    # 2. Partition the vertex set
    V_low = {v for v in cube.vertex_set if v.count('1') < partition_weight}
    V_high = cube.vertex_set - V_low
    print(f"Partitioned vertices: |V_low|={len(V_low)}, |V_high|={len(V_high)}")

    # 3. Find best shift for each partition
    print("\nSearching for best shift vector for V_low...")
    v_low, cov_low = find_best_shift_for_partition(V_low, base_code, n, shift_weight_limit)
    print(f"Found v_low = {v_low} (covers {cov_low}/{len(V_low)} vertices)")

    print("\nSearching for best shift vector for V_high...")
    v_high, cov_high = find_best_shift_for_partition(V_high, base_code, n, shift_weight_limit)
    print(f"Found v_high = {v_high} (covers {cov_high}/{len(V_high)} vertices)")

    # 4. Code Splicing
    coset_low = create_coset(base_code, v_low)
    coset_high = create_coset(base_code, v_high)

    hybrid_code = {cw for cw in coset_low if cw in V_low} | {cw for cw in coset_high if cw in V_high}
    hybrid_code = list(hybrid_code)
    print(f"\nSpliced code has {len(hybrid_code)} unique codewords.")

    # 5. Repair and Verify (this is a simplified placeholder)
    print("\nInitial check of the hybrid code...")
    is_perfect = searcher.is_perfect_code(hybrid_code)

    if is_perfect:
        print(f"\n✅ SUCCESS! The initial hybrid code is already a perfect code.")
    else:
        print(f"\n❌ FAILURE. The hybrid code is not perfect. A more advanced repair/search is needed.")
        # A full-fledged local search or GA would be implemented here.
        print("This result indicates that simple splicing is not enough.")

if __name__ == '__main__':
    N = 15
    S_TARGET = 12
    R = 4
    PARTITION_WEIGHT = 8
    SHIFT_WEIGHT_LIMIT = 4 # Keep this low to be fast

    run_strategy_3(N, S_TARGET, R, PARTITION_WEIGHT, SHIFT_WEIGHT_LIMIT)
