# Polyglot Big Arithmetic

This project explores the implementation of fundamental mathematical algorithms (Fibonacci Sequence and Factorial) across 7 different programming languages: **C++, Go, Rust, Java, Fortran, Python, and JavaScript**.

The core objective is to compare how different languages handle large numbers, memory, and native integer limitations.

## Project Structure

```text
.
├── Makefile            # Central build and run system
├── README.md           # Project documentation (you are here)
├── GEMINI.md           # Technical metadata
├── bin/                # Compiled executables
│   ├── fact/           # Factorial binaries
│   └── fibo/           # Fibonacci binaries
├── src/                # Source code organized by language
│   ├── cpp/
│   ├── fortran/
│   ├── go/
│   ├── java/
│   ├── js/
│   ├── python/
│   └── rust/
└── tests/              # Automated verification scripts
```

## Technical Implementation Details

### The Challenge of Large Numbers
The project highlights the difference between **Fixed-Width Integers** and **Arbitrary-Precision (BigInt) Integers**.

1.  **Fixed-Width (Natively in C++, Rust, Fortran)**:
    *   Standard types like `long long` (64-bit) or `u128` (128-bit) have a hard physical limit.
    *   For example, a 64-bit integer overflows at **20!**.
    *   A 128-bit integer overflows at **34!**.
2.  **Arbitrary-Precision (Python, JS, Go, Java)**:
    *   These languages use dynamic memory to store numbers as arrays of digits.
    *   They are only limited by the available RAM.

### Our Solution: Manual BigInt
To ensure parity across all languages, we implemented **Manual BigInt logic** in the compiled languages (C++, Rust, Fortran).
*   **Logic**: Instead of relying on CPU registers, we store numbers as vectors/arrays of digits.
*   **Arithmetic**: We implemented "pencil and paper" algorithms for addition (Fibonacci) and multiplication (Factorial).
*   **Result**: All 7 implementations can now calculate extremely large values (e.g., **10,000!**) accurately.

## How to Use

### Build
To build only Fibonacci binaries:
```bash
make fibo
```
To build only Factorial binaries:
```bash
make fact
```
To build everything:
```bash
make all
```

### Run
Run with a specific count (default is 10):
```bash
make run COUNT=1000           # Run Fibonacci
make run_factorial COUNT=200  # Run Factorial
```

### Verify
Automated tests compare result outputs against Python's ground truth:
```bash
make verify_all COUNT=1000
```

## Performance Comparison

We benchmarked all 7 implementations with a significant number of iterations to compare performance.

**Benchmark settings:**
- **Fibonacci**: $N = 5000$
- **Factorial**: $N = 2000$

| Language | Fibonacci (5000) | Factorial (2000) | BigInt Type |
| :--- | :--- | :--- | :--- |
| **C++** | 1.848 ms | 43.141 ms | Custom Digit Array |
| **Rust** | 2.502 ms | 31.026 ms | Custom Digit Array |
| **Go** | 2.094 ms | 1.045 ms | `math/big` |
| **Java** | 1.300 ms | 15.684 ms | `BigInteger` |
| **Python** | 0.814 ms | 1.258 ms | Native |
| **JavaScript** | 1.487 ms | 3.349 ms | `BigInt` |
| **Fortran** | 3.836 ms | 4.713 ms | Custom Digit Array |

### Observations
*   **Winner**: **Python** performed best in Fibonacci (as it's extremely well-optimized for BigInt), while **Go** and **Python** were leaders in Factorial.
*   **Custom Implementations**: Our manual implementations in C++ and Rust performed well, but are currently less optimized than the native BigInt implementations of languages like Go and Python, which use highly tuned assembly/C backends.
*   **Fortran**: The custom implementation in Fortran is functional but slower than highly optimized built-in BigInt libraries.

## Conclusions
*   **Performance vs Complexity**: Native BigInt (Python, JS) is both faster and easier to write. However, manual BigInt (C++, Rust) demonstrates the underlying mechanics of arbitrary-precision arithmetic.
*   **Optimization**: Languages with native BigInt support (Go, Java, JS, Python) leverage years of optimization. Our C++/Rust/Fortran implementations use basic algorithms.
*   **Scalability**: All 7 implementations successfully handle inputs that would overflow standard hardware types.
