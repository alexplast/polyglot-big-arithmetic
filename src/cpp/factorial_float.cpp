#include <iostream>
#include <cstdlib>
#include <chrono>
#include <iomanip>

int main() {
    const char* count_env = std::getenv("COUNT");
    int count = 170;
    if (count_env) {
        count = std::atoi(count_env);
    }

    // Use long double for extended precision (80-bit or 128-bit depending on OS/Compiler)
    long double factorial = 1.0;
    
    auto start = std::chrono::high_resolution_clock::now();
    for (int i = 1; i <= count; ++i) {
        factorial *= static_cast<long double>(i);
    }
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::nanoseconds>(end - start);

    std::cout << "Result(" << count << "!): " << std::scientific << std::setprecision(10) << factorial << std::endl;
    // Use fixed precision to ensure regex captures small values (e.g., 0.000012)
    std::cout << "Time: " << std::fixed << std::setprecision(6) << duration.count() / 1000000.0 << " ms" << std::endl;

    return 0;
}
