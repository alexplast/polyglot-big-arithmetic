# Polyglot Big Arithmetic

This project explores the implementation of fundamental mathematical algorithms (Fibonacci Sequence, Factorial, and Power) across 7 different programming languages: **C++, Go, Rust, Java, Fortran, Python, and JavaScript**.

The core objective is to compare how different languages handle large numbers, memory, and native integer limitations.

## Project Structure

```text
.
├── Makefile            # Central build and run system
├── README.md           # Project documentation
├── GEMINI.md           # Technical metadata
├── bin/                # Compiled executables
├── src/                # Source code organized by language
└── tests/              # Verification and benchmark scripts
    ├── benchmark.py    # BigInt benchmark
    └── benchmark_float.py # Float vs BigInt benchmark
```

## Technical Implementation Details

### The Challenge of Large Numbers
The project highlights the difference between **Fixed-Width Integers** and **Arbitrary-Precision (BigInt) Integers**.

1.  **Fixed-Width (Natively in C++, Rust, Fortran)**:
    *   Standard types like `long long` (64-bit) overflow quickly (e.g., 20! or 2^63).
2.  **Arbitrary-Precision (Python, JS, Go, Java)**:
    *   These languages use dynamic memory to store numbers as arrays of digits.

### Our Solution: Optimized Manual BigInt
To ensure parity, we implemented **Manual BigInt logic** in the compiled languages (C++, Rust, Fortran).
*   **Base $10^9$ Optimization**: Instead of storing one digit per array element (Base 10), we store **9 digits** (values up to 999,999,999) in each integer block.
*   **Effect**: This reduces the number of operations and memory usage by a factor of ~9.

## Performance Comparison (BigInt)

**Benchmark settings:** $N=5000$ (Fibonacci), $N=2000$ (Factorial), $2^{5000}$ (Power).

| Language | Fibonacci (5000) | Factorial (2000) | Power (2^5000) | BigInt Type |
| :--- | :--- | :--- | :--- | :--- |
| **C++** | 8.814 ms | 85.029 ms | 57.478 ms | Custom Base 10^9 |
| **Rust** | 17.826 ms | 190.995 ms | 123.535 ms | Custom Base 10^9 |
| **Go** | 1.668 ms | 0.838 ms | 0.052 ms | math/big |
| **Java** | 10.558 ms | 10.662 ms | 0.029 ms | BigInteger |
| **Python** | 0.860 ms | 1.244 ms | 0.021 ms | Native |
| **JavaScript** | 2.769 ms | 5.429 ms | 0.101 ms | BigInt |
| **Fortran** | 3.794 ms | 64.983 ms | 29.143 ms | Custom Base 10^9 |

## Experiment: BigInt vs Native Float

We ran a secondary benchmark to measure the overhead of "BigInt" abstraction against native CPU floating-point arithmetic (IEEE 754 `double`).
*   **Inputs**: Reduced to fit in 64-bit float (Fibonacci 1475, Factorial 170, Power 2^1023).
*   **Speedup**: Represents how much faster Native Float is compared to BigInt on small numbers.

| Language | Alg | BigInt Time | Float Time | Speedup |
| :--- | :--- | :--- | :--- | :--- |
| **Rust** | Fibo | 2.324 ms | 0.013 ms | **178.8x** |
| | Fact | 0.148 ms | 0.003 ms | **49.3x** |
| **Go** | Fibo | 0.503 ms | 0.002 ms | **251.5x** |
| | Fact | 0.028 ms | 0.001 ms | **28.0x** |
| **Java** | Fact | 0.996 ms | 0.003 ms | **332.0x** |
| **Python** | Fibo | 0.202 ms | 0.072 ms | **2.8x** |
| **JavaScript**| Fibo | 0.234 ms | 0.076 ms | **3.1x** |

### Conclusions
1.  **Hardware Dominance**: Compiled languages (Rust, Go) show massive speedups (**50x - 300x**) when switching to native CPU instructions. This demonstrates the heavy cost of software-defined arbitrary precision arithmetic.
2.  **The Interpreter Floor**: Interpreted languages (Python, JS) show only a **~3x** speedup. The bottleneck here is the interpreter loop (instruction dispatch), not the arithmetic itself.
3.  **Optimization Anomalies**: In some cases (like Power), native Float in Python/JS was actually *slower* than BigInt. This is because the BigInt `pow()` implementation in these languages is highly optimized C code, whereas the Float path incurs type conversion overheads that outweigh the calculation cost for small numbers.

## How to Use

### Build
```bash
make all      # Build BigInt versions
make float    # Build Float versions
```

### Run Benchmarks
```bash
python3 tests/benchmark.py        # Run BigInt Benchmark
python3 tests/benchmark_float.py  # Run Float Comparison
```