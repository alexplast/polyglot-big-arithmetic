# Project Overview

A comparative implementation of Fibonacci, Factorial and Power algorithms across 7 languages (C++, Go, Rust, Java, Fortran, Python, JS). 

**Key Feature**: All implementations support **Arbitrary Precision** (BigInt). Compiled languages (C++, Rust, Fortran) use a custom digit-array implementation to bypass native bit-width limits.

# Directory Structure

*   `src/`: Source code by language.
*   `bin/fibo/`: Fibonacci executables.
*   `bin/fact/`: Factorial executables.
*   `bin/power/`: Power (exponentiation) executables.
*   `tests/`: Python-based ground-truth verification.

# Building and Running

*   `make fibo`: Build only Fibonacci.
*   `make fact`: Build only Factorial.
*   `make power`: Build only Power.
*   `make all`: Build everything.
*   `make run COUNT=N`: Run all Fibonacci programs up to N.
*   `make run_factorial COUNT=N`: Run all Factorial programs up to N.
*   `make run_power BASE=A EXP=N`: Run all Power programs for A^N.
*   `make verify_all`: Verify correctness of all 21 programs (7 fibo + 7 fact + 7 power).

# Implementation Notes

*   **Custom BigInt**: Implemented in C++, Rust, and Fortran to handle values exceeding 128-bit capacity.
*   **Arbitrary Precision**: Go (`math/big`), Java (`BigInteger`), JS (`BigInt`), and Python (native) are used where available.
*   **Binary Exponentiation**: Power implementations use O(log n) algorithm for efficient computation.
*   **Performance Measurement**: All implementations include execution time measurement (in milliseconds).
*   **Standardized Output**: All programs output results in `Result(...): <value>` format and `Time: <val> ms` format.
