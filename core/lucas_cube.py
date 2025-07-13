
import functools

class GeneralizedLucasCube:
    """
    Represents a Generalized Lucas Cube, Λ_n(1^s).

    This graph is an induced subgraph of the n-hypercube Q_n. Its vertices
    are all n-bit binary strings that do not contain s consecutive '1's
    in any circular permutation.
    """
    def __init__(self, n: int, s: int):
        if not (isinstance(n, int) and n > 0):
            raise ValueError("n must be a positive integer.")
        if not (isinstance(s, int) and s > 1):
            raise ValueError("s must be an integer greater than 1.")
            
        self.n = n
        self.s = s
        self.forbidden_pattern = '1' * s
        
        # Memoization for performance
        self._vertices = None
        self._vertex_set = None

    @staticmethod
    @functools.lru_cache(maxsize=None)
    def _has_forbidden_substring(bits: str, pattern: str) -> bool:
        """
        Checks if the bit string contains the forbidden pattern, considering circular shifts.
        This implementation is more explicit about checking linear and wrap-around cases.
        """
        n_len = len(bits)
        s_len = len(pattern)

        if n_len < s_len:
            return False

        # 1. Check for the pattern in the linear string
        if pattern in bits:
            return True

        # 2. Check for the pattern in the circular wrap-around
        # Create a string by concatenating the last s-1 characters with the first s-1 characters
        # This seam is sufficient to find any wrap-around patterns.
        if s_len > 1:
            seam_str = bits[n_len - s_len + 1:] + bits[:s_len - 1]
            if pattern in seam_str:
                return True
        
        return False

    def _generate_vertices(self):
        """Generates all vertices of the Λ_n(1^s) cube."""
        vertices = []
        for i in range(1 << self.n):
            bits = format(i, f'0{self.n}b')
            if not self._has_forbidden_substring(bits, self.forbidden_pattern):
                vertices.append(bits)
        return vertices

    @property
    def vertices(self) -> list[str]:
        """Returns a list of all vertices in the cube."""
        if self._vertices is None:
            self._vertices = self._generate_vertices()
        return self._vertices

    @property
    def vertex_set(self) -> set[str]:
        """Returns a set of all vertices for efficient membership testing."""
        if self._vertex_set is None:
            self._vertex_set = set(self.vertices)
        return self._vertex_set

    def __contains__(self, bits: str) -> bool:
        """Allows for `item in cube` syntax."""
        return bits in self.vertex_set

    def __len__(self) -> int:
        """Returns the number of vertices in the cube."""
        return len(self.vertices)

    def get_neighbors(self, bits: str) -> list[str]:
        """Returns the neighbors of a vertex that are also in the cube."""
        neighbors = []
        for i in range(self.n):
            neighbor_list = list(bits)
            neighbor_list[i] = '1' if bits[i] == '0' else '0'
            neighbor = "".join(neighbor_list)
            if neighbor in self:
                neighbors.append(neighbor)
        return neighbors

    def get_closed_neighborhood(self, bits: str) -> list[str]:
        """Returns the vertex and its neighbors within the cube."""
        if bits not in self:
            return []
        return [bits] + self.get_neighbors(bits)

if __name__ == '__main__':
    # Example Usage
    n, s = 7, 5
    cube = GeneralizedLucasCube(n, s)
    print(f"Created cube Λ_{n}(1^{s})")
    print(f"Number of vertices: {len(cube)}")
    print(f"Is '1111100' in the cube? {'1111100' in cube}")
    print(f"Is '0101010' in the cube? {'0101010' in cube}")

    test_vertex = cube.vertices[0]
    print(f"Neighbors of {test_vertex}: {cube.get_neighbors(test_vertex)}")
