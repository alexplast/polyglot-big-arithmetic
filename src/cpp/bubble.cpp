#include <iostream>
#include <vector>
#include <cstdlib>
#include <chrono>
#include <iomanip>
#include <cstdint>

int main() {
    int N = 10000;
    const char* n_env = std::getenv("SORT_SIZE");
    if (n_env) N = std::atoi(n_env);

    std::vector<double> arr(N);
    uint32_t seed = 42;
    for (int i = 0; i < N; i++) {
        seed = (seed * 1664525 + 1013904223);
        arr[i] = (double)seed / 4294967296.0;
    }

    auto start = std::chrono::high_resolution_clock::now();
    
    for (int i = 0; i < N - 1; i++) {
        for (int j = 0; j < N - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                std::swap(arr[j], arr[j + 1]);
            }
        }
    }

    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);

    std::cout << "Sort(" << N << "): ";
    std::cout << std::fixed << std::setprecision(4);
    for(int i=0; i<5; i++) std::cout << arr[i] << " ";
    std::cout << "... ";
    for(int i=N-5; i<N; i++) std::cout << arr[i] << " ";
    std::cout << "\n";

    std::cout << "Time: " << std::fixed << std::setprecision(3) << duration.count() / 1000.0 << " ms" << std::endl;
    return 0;
}
