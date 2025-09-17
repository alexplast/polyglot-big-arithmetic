# Project Overview

This project contains implementations of the Fibonacci sequence in multiple programming languages: C++, Go, Rust, Java, Fortran, Python, and JavaScript. It serves as a comparative showcase of how the same algorithm is expressed in different languages.

Each implementation is a standalone program that calculates and prints a specified number of Fibonacci numbers. The number of elements to generate is controlled by the `COUNT` environment variable.

# Building and Running

A `Makefile` is provided to streamline the build, run, and clean processes for all language implementations.

## Key Commands

*   **Build all compiled programs:**
    ```bash
    make all
    ```
    This command compiles the C++, Go, Rust, Java, and Fortran source files into executables.

*   **Run all implementations:**
    ```bash
    make run
    ```
    This will execute all seven programs. You can specify the number of Fibonacci elements by setting the `COUNT` variable:
    ```bash
    make run COUNT=20
    ```

*   **Clean up compiled files:**
    ```bash
    make clean
    ```
    This command removes all generated executables and class files.

# Development Conventions

*   **Configuration:** All programs read the `COUNT` environment variable to determine how many Fibonacci numbers to generate. If `COUNT` is not set, it defaults to `10`.
*   **Output:** Each program prints the Fibonacci sequence to standard output, followed by a newline.
*   **Large Number Support:**
    *   Implementations in Python, Rust, Go, Java, and JavaScript use arbitrary-precision integers (`BigInt`) to correctly handle very large numbers in the sequence.
    *   The C++ and Fortran versions use `unsigned long long` and `integer(kind=8)` respectively. They include checks to detect and report an error if an integer overflow occurs.
