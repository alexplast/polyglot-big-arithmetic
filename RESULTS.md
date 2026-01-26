# Polyglot Benchmark Results

Generated on: 2026-01-26 04:59:42

## BigInt Performance

| Language | Factorial | Rel Speed | Fibonacci | Power | Type |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Go** | 6.298 ms | 1.00x | 38.863 ms | 0.160 ms | math/big |
| **Python** | 8.026 ms | 1.27x | 14.013 ms | 0.058 ms | Native |
| **Fortran** | 12.003 ms | 1.91x | 24.489 ms | 1.666 ms | Custom Base 10^9 |
| **JavaScript** | 12.562 ms | 1.99x | 23.900 ms | 0.194 ms | BigInt |
| **C** | 15.099 ms | 2.40x | 68.010 ms | 2.436 ms | Custom Base 10^9 |
| **Rust** | 16.740 ms | 2.66x | 103.222 ms | 2.140 ms | Custom Base 10^9 |
| **C++** | 26.556 ms | 4.22x | 116.724 ms | 1.902 ms | Custom Base 10^9 |
| **Java** | 56.005 ms | 8.89x | 57.507 ms | 0.068 ms | BigInteger |


![BigInt Performance Graph](results/plots/bigint.png)

---

## Float Throughput

| Language | Time | Rel Speed |
| :--- | :--- | :--- |
| **Rust** | 315.977 ms | 1.00x |
| **Java** | 324.032 ms | 1.03x |
| **Fortran** | 339.405 ms | 1.07x |
| **JavaScript** | 349.291 ms | 1.11x |
| **C++** | 427.000 ms | 1.35x |
| **C** | 433.794 ms | 1.37x |
| **Go** | 436.000 ms | 1.38x |
| **Python** | 15755.847 ms | 49.86x |


![Float Throughput Graph](results/plots/float.png)

---

## Matrix Multiplication

| Language | Time | Rel Speed |
| :--- | :--- | :--- |
| **Fortran** | 3.249 ms | 1.00x |
| **C** | 5.328 ms | 1.64x |
| **C++** | 6.523 ms | 2.01x |
| **Rust** | 7.356 ms | 2.26x |
| **Go** | 17.286 ms | 5.32x |
| **Java** | 26.448 ms | 8.14x |
| **JavaScript** | 39.464 ms | 12.15x |
| **Python** | 1164.536 ms | 358.43x |
| **Assembler** | — | — |


![Matrix Multiplication Graph](results/plots/matrix.png)

---

## Bubble Sort

| Language | Time | Rel Speed |
| :--- | :--- | :--- |
| **Assembler** | 14.204 ms | 1.00x |
| **Go** | 14.698 ms | 1.03x |
| **Rust** | 18.965 ms | 1.34x |
| **JavaScript** | 21.064 ms | 1.48x |
| **C++** | 22.529 ms | 1.59x |
| **C** | 22.680 ms | 1.60x |
| **Fortran** | 23.691 ms | 1.67x |
| **Java** | 24.025 ms | 1.69x |
| **Python** | 767.994 ms | 54.07x |


![Bubble Sort Graph](results/plots/sort.png)

---

