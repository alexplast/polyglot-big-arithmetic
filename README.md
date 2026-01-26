# Polyglot Big Arithmetic Benchmark

This project explores the implementation of fundamental mathematical algorithms across **9 different programming languages**:
**Assembler (x64), C, C++, Go, Rust, Java, Fortran, Python, and JavaScript**.

The core objective is to compare how different languages handle large numbers, memory, and native arithmetic performance using a unified test harness.

## 📊 Results & Benchmarks

**👉 [CLICK HERE TO VIEW FULL BENCHMARK RESULTS & GRAPHS](RESULTS.md)**

The benchmark performs the following tests:

1.  **Arbitrary Precision (BigInt)**:
    *   Calculates Factorial (5000!), Fibonacci (25000th), and Power ($2^{20000}$).
    *   Compares native BigInt libraries (Go, Java, Python, JS) vs Custom implementations (C, C++, Rust, Fortran).
2.  **Float Throughput**:
    *   Measures raw CPU scalar loop performance (Fibonacci float loop).
3.  **Matrix Multiplication**:
    *   Multiplies two $200 \times 200$ matrices.
    *   Tests vectorization (SIMD) and memory cache efficiency.
4.  **Bubble Sort**:
    *   Sorts an array of 3,000 random doubles.
    *   Tests branch prediction and memory write speeds.

---

## 🛠 Project Structure

```text
.
├── Makefile            # Central build and run system
├── RESULTS.md          # Generated benchmark report with charts
├── README.md           # This file
├── bin/                # Compiled executables (ignored by git)
├── results/            # CSV data and PNG plots
├── src/                # Source code organized by language
│   ├── asm/            # Hand-written x64 Assembly (AVX2 optimized)
│   ├── c/              # C implementations
│   ├── cpp/            # C++ implementations
│   ├── fortran/        # Fortran implementations
│   ├── go/             # Go implementations
│   ├── java/           # Java implementations
│   ├── js/             # JavaScript (Node.js)
│   ├── python/         # Python scripts
│   └── rust/           # Rust implementations
└── tests/              # Benchmark runners and plot generators
```

## 🚀 Building and Running

### Prerequisites
*   **Compilers**: GCC, G++, GFortran, Rustc, Go, Javac.
*   **Interpreters**: Python 3, Node.js.
*   **Python Libs**: `matplotlib` (for plotting).

### Commands

*   **Run Everything**:
    Compiles all sources, generates test data, runs benchmarks, and updates `RESULTS.md`.
    ```bash
    make bench_all
    ```

*   **Clean**:
    Removes binaries and temporary data.
    ```bash
    make clean
    ```

*   **Specific Tests**:
    You can run specific groups via `make`:
    ```bash
    make fibo      # Compile Fibonacci tests
    make matrix    # Compile Matrix tests
    # ... etc
    ```