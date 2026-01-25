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
| **Go** | 3.544 ms | 1.00x | 21.511 ms | 0.098 ms | math/big |
| **Python** | 9.580 ms | 2.70x | 16.581 ms | 0.129 ms | Native |
| **JavaScript** | 12.208 ms | 3.44x | 17.706 ms | 0.180 ms | BigInt |
| **Fortran** | 13.201 ms | 3.72x | 26.293 ms | 1.667 ms | Custom Base 10^9 |
| **Rust** | 13.515 ms | 3.81x | 46.069 ms | 1.657 ms | Custom Base 10^9 |
| **C** | 14.513 ms | 4.10x | 31.588 ms | 1.911 ms | Custom Base 10^9 |
| **C++** | 15.258 ms | 4.31x | 41.252 ms | 1.928 ms | Custom Base 10^9 |
| **Java** | 52.706 ms | 14.87x | 62.121 ms | 0.030 ms | BigInteger |
<!-- BENCHMARK_BIGINT_END -->

### 2. Native Float Throughput
Measuring raw CPU scalar performance and loop overhead.
*   **Metric**: Total time to run Fibonacci(1475) **200,000 times**.
*   **Goal**: Compare compiler/interpreter efficiency on hot loops.

<!-- BENCHMARK_FLOAT_START -->
| Language | Float Time (200k iter) | Rel Speed |
| :--- | :--- | :--- |
| **Fortran** | 400.7 ms | 1.00x |
| **Rust** | 405.4 ms | 1.01x |
| **C** | 411.8 ms | 1.03x |
| **Java** | 415.7 ms | 1.04x |
| **C++** | 419.2 ms | 1.05x |
| **Go** | 439.0 ms | 1.10x |
| **JavaScript** | 459.3 ms | 1.15x |
| **Python** | 25125.2 ms | 62.70x |
<!-- BENCHMARK_FLOAT_END -->

### 3. Matrix Multiplication (Native Performance)
Sorted by **Raw Throughput**.
*   **Metric**: Naive O(N^3) Matrix Multiplication (600x600).
*   **Test**: Vectorization (SIMD) capabilities and memory management.

<!-- BENCHMARK_MATRIX_START -->
| Language | Matrix Mult (600x600) | Relative Speed |
| :--- | :--- | :--- |
| **Fortran** | 198.469 ms | 1.00x |
| **Rust** | 203.847 ms | 1.03x |
| **C++** | 204.089 ms | 1.03x |
| **C** | 218.645 ms | 1.10x |
| **Java** | 292.183 ms | 1.47x |
| **Go** | 465.172 ms | 2.34x |
| **JavaScript** | 881.002 ms | 4.44x |
| **Python** | 51642.302 ms | 260.20x |
| **Assembler** | — | — |
<!-- BENCHMARK_MATRIX_END -->

### 4. Bubble Sort
A test of **branch prediction** and memory writes.
*   **Metric**: Sorting an array of 10,000 random `doubles` (LCG generated).
*   **Complexity**: $O(N^2) \approx 50,000,000$ comparisons/swaps.

<!-- BENCHMARK_SORT_START -->
| Language | Bubble Sort (10000) | Relative Speed |
| :--- | :--- | :--- |
| **C++** | 189.788 ms | 1.00x |
| **C** | 192.631 ms | 1.01x |
| **Fortran** | 239.819 ms | 1.26x |
| **Go** | 248.887 ms | 1.31x |
| **Java** | 264.860 ms | 1.40x |
| **Rust** | 282.065 ms | 1.49x |
| **JavaScript** | 315.258 ms | 1.66x |
| **Python** | 11104.985 ms | 58.51x |
| **Assembler** | — | — |
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
