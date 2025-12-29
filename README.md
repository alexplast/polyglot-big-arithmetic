# Polyglot Big Arithmetic

This project explores the implementation of fundamental mathematical algorithms across 9 different programming languages: **Assembler, C, C++, Go, Rust, Java, Fortran, Python, and JavaScript**.

The core objective is to compare how different languages handle large numbers, memory, and native arithmetic performance.

## Benchmarks & Results

### 1. Arbitrary Precision (BigInt)
Sorted by **Factorial** calculation time.
*   **Metric**: Median of 5 runs.
*   **Settings**: Factorial(5000), Fibonacci(25000), Power(2^20000).

<!-- BENCHMARK_BIGINT_START -->
<!-- BENCHMARK_BIGINT_END -->

### 2. Native Float Throughput
Measuring raw CPU scalar performance and loop overhead.
*   **Metric**: Total time to run Fibonacci(1475) **200,000 times**.
*   **Goal**: Compare compiler/interpreter efficiency on hot loops.

<!-- BENCHMARK_FLOAT_START -->
<!-- BENCHMARK_FLOAT_END -->

### 3. Matrix Multiplication (Native Performance)
Sorted by **Raw Throughput**.
*   **Metric**: Naive O(N^3) Matrix Multiplication (600x600).
*   **Test**: Vectorization (SIMD) capabilities and memory management.

<!-- BENCHMARK_MATRIX_START -->
<!-- BENCHMARK_MATRIX_END -->

### 4. Bubble Sort
A test of **branch prediction** and memory writes.
*   **Metric**: Sorting an array of 10,000 random `doubles` (LCG generated).
*   **Complexity**: $O(N^2) \approx 50,000,000$ comparisons/swaps.

<!-- BENCHMARK_SORT_START -->
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
