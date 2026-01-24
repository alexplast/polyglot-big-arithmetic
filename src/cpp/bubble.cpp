#include <iostream>
#include <vector>
#include <cstdlib>
#include <chrono>
#include <iomanip>
#include <fstream>

int main() {
    int N = 10000;
    const char* n_env = std::getenv("SORT_SIZE");
    if (n_env) N = std::atoi(n_env);

    std::vector<double> arr(N);

    // Read from binary file
    std::ifstream file("data.bin", std::ios::binary);
    if (!file) {
        std::cerr << "Error: 'data.bin' not found. Run 'python3 tests/gen_data.py' first.\n";
        return 1;
    }
    file.read(reinterpret_cast<char*>(arr.data()), N * sizeof(double));
    
    if (!file) {
        std::cerr << "Warning: Could not read all " << N << " elements.\n";
    }
    file.close();

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
    int print_limit = (N < 5) ? N : 5;
    for(int i=0; i<print_limit; i++) std::cout << arr[i] << " ";
    std::cout << "... ";
    if (N > 5) {
        for(int i=N-5; i<N; i++) std::cout << arr[i] << " ";
    }
    std::cout << "\n";

    std::cout << "Time: " << std::fixed << std::setprecision(3) << duration.count() / 1000.0 << " ms" << std::endl;
    return 0;
}
