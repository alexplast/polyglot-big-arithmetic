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
| **Go** | 0.810 ms | 1.00x | 1.942 ms | 0.102 ms | math/big |
| **Python** | 1.250 ms | 1.54x | 0.749 ms | 0.013 ms | Native |
| **Fortran** | 1.549 ms | 1.91x | 0.908 ms | 0.105 ms | Custom Base 10^9 |
| **Rust** | 1.658 ms | 2.05x | 1.322 ms | 0.097 ms | Custom Base 10^9 |
| **C** | 1.714 ms | 2.12x | 2.185 ms | 0.102 ms | Custom Base 10^9 |
| **C++** | 1.750 ms | 2.16x | 1.974 ms | 0.087 ms | Custom Base 10^9 |
| **JavaScript** | 3.415 ms | 4.22x | 3.446 ms | 0.098 ms | BigInt |
| **Java** | 10.108 ms | 12.48x | 5.206 ms | 0.030 ms | BigInteger |

<!-- BENCHMARK_BIGINT_END -->

### 2. BigInt vs Native Float
Sorted by native **Float CPU speed**.
**Settings**: Small numbers that fit in 64-bit float.

<!-- BENCHMARK_FLOAT_START -->
| Language | Float Time | Rel Speed | BigInt Time | Hardware Speedup |
| :--- | :--- | :--- | :--- | :--- |
| **C** | 0.0018 ms | 1.00x | 0.295 ms | 163.9x |
| **Rust** | 0.0020 ms | 1.11x | 0.333 ms | 166.5x |
| **Go** | 0.0020 ms | 1.11x | 0.334 ms | 167.0x |
| **Fortran** | 0.0020 ms | 1.11x | 0.088 ms | 44.0x |
| **C++** | 0.0023 ms | 1.28x | 0.263 ms | 114.3x |
| **Java** | 0.0310 ms | 17.22x | 1.747 ms | 56.4x |
| **Python** | 0.0690 ms | 38.33x | 0.173 ms | 2.5x |
| **JavaScript** | 0.1010 ms | 56.11x | 0.253 ms | 2.5x |

<!-- BENCHMARK_FLOAT_END -->

### 3. Matrix Multiplication (Native Performance)
Sorted by **Raw Throughput**.
Naive O(N^3) Matrix Multiplication (256x256), 1D arrays, 64-bit floats.

<!-- BENCHMARK_MATRIX_START -->
| Language | Matrix Mult (256x256) | Relative Speed |
| :--- | :--- | :--- |
| **C++** | 8.450 ms | 1.00x |
| **Assembler** | 9.323 ms | 1.10x |
| **C** | 10.427 ms | 1.23x |
| **Fortran** | 10.942 ms | 1.29x |
| **Rust** | 15.159 ms | 1.79x |
| **Java** | 37.831 ms | 4.48x |
| **Go** | 39.011 ms | 4.62x |
| **JavaScript** | 69.698 ms | 8.25x |
| **Python** | 2093.196 ms | 247.72x |

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
