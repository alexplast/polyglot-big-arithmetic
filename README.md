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
| **Go** | 2.777 ms | 1.00x | 20.144 ms | 0.122 ms | math/big |
| **Python** | 7.468 ms | 2.69x | 10.820 ms | 0.057 ms | Native |
| **Fortran** | 11.103 ms | 4.00x | 22.673 ms | 1.294 ms | Custom Base 10^9 |
| **JavaScript** | 11.332 ms | 4.08x | 14.831 ms | 0.197 ms | BigInt |
| **Rust** | 11.593 ms | 4.17x | 32.637 ms | 1.616 ms | Custom Base 10^9 |
| **C** | 11.766 ms | 4.24x | 56.700 ms | 1.440 ms | Custom Base 10^9 |
| **C++** | 13.622 ms | 4.91x | 26.462 ms | 1.267 ms | Custom Base 10^9 |
| **Java** | 36.304 ms | 13.07x | 42.782 ms | 0.036 ms | BigInteger |

<!-- BENCHMARK_BIGINT_END -->

### 2. Native Float Throughput
Measuring raw CPU scalar performance and loop overhead.
*   **Metric**: Total time to run Fibonacci(1475) **200,000 times**.
*   **Goal**: Compare compiler/interpreter efficiency on hot loops.

<!-- BENCHMARK_FLOAT_START -->
| Language | Float Time (200k iter) | Rel Speed |
| :--- | :--- | :--- |
| **Rust** | 306.7 ms | 1.00x |
| **Fortran** | 309.9 ms | 1.01x |
| **Java** | 314.0 ms | 1.02x |
| **JavaScript** | 323.8 ms | 1.06x |
| **Go** | 415.0 ms | 1.35x |
| **C** | 418.6 ms | 1.36x |
| **C++** | 421.8 ms | 1.38x |
| **Python** | 14235.5 ms | 46.41x |

<!-- BENCHMARK_FLOAT_END -->

### 3. Matrix Multiplication (Native Performance)
Sorted by **Raw Throughput**.
*   **Metric**: Naive O(N^3) Matrix Multiplication (600x600).
*   **Test**: Vectorization (SIMD) capabilities and memory management.

<!-- BENCHMARK_MATRIX_START -->
| Language | Matrix Mult (600x600) | Relative Speed |
| :--- | :--- | :--- |
| **Fortran** | 96.960 ms | 1.00x |
| **Assembler** | 116.871 ms | 1.21x |
| **C** | 124.779 ms | 1.29x |
| **C++** | 127.907 ms | 1.32x |
| **Rust** | 140.233 ms | 1.45x |
| **Java** | 231.100 ms | 2.38x |
| **Go** | 352.266 ms | 3.63x |
| **JavaScript** | 618.757 ms | 6.38x |
| **Python** | 31922.753 ms | 329.24x |

<!-- BENCHMARK_MATRIX_END -->

## Project Structure

    .
    ├── Makefile            # Central build and run system
    ├── GEMINI.md           # Technical metadata
    ├── src/                # Source code organized by language
    ├── bin/                # Compiled executables
    ├── results/            # CSV reports
    └── tests/              # Verification and benchmark scripts

## Conclusions

### 1. High-Performance Computing (Matrix Benchmark)
*   **Fortran is King (98ms)**: `gfortran` produces the fastest code for array operations, beating even hand-written SSE2 Assembly (113ms) and C++ (128ms). Its strict memory rules allow for superior auto-vectorization (AVX).
*   **Assembler**: Our manual x64 Assembly (SSE2 + Loop Unrolling) outperforms C++ and Rust, proving that manual optimization still has value, though modern compilers are closing the gap.
*   **Java Surprise**: Java (229ms) beat Go (356ms) significantly. The HotSpot JIT compiler optimizes array access very effectively for long-running processes.

### 2. Native Float Loop
*   **JIT Efficiency**: In the pure scalar loop test, **Rust**, **Fortran**, and **Java** took top spots (~300-315ms).
*   **C/C++ Lag**: Surprisingly, GCC `-O3` for C/C++ produced code that was ~35% slower (~420ms) for this specific scalar Fibonacci logic compared to Rust (LLVM) or Java (JIT). This highlights differences in loop unrolling heuristics between compilers.

### 3. The Cost of Abstraction (BigInt)
*   **Go**: The undisputed champion of arbitrary precision (2.9ms for Factorial). Its standard library is hand-tuned assembly.
*   **Python**: Extremely optimized for its niche (7.5ms), beating compiled languages like C++ and Rust (11ms) for these inputs because the overhead of our custom `Base 10^9` implementation outweighs Python's highly optimized internal C code for "medium" sized BigInts.
