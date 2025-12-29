# Project Overview

A comparative implementation of Fibonacci, Factorial, Power, and Matrix algorithms across 7 languages (C++, Go, Rust, Java, Fortran, Python, JS). 

**Key Features**: 
1.  **Arbitrary Precision** (BigInt) for huge number calculation.
2.  **Native Float** comparisons for measuring abstraction overhead.
3.  **Matrix Multiplication** for testing compiler vectorization and raw throughput.

# Directory Structure

*   `src/`: Source code by language.
    *   `src/<lang>/matrix.ext`: Naive O(N^3) matrix multiplication.
    *   `src/<lang>/*_float.ext`: IEEE 754 implementations.
    *   `src/<lang>/*.ext`: BigInt implementations.
*   `bin/`: Compiled executables.
*   `tests/`: Verification and benchmark scripts.

# Building and Running

*   `make all`: Build everything.
*   `make bench_all`: Run all 3 benchmarks (BigInt, Float, Matrix) and update README.

# Implementation Notes

*   **Matrix Optimization**: We use flattened 1D arrays for matrices in all languages to ensure cache locality and fair comparison.
*   **Optimization (Base 10^9)**: C++, Rust, and Fortran BigInts store numbers in chunks of 9 digits inside 64-bit integers.
*   **Arbitrary Precision**: Go (`math/big`), Java (`BigInteger`), JS (`BigInt`), and Python (native).
