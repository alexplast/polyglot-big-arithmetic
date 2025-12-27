# Fibonacci & Factorial: A Multilanguage Comparative Study

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

## Conclusions
*   **Performance vs Complexity**: While Python and JS handle BigInt natively and conveniently, manual implementations in C++ or Rust allow for fine-tuned performance and memory control.
*   **Scalability**: By bypassing native hardware limits with custom software arithmetic, we made the "limited" compiled languages as capable as their interpreted counterparts for symbolic mathematics.
*   **Verification**: Automated cross-language verification is essential when implementing custom arithmetic to ensure no precision is lost during carry/borrow operations.
