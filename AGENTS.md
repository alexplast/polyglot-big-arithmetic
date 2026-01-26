# Project Overview

A comprehensive comparative benchmark of fundamental mathematical algorithms across **9 programming languages**:
**Assembler (x64), C, C++, Go, Rust, Java, Fortran, Python, and JavaScript**.

The project measures performance in four distinct categories:
1.  **Arbitrary Precision (BigInt)**: Handling numbers larger than 64-bit registers using native libraries vs custom implementations.
2.  **Native Float Throughput**: Raw CPU scalar performance and loop overhead.
3.  **Matrix Multiplication**: Vectorization (SIMD) and memory efficiency.
4.  **Sorting**: Branch prediction and memory write speeds.

# Directory Structure

```text
.
├── Makefile            # Build system (GCC, GFortran, Go, Cargo, Javac)
├── README.md           # Project description
├── RESULTS.md          # Generated benchmark report with charts
├── bin/                # Compiled executables
├── results/            # Generated CSV reports and plots
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
    *   **Manual (Base $10^9$)**: C, C++, Rust, Fortran use a custom dynamic array implementation.

## 2. Float Throughput (Scalar Loop)
*   **Goal**: Measure compiler/interpreter loop overhead and scalar arithmetic speed.
*   **Method**: Run a small Fibonacci sequence 50,000 times.

## 3. Matrix Multiplication ($O(N^3)$)
*   **Goal**: Test vectorization (SIMD), cache locality, and memory management.
*   **Method**: Multiply two $200 \times 200$ matrices using 1D flat arrays.
*   **Optimization**:
    *   **Assembler**: Uses AVX2/FMA3 (`vfmadd231pd`) with Loop Unrolling (8x). Gracefully skips if CPU unsupported.
    *   **Fortran/C++**: Rely on compiler auto-vectorization (`-O3`).

## 4. Bubble Sort ($O(N^2)$)
*   **Goal**: Test Branch Prediction and Memory Writes.
*   **Method**: Sort an array of 3,000 pseudo-random `doubles` read from a binary file.
*   **Key**: Requires processors to handle unpredictable `if (a > b) swap` branches.
*   **Assembler**: Hand-optimized registers usage and stack alignment.

# Building and Running

*   `make all`: Compile all executables.
*   `make bench_all`: Run all benchmarks (median of 5), generate `RESULTS.md`, and plot graphs.
*   `make clean`: Remove binaries and results.