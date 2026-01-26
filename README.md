# Polyglot Big Arithmetic Benchmark

This project explores the implementation of fundamental mathematical algorithms across **9 different programming languages**:
**Assembler (x64), C, C++, Go, Rust, Java, Fortran, Python, and JavaScript**.

The core objective is to compare how different languages handle large numbers, memory, and native arithmetic performance using a unified test harness.

## 📊 Results & Benchmarks

**👉 [CLICK HERE TO VIEW FULL BENCHMARK RESULTS & GRAPHS](RESULTS.md)**

The benchmark performs the following tests:

1.  **Arbitrary Precision (BigInt)**:
    *   Calculates Factorial (5000!), Fibonacci (25000th), and Power (2^20000).
    *   **Native/Lib**: Go (`math/big`), Java (`BigInteger`), Python, JS, **C++ (GMP)**, **Rust (num-bigint)**.
    *   **Custom (Naive)**: C, C++, Rust, Fortran (Base 10^9 implementation).
2.  **Float Throughput**:
    *   Measures raw CPU scalar loop performance (Fibonacci float loop).
3.  **Matrix Multiplication**:
    *   Multiplies two 200x200 matrices.
    *   Tests vectorization (SIMD) and memory cache efficiency.
    *   Includes **AVX2 Assembly** implementation.
4.  **Bubble Sort**:
    *   Sorts an array of 3,000 random doubles read from a binary file.
    *   Tests branch prediction and memory write speeds.

---

## 🛠 Project Structure

    .
    ├── .github/            # CI/CD workflows
    ├── Dockerfile          # Environment definition
    ├── Makefile            # Central build and run system
    ├── RESULTS.md          # Generated benchmark report with charts
    ├── bin/                # Compiled executables (ignored by git)
    ├── results/            # CSV data and PNG plots
    ├── src/                # Source code organized by language
    └── tests/              # Benchmark runners and verifiers

## 🚀 Building and Running

### Option 1: Running with Docker (Recommended)

This is the easiest way to run the benchmarks without installing 9 different compilers and libraries (like GMP) on your machine.

1.  **Build the image** (once):

        make docker_build

2.  **Run Verification (Tests)**:

        make docker_test

3.  **Run Benchmarks**:

        make docker_run

    *Results will be saved to `RESULTS.md` and `results/plots/`.*

### Option 2: Running Locally

**Prerequisites**: GCC, G++, GFortran, Rustc (cargo), Go, JDK 21+, Python 3, Node.js 22+, `libgmp-dev`.

*   **Verify Correctness**:

        make test

*   **Run Benchmarks**:

        make bench_all

*   **Clean**:

        make clean
