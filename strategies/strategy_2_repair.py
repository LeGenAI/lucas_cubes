import sys
import os

# Adjust path to import from the core directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.lucas_cube import GeneralizedLucasCube
from core.search_utils import PerfectCodeSearcher

def load_code_from_file(filepath: str) -> list[str]:
    """Loads a code from a text file, one codeword per line."""
    with open(filepath, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def run_strategy_2(n: int, s_target: int, s_base: int, base_code_path: str):
    """
    Implements the Code Puncturing and Reconstruction strategy.
    """
    print(f"--- Running Strategy 2: Repairing from Λ_{n}(1^{s_base}) to Λ_{n}(1^{s_target}) ---")

    # 1. Setup Cubes and Searcher
    cube_target = GeneralizedLucasCube(n, s_target)
    cube_base = GeneralizedLucasCube(n, s_base)
    searcher = PerfectCodeSearcher(cube_target)

    print(f"Target cube Λ_{n}(1^{s_target}) has {len(cube_target)} vertices.")
    print(f"Base cube Λ_{n}(1^{s_base}) has {len(cube_base)} vertices.")

    # 2. Load the base perfect code
    base_code = load_code_from_file(base_code_path)
    print(f"Loaded base code with {len(base_code)} codewords from {os.path.basename(base_code_path)}.")

    # 3. Identify forbidden vertices and damaged code
    forbidden_vertices = cube_base.vertex_set - cube_target.vertex_set
    print(f"Found {len(forbidden_vertices)} vertices that are in Λ_{n}(1^{s_base}) but not in Λ_{n}(1^{s_target}).")

    damaged_code = [cw for cw in base_code if cw not in forbidden_vertices]
    removed_codewords = [cw for cw in base_code if cw in forbidden_vertices]
    print(f"Removed {len(removed_codewords)} codewords. Damaged code size: {len(damaged_code)}.")

    # 4. Identify uncovered vertices
    uncovered_vertices = set()
    for removed_cw in removed_codewords:
        # Find which vertices were covered by the removed codeword in the BASE cube
        neighborhood = {removed_cw} | set(cube_base.get_neighbors(removed_cw))
        uncovered_vertices.update(neighborhood)
    
    # Filter out vertices that are not in the target cube anyway
    uncovered_vertices &= cube_target.vertex_set
    print(f"Identified {len(uncovered_vertices)} vertices in the target cube that are now uncovered.")

    # 5. Greedy Repair Algorithm
    repaired_code = list(damaged_code)
    
    # Convert to sets for faster operations
    repaired_code_set = set(repaired_code)
    uncovered_set = set(uncovered_vertices)

    while uncovered_set:
        best_candidate = None
        max_gain = -1

        # Heuristic: only check neighbors of one uncovered vertex
        sample_vertex = next(iter(uncovered_set))
        candidate_pool = {sample_vertex} | set(cube_target.get_neighbors(sample_vertex))

        for candidate in candidate_pool:
            if candidate in repaired_code_set:
                continue

            candidate_neighborhood = {candidate} | set(cube_target.get_neighbors(candidate))
            
            # Check for collision with existing repaired code
            is_disjoint = all(v not in repaired_code_set for v in candidate_neighborhood)
            if not is_disjoint:
                continue

            # Calculate gain: how many new vertices are covered
            gain = len(uncovered_set.intersection(candidate_neighborhood))
            
            if gain > max_gain:
                max_gain = gain
                best_candidate = candidate
        
        if best_candidate and max_gain > 0:
            repaired_code.append(best_candidate)
            repaired_code_set.add(best_candidate)
            newly_covered = {best_candidate} | set(cube_target.get_neighbors(best_candidate))
            uncovered_set -= newly_covered
            print(f"  Added '{best_candidate}', covers {max_gain} new vertices. Remaining uncovered: {len(uncovered_set)}")
        else:
            print("  Could not find a candidate to make progress. Stopping repair.")
            break

    print(f"\nRepair process finished. Final code size: {len(repaired_code)}.")

    # 6. Final Verification
    if not uncovered_set:
        print("All vertices appear to be covered. Verifying if it is a perfect code...")
        is_perfect = searcher.is_perfect_code(repaired_code)
        if is_perfect:
            print(f"\n✅ SUCCESS! A perfect code was constructed for Λ_{n}(1^{s_target}).")
            # Optionally, write the code to a file
        else:
            print(f"\n❌ FAILURE. The repaired code is not a perfect code (likely due to overlaps or uncovered areas).")
    else:
        print(f"\n❌ FAILURE. Could not cover all vertices. {len(uncovered_set)} remain.")

if __name__ == '__main__':
    # Our main target: Λ_15(1^12)
    N = 15
    S_TARGET = 12
    S_BASE = 13
    # The path to the known perfect code for Λ_15(1^13)
    # This path is relative to the project root, so we adjust it.
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    BASE_CODE_FILE = os.path.join(project_root, 'codes_L15_s13.txt')

    if not os.path.exists(BASE_CODE_FILE):
        print(f"Error: Base code file not found at {BASE_CODE_FILE}")
        print("Please ensure the file from the parent directory is accessible.")
    else:
        run_strategy_2(N, S_TARGET, S_BASE, BASE_CODE_FILE)
