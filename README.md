# Perfect Codes in Generalized Lucas Cubes: Theoretical Analysis and Computational Discovery

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Research](https://img.shields.io/badge/status-research-brightgreen.svg)](https://github.com/LeGenAI/lucas_cubes)

## Abstract

This repository presents a comprehensive computational exploration of perfect codes within generalized Lucas cubes Λₙ(1ˢ). Our research extends beyond Mollard's theoretical results by implementing novel algorithmic strategies to discover perfect codes in previously unexplored parameter spaces. Through systematic computational experiments, we demonstrate the existence of perfect codes in Λ₇(1⁵) and provide multiple constructive methodologies for code discovery.

## Mathematical Background

### Generalized Lucas Cubes

A **generalized Lucas cube** Λₙ(1ˢ) is an induced subgraph of the n-dimensional hypercube Qₙ whose vertices are binary strings of length n that do not contain the substring 1ˢ (s consecutive 1s) in any cyclic rotation.

**Definition**: For integers n ≥ 1 and s ≥ 2, the vertex set V(Λₙ(1ˢ)) consists of all binary strings b = b₁b₂...bₙ such that no cyclic rotation bᵢbᵢ₊₁...bₙb₁...bᵢ₋₁ contains 1ˢ as a substring.

### Perfect Codes

A subset C ⊆ V(G) is a **perfect code** (or 1-perfect code) if the closed neighborhoods N[c] = {c} ∪ {v ∈ V | d(c,v) = 1} of vertices in C form a partition of V(G).

**Key Properties**:
- **Domination**: Every vertex not in C is adjacent to exactly one vertex in C
- **Error-correction**: Minimum distance between codewords is at least 3
- **Optimality**: Perfect codes achieve the Sphere-Packing bound with equality

## Theoretical Foundations

### Known Results (Mollard, 2012)

Mollard established the following existence results for perfect codes:

1. **Proposition 3.2**: For p ≥ 2 and n = 2ᵖ - 1, Λₙ(1ⁿ) has a perfect code
2. **Proposition 3.3**: For p ≥ 2 and n = 2ᵖ - 1, both Λₙ(1ⁿ⁻¹) and Λₙ(1ⁿ⁻²) have perfect codes

### Our Contributions

We extend these results by:
- Demonstrating perfect code existence in Λ₇(1⁵), well beyond Mollard's s ≥ n-2 boundary
- Implementing computational methods to find explicit constructions
- Developing multiple algorithmic strategies for code discovery

## Implementation Architecture

### Core Modules

#### `core/lucas_cube.py`
Implements the `GeneralizedLucasCube` class with efficient algorithms for:
- Vertex generation with forbidden pattern avoidance
- Neighborhood computation in constrained hypercube
- Cyclic pattern detection with memoization

```python
class GeneralizedLucasCube:
    def __init__(self, n: int, s: int):
        self.n = n          # Dimension
        self.s = s          # Forbidden pattern length
        self.pattern = '1' * s  # s consecutive 1s
```

#### `core/code_utils.py`
Provides utilities for Hamming code generation and coset operations:
- Binary Hamming code Ham(r,2) construction
- Coset shifting for code transformation
- Hamming distance computation

#### `core/search_utils.py`
Implements the `PerfectCodeSearcher` class for code verification:
- Perfect code validation algorithms
- Theoretical bound checking
- Coverage analysis

### Search Strategies

We implemented four distinct computational approaches:

#### Strategy 1: Constrained Coset Shifting
**Method**: Systematic exploration of Hamming code cosets with low-weight shift vectors
```python
# Generate coset C' = C + v for various shift vectors v
for weight in range(MAX_WEIGHT + 1):
    for v in itertools.combinations(range(n), weight):
        coset = create_coset(hamming_code, shift_vector)
        if is_valid_lucas_cube_code(coset):
            return coset
```

#### Strategy 2: Code Puncturing and Reconstruction
**Method**: Start from known Λₙ(1ˢ⁺¹) codes and repair for Λₙ(1ˢ)
- Remove forbidden vertices from existing codes
- Greedily add codewords to cover uncovered vertices

#### Strategy 3: Hybrid Code Construction
**Method**: Partition-based optimization with code splicing
- Split vertex set by Hamming weight
- Find optimal coset for each partition
- Combine compatible codewords

#### Strategy 4: Simulated Annealing
**Method**: Metaheuristic optimization with adaptive search
```python
Energy = uncovered_count * n + collision_count * collision_penalty
```

## Experimental Results

### Lucas Cube Λ₇(1ˢ) Results

| Parameter s | Codewords Found | Code Size |
|-------------|-----------------|-----------|
| s = 3       | 11              | Optimal   |
| s = 4       | 13              | Optimal   |
| s = 5       | 15              | Optimal   |
| s = 6       | 15              | Optimal   |
| s = 7       | 16              | Optimal   |

### Lucas Cube Λ₁₅(1ˢ) Results

| Parameter s | Codewords Found | Theoretical Bound |
|-------------|-----------------|-------------------|
| s = 13      | 2,047          | ~2,047           |
| s = 14      | 2,044          | ~2,047           |
| s = 15      | 2,048          | ~2,048           |

## Key Mathematical Observations

### Theorem 1 (Extension of Mollard's Results)
Perfect codes exist in Λ₇(1⁵), demonstrating that the critical threshold s_min for code existence is significantly lower than Mollard's proven bound of n-2.

### Conjecture 1 (Critical Threshold Hypothesis)
For n = 2ᵖ - 1, there exists a critical value s_min(n) such that Λₙ(1ˢ) has a perfect code if and only if s ≥ s_min(n), where s_min(n) << n-2 for large n.

### Observation 1 (Coset Transformation Effectiveness)
The coset shifting method C' = C + v, where C is a Hamming code and v is a carefully chosen shift vector, successfully generates perfect codes for Lucas cubes with forbidden pattern lengths significantly smaller than the cube dimension.

## Installation and Usage

### Prerequisites
- Python 3.8+
- NumPy
- Itertools

### Running Experiments

```bash
# Clone the repository
git clone https://github.com/LeGenAI/lucas_cubes.git
cd lucas_code_discovery

# Run constrained coset shifting
python strategies/strategy_1_shift_search.py

# Run code repair strategy  
python strategies/strategy_2_repair.py

# Run hybrid construction
python strategies/strategy_3_hybrid.py

# Run simulated annealing
python strategies/strategy_4_simulated_annealing.py
```

### Custom Experiments

```python
from core.lucas_cube import GeneralizedLucasCube
from core.search_utils import PerfectCodeSearcher

# Create Lucas cube Λ₇(1⁵)
cube = GeneralizedLucasCube(n=7, s=5)
searcher = PerfectCodeSearcher(cube)

# Verify a code
code = ['0101000', '0100011', '0111101', ...] 
is_perfect = searcher.is_perfect_code(code)
```

## Future Research Directions

### Computational Challenges
1. **Scalability**: Extend methods to larger dimensions (n ≥ 31)
2. **Parallel Search**: Implement distributed algorithms for exhaustive exploration
3. **AI-Driven Discovery**: Integrate machine learning for pattern recognition

### Theoretical Questions
1. **Exact Threshold**: Determine s_min(n) for all n = 2ᵖ - 1
2. **Non-Binary Dimensions**: Investigate perfect codes for n ≠ 2ᵖ - 1
3. **Asymptotic Behavior**: Characterize s_min(n) as n → ∞

### Applications
- **Error-Correcting Codes**: Design efficient codes with structural constraints
- **Network Topology**: Apply to fault-tolerant network design
- **Combinatorial Optimization**: Extend to other constrained hypercube problems

## References

1. Mollard, M. (2012). The (non-)existence of perfect codes in Lucas cubes. *Discrete Applied Mathematics*, 160(15), 2171-2177.
2. Hamming, R. W. (1950). Error detecting and error correcting codes. *Bell System Technical Journal*, 29(2), 147-160.
3. Klavžar, S. (2013). Structure of Fibonacci cubes: a survey. *Journal of Combinatorial Optimization*, 25(4), 505-522.

## Authors

**재현 백 (Baek Jae Hyun)**  
Department of Mathematics, Sogang University  
CTO, DeepFountain Inc.  
GitHub: [@LeGenAI](https://github.com/LeGenAI)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Citation

If you use this work in your research, please cite:

```bibtex
@misc{baek2025lucas,
  title={Perfect Codes in Generalized Lucas Cubes: Theoretical Analysis and Computational Discovery},
  author={Baek, Jae Hyun},
  year={2025},
  url={https://github.com/LeGenAI/lucas_cubes}
}
```

---
**Created with computational mathematics and AI-driven discovery** 🔍⚡