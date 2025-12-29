# Project Overview

A comprehensive comparative benchmark of fundamental mathematical algorithms across **9 programming languages**: 
**Assembler (x64), C, C++, Go, Rust, Java, Fortran, Python, and JavaScript**.

The project measures performance in four distinct categories:
1.  **Arbitrary Precision (BigInt)**: Handling numbers larger than 64-bit registers.
2.  **Native Float Throughput**: Raw CPU scalar performance and loop overhead.
3.  **Matrix Multiplication**: Vectorization (SIMD) and memory efficiency.
4.  **Sorting**: Branch prediction and memory write speeds.

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
    *   **Manual (Base $10^9$)**: C, C++, Rust, Fortran use a custom dynamic array implementation.

## 2. Float Throughput (Scalar Loop)
*   **Goal**: Measure compiler/interpreter loop overhead and scalar arithmetic speed.
*   **Method**: Run a small Fibonacci sequence 200,000 times.

## 3. Matrix Multiplication ($O(N^3)$)
*   **Goal**: Test vectorization (SIMD), cache locality, and memory management.
*   **Method**: Multiply two $600 \times 600$ matrices using 1D flat arrays.
*   **Optimization**: 
    *   **Assembler**: Uses SSE2 (`mulpd`/`addpd`) with Loop Unrolling.
    *   **Fortran/C++**: Rely on compiler auto-vectorization (`-O3`).

## 4. Bubble Sort ($O(N^2)$)
*   **Goal**: Test Branch Prediction and Memory Writes.
*   **Method**: Sort an array of 10,000 pseudo-random `doubles` generated via LCG.
*   **Key**: Requires processors to handle unpredictable `if (a > b) swap` branches.

# Building and Running

*   `make all`: Compile all executables.
*   `make bench_all`: Run all benchmarks (median of 5), update `README.md`, and generate CSV files in `results/`.
*   `make clean`: Remove binaries and results.
