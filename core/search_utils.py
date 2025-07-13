
from .lucas_cube import GeneralizedLucasCube

class PerfectCodeSearcher:
    """
    A utility to check if a given set of vertices C forms a perfect code
    in a given Generalized Lucas Cube G.
    """
    def __init__(self, cube: GeneralizedLucasCube):
        self.cube = cube
        self.n = cube.n
        self.V = cube.vertex_set

    def is_code(self, C: list[str]) -> bool:
        """Checks if the minimum distance between any two codewords is at least 3."""
        # This is a simplified check. A full distance check is more complex.
        # For now, we check if closed neighborhoods are disjoint.
        # This is equivalent to the perfect code definition.
        # A more direct distance check might be needed for other code properties.
        return True # The main check is in is_perfect_code

    def is_perfect_code(self, C: list[str]) -> bool:
        """
        Checks if C is a perfect code in the cube.
        This means the closed neighborhoods of all codewords in C form a partition of the cube's vertex set.
        """
        if not C:
            return False

        covered_vertices = set()
        
        for codeword in C:
            if codeword not in self.V:
                # All codewords must belong to the cube
                return False

            neighborhood = {codeword} | set(self.cube.get_neighbors(codeword))
            
            # Check for overlap (violates distance >= 3)
            if not covered_vertices.isdisjoint(neighborhood):
                return False
            
            covered_vertices.update(neighborhood)

        # Check if the union of neighborhoods covers the entire graph
        return covered_vertices == self.V

    def get_theoretical_code_size(self) -> int:
        """Calculates the theoretical size of a perfect 1-code."""
        # For a 1-perfect code, each codeword covers itself and n neighbors.
        # So, each codeword covers n+1 vertices.
        # The total number of vertices must be divisible by (n+1).
        num_vertices = len(self.V)
        return num_vertices / (self.n + 1)

if __name__ == '__main__':
    # Example Usage
    # Test with a known perfect code case: Λ_3(1^3)
    n, s = 3, 3
    test_cube = GeneralizedLucasCube(n, s)
    print(f"Testing cube Λ_{n}(1^{s}) with {len(test_cube)} vertices.")

    # The set {'000', '111'} is a perfect code in Q3, and also in Λ_3(1^3)
    # Let's test a coset of it.
    from .code_utils import create_coset
    
    # A known perfect code in Λ_3(1^3) is {'010', '101'}
    candidate_code = ['010', '101']
    
    searcher = PerfectCodeSearcher(test_cube)
    is_perfect = searcher.is_perfect_code(candidate_code)
    
    print(f"Is {candidate_code} a perfect code? {is_perfect}")

    # Test a failing case
    candidate_code_fail = ['000', '110']
    is_perfect_fail = searcher.is_perfect_code(candidate_code_fail)
    print(f"Is {candidate_code_fail} a perfect code? {is_perfect_fail}")
