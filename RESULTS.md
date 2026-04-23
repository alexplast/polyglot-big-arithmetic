# Polyglot Benchmark Results

Generated on: 2026-04-23 00:05:02

## Environment & Run Settings

- Generated on: 2026-04-23 00:05:02
- Git: branch `master`, commit `1e2312a`
- Host: Linux-6.17.0-1010-azure-x86_64-with-glibc2.39
- CPU: AMD EPYC 7763 64-Core Processor
- Memory: 16373464 kB
- Toolchain: gcc `gcc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0`; g++ `g++ (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0`; gfortran `GNU Fortran (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0`; rustc `rustc 1.95.0 (59807616e 2026-04-14)`; go `go version go1.23.4 linux/amd64`; javac `javac 21.0.10`; python `Python 3.12.3`; node `v22.22.2`
- Run config: bench `all`, profile `full`, runs `5`, warmup `1`, data seed `1337`
- Problem sizes: factorial `5000`, fibonacci `25000`, power `2^20000`, float count `1475`, matrix `200`, sort `3000`

---
## BigInt Performance

| Language | Factorial | Rel Speed | Fibonacci | Power | Type |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Rust (Lib)** | 1.635 ms | 1.00x | 3.618 ms | 0.006 ms | num-bigint |
| **C++ (GMP)** | 1.681 ms | 1.03x | 3.543 ms | 0.006 ms | GMP Lib |
| **Go** | 1.812 ms | 1.11x | 6.990 ms | 0.017 ms | math/big |
| **Python** | 4.275 ms | 2.61x | 6.169 ms | 0.034 ms | Native |
| **JavaScript** | 5.689 ms | 3.48x | 6.929 ms | 0.084 ms | BigInt |
| **C** | 9.256 ms | 5.66x | 43.537 ms | 1.422 ms | Custom Base 10^9 |
| **Fortran** | 9.299 ms | 5.69x | 17.539 ms | 1.078 ms | Custom Base 10^9 |
| **C++** | 9.323 ms | 5.70x | 21.123 ms | 1.061 ms | Custom Base 10^9 |
| **Rust** | 9.340 ms | 5.71x | 27.796 ms | 1.202 ms | Custom Base 10^9 |
| **Java** | 18.162 ms | 11.11x | 17.517 ms | 0.017 ms | BigInteger |


![BigInt Performance Graph](results/plots/bigint.png)

---

## Float Throughput

| Language | Time | Rel Speed |
| :--- | :--- | :--- |
| **Rust** | 264.280 ms | 1.00x |
| **Java** | 267.710 ms | 1.01x |
| **Fortran** | 269.594 ms | 1.02x |
| **C** | 269.811 ms | 1.02x |
| **C++** | 269.877 ms | 1.02x |
| **Go** | 273.000 ms | 1.03x |
| **JavaScript** | 277.404 ms | 1.05x |
| **Python** | 10216.547 ms | 38.66x |


![Float Throughput Graph](results/plots/float.png)

---

## Matrix Multiplication

| Language | Time | Rel Speed |
| :--- | :--- | :--- |
| **Assembler** | 1.176 ms | 1.00x |
| **Fortran** | 1.504 ms | 1.28x |
| **C** | 1.728 ms | 1.47x |
| **Rust** | 1.925 ms | 1.64x |
| **C++** | 2.612 ms | 2.22x |
| **Go** | 7.222 ms | 6.14x |
| **Java** | 11.296 ms | 9.61x |
| **JavaScript** | 16.967 ms | 14.43x |
| **Python** | 598.606 ms | 509.02x |


![Matrix Multiplication Graph](results/plots/matrix.png)

---

## Bubble Sort

| Language | Time | Rel Speed |
| :--- | :--- | :--- |
| **Assembler** | 5.597 ms | 1.00x |
| **Rust** | 5.706 ms | 1.02x |
| **Go** | 6.292 ms | 1.12x |
| **JavaScript** | 12.314 ms | 2.20x |
| **Java** | 13.469 ms | 2.41x |
| **C++** | 20.209 ms | 3.61x |
| **Fortran** | 20.267 ms | 3.62x |
| **C** | 20.287 ms | 3.62x |
| **Python** | 342.244 ms | 61.15x |


![Bubble Sort Graph](results/plots/sort.png)

---

