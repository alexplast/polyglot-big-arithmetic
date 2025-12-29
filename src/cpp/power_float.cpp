#include <iostream>
#include <cstdlib>
#include <chrono>
#include <iomanip>

// Binary exponentiation for long double
long double power(long double base, int exp) {
    long double result = 1.0;
    long double b = base;
    
    while (exp > 0) {
        if (exp % 2 == 1) {
            result *= b;
        }
        b *= b;
        exp /= 2;
    }
    
    return result;
}

int main() {
    const char* base_env = std::getenv("BASE");
    const char* exp_env = std::getenv("EXP");
    
    long double base = 2.0;
    int exp = 1023;
    
    if (base_env) base = std::strtold(base_env, nullptr);
    if (exp_env) exp = std::atoi(exp_env);

    auto start = std::chrono::high_resolution_clock::now();
    long double result = power(base, exp);
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::nanoseconds>(end - start);

    std::cout << "Result(" << (double)base << "^" << exp << "): " << std::scientific << std::setprecision(10) << result << std::endl;
    std::cout << "Time: " << std::fixed << std::setprecision(6) << duration.count() / 1000000.0 << " ms" << std::endl;

    return 0;
}
