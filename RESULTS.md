# Polyglot Benchmark Results

Generated on: 2026-01-26 04:19:13

## BigInt Performance

| Language | Factorial | Rel Speed | Fibonacci | Power | Type |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **C++ (GMP)** | 2.399 ms | 1.00x | 9.010 ms | 0.018 ms | GMP Lib |
| **Rust (Lib)** | 2.483 ms | 1.04x | 10.249 ms | 0.023 ms | num-bigint |
| **Go** | 4.425 ms | 1.84x | 23.721 ms | 0.135 ms | math/big |
| **Python** | 8.870 ms | 3.70x | 12.227 ms | 0.057 ms | Native |
| **JavaScript** | 11.303 ms | 4.71x | 17.923 ms | 0.192 ms | BigInt |
| **Fortran** | 11.872 ms | 4.95x | 25.318 ms | 1.399 ms | Custom Base 10^9 |
| **Rust** | 12.415 ms | 5.18x | 35.178 ms | 1.788 ms | Custom Base 10^9 |
| **C** | 13.073 ms | 5.45x | 73.380 ms | 1.955 ms | Custom Base 10^9 |
| **C++** | 16.971 ms | 7.07x | 32.735 ms | 1.732 ms | Custom Base 10^9 |
| **Java** | 45.855 ms | 19.11x | 61.384 ms | 0.028 ms | BigInteger |


![BigInt Performance Graph](results/plots/bigint.png)

---

## Float Throughput

| Language | Time | Rel Speed |
| :--- | :--- | :--- |
| **Rust** | 329.134 ms | 1.00x |
| **Java** | 329.850 ms | 1.00x |
| **Fortran** | 338.673 ms | 1.03x |
| **C++** | 440.215 ms | 1.34x |
| **C** | 440.871 ms | 1.34x |
| **Go** | 441.000 ms | 1.34x |
| **JavaScript** | 481.905 ms | 1.46x |
| **Python** | 16735.120 ms | 50.85x |


![Float Throughput Graph](results/plots/float.png)

---

## Matrix Multiplication

| Language | Time | Rel Speed |
| :--- | :--- | :--- |
| **Fortran** | 4.493 ms | 1.00x |
| **C** | 5.650 ms | 1.26x |
| **Rust** | 6.853 ms | 1.53x |
| **C++** | 8.464 ms | 1.88x |
| **Go** | 15.472 ms | 3.44x |
| **Java** | 24.403 ms | 5.43x |
| **JavaScript** | 39.905 ms | 8.88x |
| **Python** | 1210.352 ms | 269.39x |
| **Assembler** | — | — |


![Matrix Multiplication Graph](results/plots/matrix.png)

---

## Bubble Sort

| Language | Time | Rel Speed |
| :--- | :--- | :--- |
| **Rust** | 11.851 ms | 1.00x |
| **Go** | 12.617 ms | 1.06x |
| **Assembler** | 13.896 ms | 1.17x |
| **Fortran** | 22.374 ms | 1.89x |
| **C++** | 22.383 ms | 1.89x |
| **Java** | 23.445 ms | 1.98x |
| **C** | 23.868 ms | 2.01x |
| **JavaScript** | 28.326 ms | 2.39x |
| **Python** | 731.614 ms | 61.73x |


![Bubble Sort Graph](results/plots/sort.png)

---

