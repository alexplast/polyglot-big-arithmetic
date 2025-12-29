# Polyglot Big Arithmetic

This project explores the implementation of fundamental mathematical algorithms across 9 different programming languages: **Assembler, C, C++, Go, Rust, Java, Fortran, Python, and JavaScript**.

The core objective is to compare how different languages handle large numbers, memory, and native arithmetic performance.

## Benchmarks & Results

### 1. Arbitrary Precision (BigInt)
Sorted by **Factorial** calculation time.
*   **Metric**: Median of 5 runs.
*   **Settings**: Factorial(5000), Fibonacci(25000), Power(2^20000).

<!-- BENCHMARK_BIGINT_START -->
| Language | Factorial (5000) | Rel Speed | Fibonacci (25000) | Power (2^20000) | BigInt Type |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Go** | 2.928 ms | 1.00x | 22.161 ms | 0.087 ms | math/big |
| **Python** | 7.507 ms | 2.56x | 10.547 ms | 0.054 ms | Native |
| **Fortran** | 10.838 ms | 3.70x | 22.453 ms | 1.279 ms | Custom Base 10^9 |
| **JavaScript** | 10.980 ms | 3.75x | 14.805 ms | 0.158 ms | BigInt |
| **C** | 11.698 ms | 4.00x | 54.304 ms | 1.476 ms | Custom Base 10^9 |
| **C++** | 12.257 ms | 4.19x | 26.044 ms | 1.228 ms | Custom Base 10^9 |
| **Rust** | 12.351 ms | 4.22x | 29.660 ms | 1.582 ms | Custom Base 10^9 |
| **Java** | 41.692 ms | 14.24x | 45.216 ms | 0.035 ms | BigInteger |

<!-- BENCHMARK_BIGINT_END -->

### 2. Native Float Throughput
Measuring raw CPU scalar performance and loop overhead.
*   **Metric**: Total time to run Fibonacci(1475) **200,000 times**.
*   **Goal**: Compare compiler/interpreter efficiency on hot loops.

<!-- BENCHMARK_FLOAT_START -->
| Language | Float Time (200k iter) | Rel Speed |
| :--- | :--- | :--- |
| **Rust** | 309.2 ms | 1.00x |
| **Java** | 318.9 ms | 1.03x |
| **Fortran** | 320.2 ms | 1.04x |
| **JavaScript** | 324.2 ms | 1.05x |
| **C++** | 412.1 ms | 1.33x |
| **C** | 415.1 ms | 1.34x |
| **Go** | 427.0 ms | 1.38x |
| **Python** | 14370.4 ms | 46.47x |

<!-- BENCHMARK_FLOAT_END -->

### 3. Matrix Multiplication (Native Performance)
Sorted by **Raw Throughput**.
*   **Metric**: Naive O(N^3) Matrix Multiplication (600x600).
*   **Test**: Vectorization (SIMD) capabilities and memory management.

<!-- BENCHMARK_MATRIX_START -->
| Language | Matrix Mult (600x600) | Relative Speed |
| :--- | :--- | :--- |
| **Fortran** | 103.650 ms | 1.00x |
| **Assembler** | 116.396 ms | 1.12x |
| **C++** | 121.178 ms | 1.17x |
| **C** | 136.074 ms | 1.31x |
| **Rust** | 138.988 ms | 1.34x |
| **Java** | 246.057 ms | 2.37x |
| **Go** | 361.133 ms | 3.48x |
| **JavaScript** | 647.985 ms | 6.25x |
| **Python** | 32468.790 ms | 313.25x |

<!-- BENCHMARK_MATRIX_END -->

### 4. Bubble Sort
A test of **branch prediction** and memory writes.
*   **Metric**: Sorting an array of 10,000 random `doubles` (LCG generated).
*   **Complexity**: $O(N^2) \approx 50,000,000$ comparisons/swaps.

<!-- BENCHMARK_SORT_START -->
| Language | Bubble Sort (10000) | Relative Speed |
| :--- | :--- | :--- |
| **Rust** | 155.709 ms | 1.00x |
| **Assembler** | 160.776 ms | 1.03x |
| **Java** | 172.475 ms | 1.11x |
| **Go** | 174.213 ms | 1.12x |
| **JavaScript** | 213.616 ms | 1.37x |
| **C** | 283.700 ms | 1.82x |
| **Fortran** | 286.458 ms | 1.84x |
| **C++** | 286.994 ms | 1.84x |
| **Python** | 7217.864 ms | 46.35x |

<!-- BENCHMARK_SORT_END -->

## Project Structure

    .
    ├── Makefile            # Central build and run system
    ├── GEMINI.md           # Technical metadata
    ├── src/                # Source code organized by language
    ├── bin/                # Compiled executables
    ├── results/            # CSV reports
    └── tests/              # Verification and benchmark scripts

## Conclusions

### 1. High-Performance Computing (Matrix vs Sort)
*   **Assembler & Fortran**: They dominate in pure number crunching (Matrix), utilizing SIMD/AVX effectively.
*   **The Rust Surprise**: In the Bubble Sort benchmark, Rust (LLVM) nearly matched hand-written Assembler, significantly outperforming C/C++ (GCC). This suggests LLVM is better at optimizing conditional swaps (likely using `cmov` or `min/max` instructions) to avoid branch misprediction penalties.
*   **JIT vs Static**: Java and Go outperformed C++ in Bubble Sort. This highlights that for logic with unpredictable branching, JIT compilers and modern GC languages can generate extremely efficient machine code.

### 2. The Cost of Abstraction (BigInt)
*   **Go**: The undisputed champion of arbitrary precision (2.9ms for Factorial). Its standard library is hand-tuned assembly.
*   **Python**: Extremely optimized for its niche (7.5ms), beating compiled languages like C++ and Rust (11ms) for these inputs because the overhead of our custom `Base 10^9` implementation outweighs Python's highly optimized internal C code for "medium" sized BigInts.

### 3. General Observations
*   **Python** is consistently ~50x to ~300x slower than compiled languages in raw algorithmic tasks, confirming the need for C-extensions (NumPy) for heavy lifting.
*   **Assembler**: Writing manual assembly (SSE2/AVX) is still the way to get the absolute maximum performance (1st place in Sort, 2nd in Matrix), but modern compilers (Fortran, Rust) are getting incredibly close.
