# Polyglot Benchmark Results

Generated on: 2026-04-22 23:50:09

## Environment & Run Settings

- Generated on: 2026-04-22 23:50:09
- Git: branch `master`, commit `b64c5f6`
- Host: Linux-6.8.0-100-generic-x86_64-with-glibc2.39
- CPU: Intel(R) Core(TM) i5-4250U CPU @ 1.30GHz
- Memory: 2013296 kB
- Toolchain: gcc `gcc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0`; g++ `g++ (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0`; gfortran `GNU Fortran (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0`; rustc `rustc 1.95.0 (59807616e 2026-04-14)`; go `go version go1.23.4 linux/amd64`; javac `javac 21.0.10`; python `Python 3.12.3`; node `v22.22.2`
- Run config: bench `all`, profile `full`, runs `5`, warmup `1`, data seed `1337`
- Problem sizes: factorial `5000`, fibonacci `25000`, power `2^20000`, float count `1475`, matrix `200`, sort `3000`

---
## BigInt Performance

| Language | Factorial | Rel Speed | Fibonacci | Power | Type |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **C++ (GMP)** | 2.701 ms | 1.00x | 11.018 ms | 0.025 ms | GMP Lib |
| **Rust (Lib)** | 5.733 ms | 2.12x | 17.890 ms | 0.018 ms | num-bigint |
| **Python** | 9.474 ms | 3.51x | 12.171 ms | 0.081 ms | Native |
| **Go** | 10.333 ms | 3.83x | 49.517 ms | 0.403 ms | math/big |
| **JavaScript** | 13.014 ms | 4.82x | 17.242 ms | 0.288 ms | BigInt |
| **C++** | 16.519 ms | 6.12x | 40.305 ms | 2.194 ms | Custom Base 10^9 |
| **Fortran** | 16.593 ms | 6.14x | 38.912 ms | 2.495 ms | Custom Base 10^9 |
| **C** | 16.733 ms | 6.20x | 81.723 ms | 2.631 ms | Custom Base 10^9 |
| **Rust** | 18.223 ms | 6.75x | 44.781 ms | 2.160 ms | Custom Base 10^9 |
| **Java** | 65.585 ms | 24.28x | 89.219 ms | 0.034 ms | BigInteger |


![BigInt Performance Graph](results/plots/bigint.png)

---

## Float Throughput

| Language | Time | Rel Speed |
| :--- | :--- | :--- |
| **Fortran** | 381.286 ms | 1.00x |
| **Rust** | 445.979 ms | 1.17x |
| **Java** | 455.496 ms | 1.19x |
| **JavaScript** | 466.383 ms | 1.22x |
| **C** | 471.239 ms | 1.24x |
| **Go** | 472.000 ms | 1.24x |
| **C++** | 473.841 ms | 1.24x |
| **Python** | 15577.582 ms | 40.86x |


![Float Throughput Graph](results/plots/float.png)

---

## Matrix Multiplication

| Language | Time | Rel Speed |
| :--- | :--- | :--- |
| **Assembler** | 3.806 ms | 1.00x |
| **C** | 4.684 ms | 1.23x |
| **Fortran** | 5.511 ms | 1.45x |
| **C++** | 5.912 ms | 1.55x |
| **Rust** | 8.753 ms | 2.30x |
| **Java** | 35.143 ms | 9.23x |
| **Go** | 39.205 ms | 10.30x |
| **JavaScript** | 71.110 ms | 18.68x |
| **Python** | 1932.223 ms | 507.68x |


![Matrix Multiplication Graph](results/plots/matrix.png)

---

## Bubble Sort

| Language | Time | Rel Speed |
| :--- | :--- | :--- |
| **Go** | 17.418 ms | 1.00x |
| **Rust** | 19.314 ms | 1.11x |
| **Assembler** | 29.332 ms | 1.68x |
| **Fortran** | 30.162 ms | 1.73x |
| **C++** | 30.855 ms | 1.77x |
| **JavaScript** | 36.719 ms | 2.11x |
| **Java** | 45.723 ms | 2.63x |
| **C** | 84.064 ms | 4.83x |
| **Python** | 973.823 ms | 55.91x |


![Bubble Sort Graph](results/plots/sort.png)

---

