#include <iostream>
#include <cstdlib>
#include <chrono>
#include <iomanip>

int main() {
    const char* count_env = std::getenv("COUNT");
    int n = 1475;
    if (count_env) {
        n = std::atoi(count_env);
    }

    if (n < 0) return 0;
    
    // long double
    long double a = 0.0;
    long double b = 1.0;

    auto start = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < n; i++) {
        long double temp = a;
        a = b;
        b = temp + b;
    }
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::nanoseconds>(end - start);

    std::cout << "Result(F_" << n << "): " << std::scientific << std::setprecision(10) << a << std::endl;
    std::cout << "Time: " << std::fixed << std::setprecision(6) << duration.count() / 1000000.0 << " ms" << std::endl;

    return 0;
}
