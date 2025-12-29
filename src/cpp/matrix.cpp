#include <iostream>
#include <vector>
#include <cstdlib>
#include <chrono>
#include <iomanip>

int main() {
    const char* n_env = std::getenv("MATRIX_SIZE");
    int N = 256;
    if (n_env) N = std::atoi(n_env);

    // Using 1D flat arrays for performance consistency
    std::vector<double> A(N * N, 1.0);
    std::vector<double> B(N * N, 1.0);
    std::vector<double> C(N * N, 0.0);

    // Initialize
    for(int i=0; i<N*N; ++i) {
        A[i] = 1.0 + (i % 100) * 0.01;
        B[i] = 1.0 - (i % 100) * 0.01;
    }

    auto start = std::chrono::high_resolution_clock::now();
    
    // Matrix Multiplication: C = A * B
    for (int i = 0; i < N; ++i) {
        for (int k = 0; k < N; ++k) {
            double r = A[i * N + k];
            for (int j = 0; j < N; ++j) {
                C[i * N + j] += r * B[k * N + j];
            }
        }
    }

    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);

    std::cout << "Matrix(" << N << "x" << N << ")" << std::endl;
    std::cout << "Result[0]: " << C[0] << std::endl; // Anti-optimization
    std::cout << "Time: " << std::fixed << std::setprecision(3) << duration.count() / 1000.0 << " ms" << std::endl;

    return 0;
}
