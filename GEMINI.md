# Project Overview

A comprehensive comparative benchmark of fundamental mathematical algorithms across **9 programming languages**: 
**Assembler (x64), C, C++, Go, Rust, Java, Fortran, Python, and JavaScript**.

The project measures performance in three distinct categories:
1.  **Arbitrary Precision (BigInt)**: Handling numbers larger than 64-bit registers.
2.  **Native Float Throughput**: Raw CPU scalar performance and loop overhead.
3.  **High-Performance Computing**: Matrix multiplication tests for vectorization (SIMD) and memory efficiency.

# Directory Structure

```text
.
├── Makefile            # Build system (GCC, GFortran, Go, Cargo, Javac)
├── README.md           # Results and analysis
├── bin/                # Compiled executables
├── results/            # Generated CSV reports
├── src/                # Source code
│   ├── asm/            # Hand-written x64 Assembly (GAS syntax)
│   ├── c/              # Pure C implementations
│   ├── cpp/            # C++ implementations
│   ├── fortran/        # Fortran implementations
│   ├── go/             # Go implementations
│   ├── java/           # Java implementations
│   ├── js/             # JavaScript (Node.js)
│   ├── python/         # Python scripts
│   └── rust/           # Rust implementations
└── tests/              # Benchmark automation scripts (Python)
```

# Benchmarks

## 1. BigInt (Factorial, Fibonacci, Power)
*   **Goal**: Compare native library speed vs. manual implementation overhead.
*   **Implementations**:
    *   **Native**: Python, Go (`math/big`), Java (`BigInteger`), JS (`BigInt`).
    *   **Manual (Base $10^9$)**: C, C++, Rust, Fortran use a custom dynamic array implementation storing 9 digits per 64-bit integer.

## 2. Float Throughput (Scalar Loop)
*   **Goal**: Measure compiler/interpreter loop overhead and scalar arithmetic speed.
*   **Method**: Run a small Fibonacci sequence 200,000 times.
*   **Metric**: Median time of 5 runs.

## 3. Matrix Multiplication ($O(N^3)$)
*   **Goal**: Test vectorization (SIMD), cache locality, and memory management.
*   **Method**: Multiply two $600 \times 600$ matrices using 1D flat arrays.
*   **Optimization**: 
    *   **Assembler**: Uses SSE2 (`mulpd`/`addpd`) with Loop Unrolling (8 doubles per stride).
    *   **Fortran/C++**: Rely on compiler auto-vectorization (`-O3`).

# Building and Running

*   `make all`: Compile all executables.
*   `make bench_all`: Run all benchmarks (median of 5), update `README.md`, and generate CSV files in `results/`.
*   `make clean`: Remove binaries and results.

# Implementation Notes

*   **Assembler**: Written in GAS (GNU Assembler) Intel syntax to ensure compatibility with standard GCC toolchains without requiring `nasm`.
*   **Fortran**: Uses standard `real(kind=8)` (64-bit double) for fair hardware comparison against C/C++.
*   **Output**: All scripts generate both Markdown tables (console/README) and machine-readable CSV files.
