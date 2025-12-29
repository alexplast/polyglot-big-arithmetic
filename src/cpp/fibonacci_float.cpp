#include <iostream>
#include <cstdlib>
#include <chrono>
#include <iomanip>

int main() {
    const char* count_env = std::getenv("COUNT");
    int n = 1475;
    if (count_env) n = std::atoi(count_env);

    double a = 0.0, b = 1.0;
    
    auto start = std::chrono::high_resolution_clock::now();
    // Run 200,000 iterations to measure CPU throughput
    for (int k = 0; k < 200000; k++) {
        a = 0.0; b = 1.0;
        for (int i = 0; i < n; i++) {
            double temp = a;
            a = b;
            b = temp + b;
        }
    }
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);

    std::cout << "Result: " << a << std::endl;
    std::cout << "Time: " << std::fixed << std::setprecision(3) << duration.count() / 1000.0 << " ms" << std::endl;
    return 0;
}
