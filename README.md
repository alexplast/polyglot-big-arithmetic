# Polyglot Big Arithmetic Benchmark

This project explores the implementation of fundamental mathematical algorithms across **9 different programming languages**:
**Assembler (x64), C, C++, Go, Rust, Java, Fortran, Python, and JavaScript**.

The core objective is to compare how different languages handle large numbers, memory, and native arithmetic performance using a unified test harness.

## 📊 Results & Benchmarks

**👉 [CLICK HERE TO VIEW FULL BENCHMARK RESULTS & GRAPHS](RESULTS.md)**

*Note: published benchmark results should be treated as environment-specific snapshots. Full reproducible runs are generated in Docker and now record environment metadata.*

The benchmark performs the following tests:

1.  **Arbitrary Precision (BigInt)**:
    *   Calculates Factorial (5000!), Fibonacci (25000th), and Power (2^20000).
    *   **External Libs**: C++ (`GMP`), Rust (`num-bigint`).
    *   **Native Libs**: Go (`math/big`), Java (`BigInteger`), Python, JS.
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
    ├── .github/            # CI workflows (verification + manual/tag benchmarks)
    ├── Dockerfile          # Environment definition (Ubuntu 24.04 + GMP)
    ├── Makefile            # Central build and run system
    ├── RESULTS.md          # Generated benchmark report with charts
    ├── bin/                # Compiled executables (ignored by git)
    ├── results/            # CSV data, plots and metadata JSON
    ├── src/                # Source code organized by language
    └── tests/              # Benchmark runners, plotting and verifiers

## 🚀 Building and Running

### Option 1: Running with Docker (Recommended)

This is the easiest way to run the benchmarks without installing 9 different compilers and libraries on your machine.

1.  **Build the image** (cached):

        make docker_build

2.  **Run Verification (Tests)**:

        make docker_test

3.  **Run Benchmarks**:

        make docker_run

    *Results will be saved to `RESULTS.md`, `results/*.csv`, `results/meta.json` and `results/plots/`.*

4.  **Run Fast Smoke Benchmarks**:

        make docker_smoke

### Option 2: Running Locally

**Prerequisites**: GCC, G++, GFortran, Rustc (cargo), Go, JDK 21+, Python 3, Node.js 22+, `libgmp-dev`.

For full local benchmark reports you also need `matplotlib`. If you only need timing data without plots, run the runner with `--no-plots` or use the smoke target.

On macOS the hand-written ASM targets are intentionally skipped: they use GNU assembler/Linux-specific directives and are validated through Docker/Linux runs instead.

*   **Verify Correctness**:

        make test

*   **Run Benchmarks**:

        make bench_all

*   **Run Fast Smoke Benchmarks**:

        make bench_smoke

*   **Run Benchmarks Without Plots**:

        python3 tests/runner.py --bench all --no-plots

*   **Clean**:

        make clean

## Reproducibility

Each benchmark run now records environment and run settings in `results/meta.json`, including:

- host platform and CPU information
- toolchain versions
- git branch and commit
- benchmark profile, run count, warmup count and data seed
- input sizes for each benchmark category

`RESULTS.md` includes the same metadata in an `Environment & Run Settings` section so timing tables can be interpreted against the actual machine they came from.

The sort input file is deterministic and seeded. By default:

- data file size: `10000`
- data seed: `1337`

You can override those values through Make variables, for example:

    make test DATA_SEED=2026
    make docker_run DATA_SEED=2026 RUNNER_ARGS="--runs 7 --warmup 2"

## CI Policy

CI is split into two paths:

- Pull requests run verification plus a Docker smoke benchmark.
- Full Docker benchmarks run only on `workflow_dispatch` or tags matching `bench-*`.

Manual workflow dispatch can optionally publish refreshed `RESULTS.md` and `results/` back to the selected branch. Tag-triggered runs upload artifacts but do not try to push commits.
