# Polyglot Benchmark Results

Generated on: 2026-01-26 04:44:50

## BigInt Performance

| Language | Factorial | Rel Speed | Fibonacci | Power | Type |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Rust (Lib)** | 1.533 ms | 1.00x | 3.587 ms | 0.006 ms | num-bigint |
| **C++ (GMP)** | 1.682 ms | 1.10x | 3.522 ms | 0.005 ms | GMP Lib |
| **Go** | 1.875 ms | 1.22x | 6.729 ms | 0.017 ms | math/big |
| **Python** | 4.274 ms | 2.79x | 6.074 ms | 0.035 ms | Native |
| **JavaScript** | 5.622 ms | 3.67x | 6.889 ms | 0.088 ms | BigInt |
| **C** | 9.253 ms | 6.04x | 43.413 ms | 1.388 ms | Custom Base 10^9 |
| **Rust** | 9.275 ms | 6.05x | 27.716 ms | 1.201 ms | Custom Base 10^9 |
| **C++** | 9.285 ms | 6.06x | 21.005 ms | 1.056 ms | Custom Base 10^9 |
| **Fortran** | 9.294 ms | 6.06x | 17.475 ms | 1.081 ms | Custom Base 10^9 |
| **Java** | 18.578 ms | 12.12x | 17.905 ms | 0.018 ms | BigInteger |


![BigInt Performance Graph](results/plots/bigint.png)

---

## Float Throughput

| Language | Time | Rel Speed |
| :--- | :--- | :--- |
| **Rust** | 263.890 ms | 1.00x |
| **Java** | 267.158 ms | 1.01x |
| **Fortran** | 269.491 ms | 1.02x |
| **C++** | 269.587 ms | 1.02x |
| **C** | 269.611 ms | 1.02x |
| **Go** | 272.000 ms | 1.03x |
| **JavaScript** | 277.458 ms | 1.05x |
| **Python** | 7836.693 ms | 29.70x |


![Float Throughput Graph](results/plots/float.png)

---

## Matrix Multiplication

| Language | Time | Rel Speed |
| :--- | :--- | :--- |
| **Fortran** | 1.495 ms | 1.00x |
| **C** | 1.773 ms | 1.19x |
| **Rust** | 2.075 ms | 1.39x |
| **C++** | 2.603 ms | 1.74x |
| **Go** | 7.514 ms | 5.03x |
| **Java** | 14.067 ms | 9.41x |
| **JavaScript** | 17.658 ms | 11.81x |
| **Python** | 588.698 ms | 393.78x |
| **Assembler** | — | — |


![Matrix Multiplication Graph](results/plots/matrix.png)

---

## Bubble Sort

| Language | Time | Rel Speed |
| :--- | :--- | :--- |
| **Assembler** | 5.690 ms | 1.00x |
| **Rust** | 6.165 ms | 1.08x |
| **Go** | 6.553 ms | 1.15x |
| **JavaScript** | 13.023 ms | 2.29x |
| **Java** | 13.630 ms | 2.40x |
| **C++** | 20.333 ms | 3.57x |
| **C** | 20.368 ms | 3.58x |
| **Fortran** | 20.427 ms | 3.59x |
| **Python** | 371.942 ms | 65.37x |


![Bubble Sort Graph](results/plots/sort.png)

---

