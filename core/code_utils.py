import math
from typing import List

def _xor_bits(a: str, b: str) -> str:
    """Bitwise XOR between two equal-length binary strings."""
    return ''.join('1' if x != y else '0' for x, y in zip(a, b))

def generate_hamming_code(r: int) -> List[str]:
    """
    Generates the binary Hamming code Ham(r, 2).
    The code has length n = 2^r - 1.
    """
    n = 2**r - 1
    if n <= 0:
        raise ValueError("r must be >= 2, resulting in n > 0")

    code: List[str] = []
    # The parity-check matrix H has columns that are the binary representations of 1 to n.
    # A vector c is a codeword if Hc^T = 0.
    for i in range(1 << n):
        bits = format(i, f'0{n}b')
        syndrome = 0
        for j, bit in enumerate(bits):
            if bit == '1':
                syndrome ^= (j + 1)  # j+1 is the integer value of the column
        
        if syndrome == 0:
            code.append(bits)
    return code

def get_hamming_distance(s1: str, s2: str) -> int:
    """Calculates the Hamming distance between two binary strings."""
    if len(s1) != len(s2):
        raise ValueError("Strings must be of the same length.")
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))

def create_coset(code: List[str], shift_vector: str) -> List[str]:
    """Creates a coset of the given code by shifting with the vector."""
    if not code:
        return []
    n = len(code[0])
    if len(shift_vector) != n:
        raise ValueError("Shift vector must have the same length as the codewords.")
    
    return [_xor_bits(cw, shift_vector) for cw in code]

if __name__ == '__main__':
    # Example Usage
    r = 3
    n = 2**r - 1
    print(f"Generating Hamming code for r={r}, n={n}")
    hamming_code = generate_hamming_code(r)
    print(f"Generated Ham({r}, 2) with {len(hamming_code)} codewords.")
    print("First 5 codewords:", hamming_code[:5])

    shift_v = '0101000'
    coset = create_coset(hamming_code, shift_v)
    print(f"\nCreated a coset with shift vector {shift_v}")
    print("First 5 coset words:", coset[:5])
