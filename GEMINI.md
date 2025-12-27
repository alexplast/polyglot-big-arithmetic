# Project Overview

A comparative implementation of Fibonacci, Factorial and Power algorithms across 7 languages (C++, Go, Rust, Java, Fortran, Python, JS). 

**Key Feature**: All implementations support **Arbitrary Precision** (BigInt). 
*   **Native Support**: Python, JavaScript, Go, Java.
*   **Manual Implementation**: C++, Rust, Fortran use a custom **Base $10^9$** digit-array implementation to efficiently bypass native bit-width limits.

# Directory Structure

*   `src/`: Source code by language.
*   `bin/`: Compiled executables.
*   `tests/`: Verification and benchmark scripts.

# Building and Running

*   `make all`: Build everything.
*   `make run COUNT=N`: Run all Fibonacci programs up to N.
*   `make run_factorial COUNT=N`: Run all Factorial programs up to N.
*   `make run_power BASE=A EXP=N`: Run all Power programs for A^N.
*   `make verify_all`: Verify correctness of all 21 programs.
*   `python3 tests/benchmark.py`: Run performance benchmark and update README.

# Implementation Notes

*   **Optimization (Base $10^9$)**: C++, Rust, and Fortran store numbers in chunks of 9 digits (0-999,999,999) inside 32/64-bit integers. This reduces memory usage by 9x and significantly speeds up arithmetic operations compared to a standard digit-by-digit approach.
*   **Arbitrary Precision**: Go (`math/big`), Java (`BigInteger`), JS (`BigInt`), and Python (native) use highly optimized standard libraries.
*   **Binary Exponentiation**: Power implementations use O(log n) algorithm.
*   **Standardized Output**: All programs output results in `Result(...): <value>` format and `Time: <val> ms` format.
