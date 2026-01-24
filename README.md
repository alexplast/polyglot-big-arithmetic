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
| **Go** | 9.234 ms | 1.00x | 44.194 ms | 0.235 ms | math/big |
| **Python** | 19.953 ms | 2.16x | 39.748 ms | 0.149 ms | Native |
| **Fortran** | 27.876 ms | 3.02x | 67.059 ms | 4.389 ms | Custom Base 10^9 |
| **C** | 28.334 ms | 3.07x | 75.735 ms | 4.038 ms | Custom Base 10^9 |
| **Rust** | 30.579 ms | 3.31x | 121.250 ms | 3.789 ms | Custom Base 10^9 |
| **C++** | 33.250 ms | 3.60x | 107.861 ms | 4.232 ms | Custom Base 10^9 |
| **JavaScript** | 47.517 ms | 5.15x | 54.436 ms | 0.341 ms | BigInt |
| **Java** | 122.178 ms | 13.23x | 134.933 ms | 0.091 ms | BigInteger |
<!-- BENCHMARK_BIGINT_END -->

### 2. Native Float Throughput
Measuring raw CPU scalar performance and loop overhead.
*   **Metric**: Total time to run Fibonacci(1475) **200,000 times**.
*   **Goal**: Compare compiler/interpreter efficiency on hot loops.

<!-- BENCHMARK_FLOAT_START -->
| Language | Float Time (200k iter) | Rel Speed |
| :--- | :--- | :--- |
| **C++** | 725.0 ms | 1.00x |
| **Rust** | 727.8 ms | 1.00x |
| **C** | 741.2 ms | 1.02x |
| **Go** | 838.0 ms | 1.16x |
| **JavaScript** | 974.5 ms | 1.34x |
| **Fortran** | 1075.8 ms | 1.48x |
| **Python** | 46546.9 ms | 64.20x |
| **Java** | — | — |
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
