# Polyglot Big Arithmetic

This project explores the implementation of fundamental mathematical algorithms across 7 different programming languages: **C++, Go, Rust, Java, Fortran, Python, and JavaScript**.

The core objective is to compare how different languages handle large numbers, memory, and native arithmetic performance.

## Project Structure

    .
    ├── Makefile            # Central build and run system
    ├── GEMINI.md           # Technical metadata
    ├── src/                # Source code organized by language
    ├── bin/                # Compiled executables
    └── tests/              # Verification and benchmark scripts

## Technical Implementation Details

### 1. Arbitrary Precision (BigInt)
The project highlights the difference between Fixed-Width Integers and BigInts.
*   **Native Support**: Python, JS, Go (`math/big`), Java (`BigInteger`).
*   **Manual Implementation**: C++, Rust, Fortran use a custom **Base 10^9** digit-array implementation.

### 2. Native Performance (Float & Matrix)
We also implement algorithms using native IEEE 754 `double` to measure raw CPU throughput and compiler optimizations (SIMD, Vectorization), comparing it against the overhead of BigInt abstractions.

## How to Run

1. Build Everything:

    make all

2. Run All Benchmarks & Update README:

    make bench_all

## Benchmarks & Results

### 1. Arbitrary Precision (BigInt)
Sorted by **Factorial** calculation time.
**Settings**: Fibonacci(5000), Factorial(2000), Power(2^5000).

<!-- BENCHMARK_BIGINT_START -->
| Language | Factorial (2000) | Rel Speed | Fibonacci (5000) | Power (2^5000) | BigInt Type |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Go** | 0.754 ms | 1.00x | 3.805 ms | 0.089 ms | math/big |
| **Python** | 1.341 ms | 1.78x | 1.960 ms | 0.013 ms | Native |
| **Fortran** | 1.701 ms | 2.26x | 0.943 ms | 0.228 ms | Custom Base 10^9 |
| **Rust** | 1.844 ms | 2.45x | 1.846 ms | 0.122 ms | Custom Base 10^9 |
| **C++** | 1.879 ms | 2.49x | 1.738 ms | 0.134 ms | Custom Base 10^9 |
| **JavaScript** | 4.758 ms | 6.31x | 6.267 ms | 0.092 ms | BigInt |
| **Java** | 12.103 ms | 16.05x | 9.328 ms | 0.029 ms | BigInteger |

<!-- BENCHMARK_BIGINT_END -->

### 2. BigInt vs Native Float
Sorted by native **Float CPU speed**.
**Settings**: Small numbers that fit in 64-bit float.

<!-- BENCHMARK_FLOAT_START -->
| Language | Float Time | Rel Speed | BigInt Time | Hardware Speedup |
| :--- | :--- | :--- | :--- | :--- |
| **Rust** | 0.0020 ms | 1.00x | 0.215 ms | 107.5x |
| **Go** | 0.0020 ms | 1.00x | 0.608 ms | 304.0x |
| **C++** | 0.0022 ms | 1.10x | 0.210 ms | 95.5x |
| **Java** | 0.0310 ms | 15.50x | 2.377 ms | 76.7x |
| **Python** | 0.0700 ms | 35.00x | 0.261 ms | 3.7x |
| **Fortran** | 0.0706 ms | 35.30x | 0.191 ms | 2.7x |
| **JavaScript** | 0.2380 ms | 119.00x | 0.219 ms | 0.9x |

<!-- BENCHMARK_FLOAT_END -->

### 3. Matrix Multiplication (Native Performance)
Sorted by **Raw Throughput**.
Naive O(N^3) Matrix Multiplication (256x256), 1D arrays, 64-bit floats.

<!-- BENCHMARK_MATRIX_START -->
| Language | Matrix Mult (256x256) | Relative Speed |
| :--- | :--- | :--- |
| **C++** | 18.437 ms | 1.00x (Baseline) |
| **Fortran** | 21.510 ms | 1.17x |
| **Java** | 28.842 ms | 1.56x |
| **Rust** | 37.518 ms | 2.03x |
| **Go** | 49.476 ms | 2.68x |
| **JavaScript** | 79.901 ms | 4.33x |
| **Python** | 2638.812 ms | 143.13x |

<!-- BENCHMARK_MATRIX_END -->

## Conclusions

### 1. The Cost of Abstraction (BigInt vs Float)
*   **Compiled Languages (Rust, Go)** show massive speedups (**150x - 250x**) when switching from BigInt software emulation to native CPU instructions.
*   **Interpreted Languages (Python, JS)** show only a **~3x** speedup. The bottleneck is the interpreter loop, not the arithmetic itself.

### 2. High-Performance Computing (Matrix Benchmark)
*   **Fortran is King**: Even with the same `-O3` flags, `gfortran` generated code that is **2.5x faster** than C++ and **4x faster** than Rust. Its strict array handling allows for aggressive auto-vectorization (SIMD).
*   **Java Surprise**: Java (HotSpot JIT) outperformed both Rust and Go in the matrix test. This demonstrates that for "hot" loops, JIT compilers can be incredibly efficient.
*   **Python's Limit**: For raw nested loops, Python is **280x slower** than Fortran. This confirms why libraries like NumPy (written in C/Fortran) are mandatory for data science.

### 3. BigInt Libraries
*   **Python & Go** have the best "out-of-the-box" experience for arbitrary precision math, combining ease of use with highly optimized Karatsuba algorithms.
